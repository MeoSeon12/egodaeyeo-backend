from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path('contracts/<int:item_id>', consumers.RentalConsumer.as_asgi()),
]
