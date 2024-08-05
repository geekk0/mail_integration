import json
import time
import threading
import imapclient
import email

from typing import Any
from channels.generic.websocket import WebsocketConsumer
from email.utils import parsedate_to_datetime
from django.utils import timezone


from .models import EmailMessage, EmailAccount
from .utils import get_emails_qty, decode_mime_words, get_text_from_email, get_attachments_from_email


class EmailConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'status': 'Чтение сообщений ...'
        }))
        print("WebSocket connected")  # Debugging line
        self.send_progress_updates()

    def send_progress_updates(self):
        def progress():
            email_account = EmailAccount.objects.first()
            total_emails = get_emails_qty(email_account)  # Get the total number of emails
            self.send(text_data=json.dumps({
                'status': 'Чтение сообщений, всего: ' + str(total_emails),
            }))
            server = imapclient.IMAPClient(email_account.imap_server, ssl=True)
            server.login(email_account.email, email_account.password)
            server.select_folder('INBOX', readonly=True)

            messages = server.search(['NOT', 'DELETED'])
            total_emails = len(messages)  # Get the total number of emails

            for i, msgid in enumerate(messages):
                data = server.fetch([msgid], 'RFC822')[msgid]
                msg = email.message_from_bytes(data[b'RFC822'])
                subject = decode_mime_words(msg['subject'])

                # Parse the date strings into datetime objects
                sent_date = parsedate_to_datetime(msg['date'])
                received_date = parsedate_to_datetime(msg['date'])

                # Make the datetime objects timezone-aware if they are naive
                if timezone.is_naive(sent_date):
                    sent_date = timezone.make_aware(sent_date)
                if timezone.is_naive(received_date):
                    received_date = timezone.make_aware(received_date)

                # Extract text content from the email
                description = get_text_from_email(msg)

                # Extract attachments from the email
                attachments = get_attachments_from_email(msg)

                if not EmailMessage.objects.filter(subject=subject, sent_date=sent_date).exists():
                    # Extract text content from the email
                    description = get_text_from_email(msg)

                    # Extract attachments from the email
                    attachments = get_attachments_from_email(msg)

                    EmailMessage.objects.create(
                        subject=subject,
                        sent_date=sent_date,
                        received_date=received_date,
                        description=description,
                        attachments=attachments,  # Save attachments
                        email_account=email_account
                    )

                unprocessed_emails = total_emails - (i + 1)
                progress_percentage = int(((i + 1) / total_emails) * 100)
                email_data = {
                    'id': msgid,
                    'subject': subject,
                    'sent_date': sent_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'received_date': received_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'description': description,
                    'attachments': attachments
                }
                self.send(text_data=json.dumps({
                    'status': f'Progress: {unprocessed_emails}',
                    'progress_percentage': progress_percentage,
                    'email': email_data
                }))

            server.logout()
        threading.Thread(target=progress).start()




