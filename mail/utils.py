# email/utils.py
import time

import imapclient
import email
from email.utils import parsedate_to_datetime
from email.header import decode_header
from bs4 import BeautifulSoup
from django.utils import timezone

from .models import EmailMessage


def decode_mime_words(s):
    decoded_words = []
    for word, encoding in decode_header(s):
        if isinstance(word, bytes):
            if encoding is None:
                decoded_words.append(word.decode('utf-8'))
            else:
                decoded_words.append(word.decode(encoding))
        else:
            decoded_words.append(word)
    return ''.join(decoded_words)


def decode_payload(payload):
    encodings = ['utf-8', 'latin-1', 'windows-1252']
    for encoding in encodings:
        try:
            return payload.decode(encoding)
        except (UnicodeDecodeError, AttributeError):
            continue
    return payload.decode('utf-8', errors='ignore')


def get_text_from_email(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" not in content_disposition:
                if content_type == "text/plain":
                    return decode_payload(part.get_payload(decode=True))
                elif content_type == "text/html":
                    html = decode_payload(part.get_payload(decode=True))
                    soup = BeautifulSoup(html, 'html.parser')
                    return soup.get_text()
    else:
        content_type = msg.get_content_type()
        if content_type == "text/plain":
            return decode_payload(msg.get_payload(decode=True))
        elif content_type == "text/html":
            html = decode_payload(msg.get_payload(decode=True))
            soup = BeautifulSoup(html, 'html.parser')
            return soup.get_text()
    return ""


def get_attachments_from_email(msg):
    attachments = []
    if msg.is_multipart():
        for part in msg.walk():
            content_disposition = str(part.get("Content-Disposition"))
            content_type = part.get_content_type()
            if "attachment" in content_disposition and not content_type.startswith("text/"):
                filename = part.get_filename()
                if filename and not filename.startswith("=?"):
                    attachments.append(filename)
    return attachments


def fetch_emails(email_account):
    start_time = time.time()
    server = imapclient.IMAPClient(email_account.imap_server, ssl=True)
    server.login(email_account.email, email_account.password)
    server.select_folder('INBOX', readonly=True)

    messages = server.search(['NOT', 'DELETED'])
    for msgid, data in server.fetch(messages, 'RFC822').items():
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

        EmailMessage.objects.create(
            subject=subject,
            sent_date=sent_date,
            received_date=received_date,
            description=description,
            attachments=attachments,  # Save attachments
            email_account=email_account
        )
    server.logout()
    end_time = time.time()
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"Time taken to process emails: {elapsed_time:.2f} seconds")  # Print the elapsed time


def get_emails_qty(email_account):
    start_time = time.time()  # Start the timer
    server = imapclient.IMAPClient(email_account.imap_server, ssl=True)
    server.login(email_account.email, email_account.password)
    server.select_folder('INBOX', readonly=True)

    messages = server.search(['NOT', 'DELETED'])
    total_emails = len(messages)  # Get the total number of emails

    server.logout()
    end_time = time.time()  # End the timer
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"Time taken to get email quantity: {elapsed_time:.2f} seconds")  # Print the elapsed time

    return total_emails  # Return the total number of emails