import json
import time
import threading
from typing import Any

from channels.generic.websocket import WebsocketConsumer

from .models import EmailMessage, EmailAccount
from .utils import fetch_emails


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
            fetch_emails(email_account)
            emails = EmailMessage.objects.all().order_by('-id')
            total_emails = len(emails)
            for i, email in enumerate(emails):
                time.sleep(0.1)  # Simulate progress
                progress = int((i + 1) / total_emails * 100)
                email_data = {
                    'id': email.id,
                    'subject': email.subject,
                    'sent_date': email.sent_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'received_date': email.received_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'description': email.description,
                    'attachments': email.attachments
                }
                self.send(text_data=json.dumps({
                    'status': f'Progress: {progress}%',
                    'email': email_data
                }))
                print(f"Progress: {progress}%")  # Debugging line
            self.send(text_data=json.dumps({
                'status': 'Completed'
            }))
        threading.Thread(target=progress).start()

    def receive(self, text_data: Any) -> None:
        data = json.loads(text_data)
        print(f"Received data: {data}")  # Debugging line

    def disconnect(self, close_code):
        print("WebSocket disconnected")  # Debugging line




# class EmailConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#         self.send(text_data=json.dumps({
#             'status': 'Чтение сообщений'
#         }))
#         print("WebSocket connected")  # Debugging line
#         self.send_progress_updates()
#
#     def send_progress_updates(self):
#         def progress():
#             for i in range(1, 101):
#                 time.sleep(0.1)  # Simulate progress
#                 self.send(text_data=json.dumps({
#                     'status': f'Progress: {i}%'
#                 }))
#                 print(f"Progress: {i}%")  # Debugging line
#         threading.Thread(target=progress).start()
#
#     def receive(self, text_data: Any) -> None:
#         data = json.loads(text_data)
#         print(f"Received data: {data}")  # Debugging line
#
#     def disconnect(self, close_code):
#         print("WebSocket disconnected")  # Debugging line

