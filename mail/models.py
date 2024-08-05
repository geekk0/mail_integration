from django.db import models


class EmailAccount(models.Model):
    name = models.CharField(max_length=255, default='email_account')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    imap_server = models.CharField(max_length=255, default='imap.server.domain')


class EmailMessage(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=1024)
    sent_date = models.DateTimeField()
    received_date = models.DateTimeField()
    description = models.TextField()
    attachments = models.JSONField(null=True, blank=True)  # Список прикреплённых файлов
    email_account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE)


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')
    email_message = models.ForeignKey(EmailMessage, related_name='attachment_files', on_delete=models.CASCADE)


