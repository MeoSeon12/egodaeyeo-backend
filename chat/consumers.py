from datetime import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import locale
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from chat.models import ChatMessage, ChatRoom
from user.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication

locale.setlocale(locale.LC_TIME, 'ko_KR')

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        #url에 room_id를 받아서 가져온다.
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_id
        print("그룹네임", self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("disconnect", self.room_group_name)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        
        received_data = json.loads(text_data)
        print("리시브",received_data)
        message = received_data.get('message')
        sender_id = received_data.get('sender')
        receiver_id = received_data.get('receiver')
        room_id = received_data.get('room_id')
        item_id = received_data.get('item_id')

        if not message:
            print('Error:: empty message')
            return False

        sender = await self.get_user_object(sender_id)
        receiver = await self.get_user_object(receiver_id)
        room_obj = await self.get_chatroom(room_id)
        
        if not sender:
            print('Error:: sent by user is incorrect')
        if not receiver:
            print('Error:: send to user is incorrect')
        if not room_obj:
            print('Error:: Header id is incorrect')

        await self.create_chat_message(room_obj, sender, message)
        
        self_user = sender

        now_date = datetime.now().strftime('%Y년 %m월 %d일 %A')
        now_time = datetime.now().strftime('%p %I:%M')

        response = {
            'message': message,
            'sender': self_user.id,
            'room_id': room_id,
            'date': now_date,
            'time': now_time,
            'item_id': item_id,
        }
        
        # 현재그룹에 send
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

    async def chat_message(self, event):
        text = json.loads(event['text'])
        message = text['message']
        now_time = text['time']
        now_date = text['date']
        room_id = text['room_id']
        item_id = text['item_id']
        sender = text['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'time': now_time,
            'date': now_date,
            'room_id': room_id,
            'item_id': item_id,
            'sender': sender
        }))

   
    @database_sync_to_async
    def get_user_object(self, user_id):
        qs = User.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def get_chatroom(self, room_id):
        qs = ChatRoom.objects.filter(id=room_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def create_chat_message(self, room, sender, content):
        ChatMessage.objects.create(room=room, user=sender, content=content)