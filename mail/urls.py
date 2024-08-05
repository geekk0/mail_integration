from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EmailAccountViewSet, EmailMessageViewSet, email_list, register_mail_account, accounts_list
router = DefaultRouter()
router.register(r'accounts', EmailAccountViewSet)
router.register(r'messages', EmailMessageViewSet)

urlpatterns = [
    path('accounts_list', accounts_list, name='accounts_list'),  # Email list view
    path('email_list/<int:account_id>', email_list, name='email_list'),  # Email list view
    path('register/', register_mail_account, name='register_mail_account'),
]
