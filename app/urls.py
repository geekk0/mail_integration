from django.contrib import admin
from django.urls import path, include

from mail.urls import urlpatterns as email_urls
from mail.views import main_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mail/', include(email_urls)),
    path('', main_page, name='main_page'),  # Main page view

]
