import json

from channels.generic.websocket import AsyncWebsocketConsumer


# class Consumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         print("CONNECTED")
#         await self.accept()

#     async def send_message(self, event):
#         # if not self.scope["user"].is_anonymous:
#         message = event["message"]
#         print("MESSAGE: ", message)
#         await self.send(text_data=json.dumps(message))
    
#     async def disconnect(self, close_code):
#         print("DISCONNECTED")
#         pass

class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)

        await self.send(text_data=json.dumps({
            'message': message
        }))
    
    def send(self, event):
        print("EVENT TRIGERED")
        # Receive message from room group
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))
        
        import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
        }))
