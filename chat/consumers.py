from datetime import datetime
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import locale
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from chat.models import ChatMessage, ChatRoom
from user.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication

locale.setlocale(locale.LC_TIME, 'ko_KR')

class ChatConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        
        #url에 user_id를 받아서 가져온다.
        user_id = self.scope['url_route']['kwargs']['user_id']
        chat_room = f'user_chatroom_{user_id}'
        self.chat_room = chat_room
        
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        
        received_data = json.loads(event['text'])
        content = received_data.get('message')
        sender_id = received_data.get('sender')
        receiver_id = received_data.get('receiver')
        room_id = received_data.get('room_id')

        if not content:
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

        await self.create_chat_message(room_obj, sender, content)
        
        other_user_chat_room = f'user_chatroom_{receiver_id}'
        self_user = sender

        now_date = datetime.now().strftime('%Y년 %m월 %d일 %A')
        now_time = datetime.now().strftime('%p %I:%M')

        response = {
            'message': content,
            'sender': self_user.id,
            'room_id': room_id,
            'date': now_date,
            'time': now_time,
        }
        
        print('아덜채팅', other_user_chat_room)
        #상대방 채팅창에 send
        await self.channel_layer.group_send(
            other_user_chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

        print('셀프채팅',self.chat_room)
        #내 채팅창에 send
        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

    async def websocket_disconnect(self, event):
        print('disconnect', event)


    async def chat_message(self, event):
        # print('chat_message', event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text'],
        })
    
    
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