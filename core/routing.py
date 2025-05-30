from django.urls import re_path
from .consumers import LocationConsumer

websocket_urlpatterns = [
    re_path(r'ws/location/(?P<driver_id>\w+)/$', LocationConsumer.as_asgi()),
]
