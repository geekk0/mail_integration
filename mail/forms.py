# mail/forms.py
from django import forms
from .models import EmailAccount

class EmailAccountForm(forms.ModelForm):
    class Meta:
        model = EmailAccount
        fields = ['name', 'email', 'password', 'imap_server']
