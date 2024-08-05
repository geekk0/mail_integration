from django.contrib import admin
from .models import EmailAccount


@admin.register(EmailAccount)
class EmailAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'imap_server')
    search_fields = ('name', 'email')


