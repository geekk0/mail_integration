from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import EmailAccount, EmailMessage
from .serializers import EmailAccountSerializer, EmailMessageSerializer

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
            return redirect('accounts_list')  # Use the named URL pattern
    else:
        form = EmailAccountForm()
    return render(request, 'register_mail_account.html', {'form': form})


def email_list(request, account_id):
    context = {'account_id': account_id}
    return render(request, 'email_list.html', context)


def main(request):
    return render(request, 'main_page.html')


def accounts_list(request):
    accounts = EmailAccount.objects.all()
    context = {'accounts': accounts}
    return render(request, 'accounts_list.html', context)



