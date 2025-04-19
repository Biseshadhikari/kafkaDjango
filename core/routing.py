from . import consumer
from django.urls import path

websocket_urlpatterns = [
    path('ws/chat/', consumer.ChatConsumer.as_asgi()),
]