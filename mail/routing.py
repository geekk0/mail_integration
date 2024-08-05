from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/email/', consumers.EmailConsumer.as_asgi()),
]
