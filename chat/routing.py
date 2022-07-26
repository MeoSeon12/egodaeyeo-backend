from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/socket-server/<int:id>', consumers.ChatConsumer.as_asgi()),
    path('chats/<int:user_id>', consumers.ChatConsumer.as_asgi()),
]