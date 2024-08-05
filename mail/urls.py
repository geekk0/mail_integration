from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EmailAccountViewSet, EmailMessageViewSet, email_list, register_mail_account, fetch_emails_view
router = DefaultRouter()
router.register(r'accounts', EmailAccountViewSet)
router.register(r'messages', EmailMessageViewSet)

urlpatterns = [
    path('email_list/', email_list, name='email_list'),  # Email list view
    path('register/', register_mail_account, name='register_mail_account'),
    path('fetch_emails/', fetch_emails_view, name='fetch_emails'),

]
