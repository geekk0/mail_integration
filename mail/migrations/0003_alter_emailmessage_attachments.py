# Generated by Django 5.0.7 on 2024-08-04 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0002_emailaccount_imap_server_emailaccount_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailmessage',
            name='attachments',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
