from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import EmailAccount, EmailMessage
from .serializers import EmailAccountSerializer, EmailMessageSerializer
from django.http import JsonResponse


from .utils import fetch_emails
from .forms import EmailAccountForm


class EmailAccountViewSet(viewsets.ModelViewSet):
    queryset = EmailAccount.objects.all()
    serializer_class = EmailAccountSerializer


class EmailMessageViewSet(viewsets.ModelViewSet):
    queryset = EmailMessage.objects.all()
    serializer_class = EmailMessageSerializer


def main_page(request):
    return render(request, 'main_page.html')


# def email_list(request):
#     return render(request, 'email_list.html')


def register_mail_account(request):
    if request.method == 'POST':
        form = EmailAccountForm(request.POST)
        if form.is_valid():
            email_account = form.save()
            fetch_emails(email_account)  # Fetch emails after saving the account
            return redirect('email_list')  # Use the named URL pattern
    else:
        form = EmailAccountForm()
    return render(request, 'register_mail_account.html', {'form': form})


def email_list(request):
    return render(request, 'email_list.html')
    # email_account = EmailAccount.objects.first()  # Get the first email account for demo purposes
    # fetch_emails(email_account)
    # emails = EmailMessage.objects.all().order_by('-id')
    # return render(request, 'email_list.html', {'emails': emails})


def fetch_emails_view(request):
    email_account = EmailAccount.objects.first()  # Get the first email account for demo purposes
    fetch_emails(email_account)
    emails = EmailMessage.objects.all().order_by('-id')
    email_data = list(emails.values('id', 'subject', 'sent_date', 'received_date', 'description', 'attachments'))
    return JsonResponse({'emails': email_data})

