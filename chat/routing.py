from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path('chats/<int:room_id>', consumers.ChatConsumer.as_asgi()),
    path('chats/contracts/<int:room_id>', consumers.ContractConsumer.as_asgi()),
]