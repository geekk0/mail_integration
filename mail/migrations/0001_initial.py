# Generated by Django 5.0.7 on 2024-08-04 06:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EmailMessage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=255)),
                ('sent_date', models.DateTimeField()),
                ('received_date', models.DateTimeField()),
                ('description', models.TextField()),
                ('attachments', models.JSONField()),
                ('email_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mail.emailaccount')),
            ],
        ),
    ]
