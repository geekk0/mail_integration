from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/email/<int:account_id>/', consumers.EmailConsumer.as_asgi()),
]

# websocket_urlpatterns = [
#     re_path(r'ws/email/(?P<account_id>\d+)/$', EmailConsumer.as_asgi()),
# ]