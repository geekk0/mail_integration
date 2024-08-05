import json
import threading
import imaplib
import email
import os

from channels.generic.websocket import WebsocketConsumer
from email.utils import parsedate_to_datetime
from django.utils import timezone
from django.core.files.base import ContentFile
from email.header import decode_header

from .models import EmailMessage, EmailAccount, Attachment
from .utils import decode_mime_words, get_text_from_email, get_attachments_from_email


def decode_filename(filename):
    decoded_bytes, charset = decode_header(filename)[0]
    if isinstance(decoded_bytes, bytes):
        return decoded_bytes.decode(charset or 'utf-8')
    return decoded_bytes


class EmailConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'status': 'Поиск сообщений...'
        }))
        print("WebSocket connected")  # Debugging line
        account_id = self.scope['url_route']['kwargs']['account_id']
        self.send_progress_updates(account_id)

    def send_progress_updates(self, account_id):
        def progress():
            email_account = EmailAccount.objects.get(id=account_id)
            print()
            last_email = EmailMessage.objects.filter(email_account=email_account).order_by('-id').first()

            last_received_date = last_email.received_date if last_email else None

            self.send(text_data=json.dumps({
                'status': 'Получение сообщений...',
            }))

            server = imaplib.IMAP4_SSL(email_account.imap_server)
            server.login(email_account.email, email_account.password)
            server.select('INBOX')

            search_criteria = '(NOT DELETED)'
            if last_received_date:
                search_criteria = f'(SINCE {last_received_date.strftime("%d-%b-%Y")} NOT DELETED)'

            result, data = server.search(None, search_criteria)
            messages = data[0].split()
            total_emails = len(messages)

            for i, msgid in enumerate(messages):
                result, data = server.fetch(msgid, '(RFC822)')
                msg = email.message_from_bytes(data[0][1])
                subject = decode_mime_words(msg['subject'])

                sent_date = parsedate_to_datetime(msg['date'])
                received_date = parsedate_to_datetime(msg['date'])

                if timezone.is_naive(sent_date):
                    sent_date = timezone.make_aware(sent_date)
                if timezone.is_naive(received_date):
                    received_date = timezone.make_aware(received_date)

                description = get_text_from_email(msg)
                attachments_data = get_attachments_from_email(msg)

                email_message = EmailMessage.objects.create(
                    subject=subject,
                    sent_date=sent_date,
                    received_date=received_date,
                    description=description,
                    attachments=[decode_filename(filename) for filename, _ in attachments_data],
                    email_account=email_account
                )

                for filename, file_data in attachments_data:
                    filename = decode_filename(filename)
                    if not os.path.splitext(filename)[1]:  # Skip if no file extension
                        continue
                    attachment = Attachment(
                        email_message=email_message
                    )
                    attachment.file.save(filename, ContentFile(file_data))
                    attachment.save()

                unprocessed_emails = total_emails - (i + 1)
                progress_percentage = int(((i + 1) / total_emails) * 100)
                email_data = {
                    'id': msgid.decode('utf-8'),
                    'subject': subject,
                    'sent_date': sent_date.strftime('%d-%m-%Y %H:%M:%S'),
                    'received_date': received_date.strftime('%d-%m-%Y %H:%M:%S'),
                    'description': description,
                    'attachments': [decode_filename(filename) for filename, _ in attachments_data]
                }
                self.send(text_data=json.dumps({
                    'status': f'Progress: {unprocessed_emails}',
                    'progress_percentage': progress_percentage,
                    'email': email_data
                }))

            server.logout()
        threading.Thread(target=progress).start()
