import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "global_chat"
        print("WebSocket connect() called")

        # Add the user to the group (for broadcasting messages)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the connection
        await self.accept()
        print("WebSocket connection accepted")

    async def disconnect(self, close_code):
        print(f"WebSocket disconnected with code {close_code}")

        # Remove the user from the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(f"Received message: {text_data}")

        data = json.loads(text_data)
        message = data['message']

        # Send the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        print(f"Sending message to WebSocket: {event['message']}")

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
