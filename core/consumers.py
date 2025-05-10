from channels.generic.websocket import AsyncWebsocketConsumer
import json

class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join location group
        await self.channel_layer.group_add(
            "locations",  # Group name
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave location group
        await self.channel_layer.group_discard(
            "locations",
            self.channel_name
        )

    async def send_location(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['data']))
