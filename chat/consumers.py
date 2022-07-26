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

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):

#         self.room_group_name = 'test'
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
        
#         self.accept()
        
        
#     def receive(self, text_data):

#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
        
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
        
        
#     def chat_message(self, event):

#         message = event['message']
#         now_time = datetime.now().strftime('%p %I:%M')
        
#         self.send(text_data = json.dumps({
#             'type': 'chat',
#             'message': message,
#             'time': now_time
#         }))

class ChatConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        # print('connected', event)
        user = self.scope['user']
        chat_room = f'user_chatroom_{user.id}'
        # print(chat_room, user)
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        # print('receive', event)
        received_data = json.loads(event['text'])
        print('received_data',received_data)
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
        now_time = datetime.now().strftime('%p %I:%M')
        response = {
            'message': content,
            'sender': self_user.id,
            'room_id': room_id,
            'time': now_time
        }

        await self.channel_layer.group_send(
            other_user_chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

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