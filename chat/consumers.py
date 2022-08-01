from datetime import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
import locale
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from chat.models import ChatMessage, ChatRoom
from user.models import User
from contract.models import Contract

locale.setlocale(locale.LC_TIME, 'ko_KR')


# 채팅 컨슈머
class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        #url에 room_id를 받아서 가져온다.
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_id

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


# 거래 컨슈머
class ContractConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'contract_{self.room_id}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()


    async def receive(self, text_data):
        received_data = json.loads(text_data)
        room_id = received_data['room_id']
        sender = received_data['sender']
        contract_type = received_data['contract_type']

        response = {
            'room_id': room_id,
            'sender': sender,
            'contract_type': contract_type,
            'date': datetime.now().strftime('%Y년 %m월 %d일 %A'),
            'time': datetime.now().strftime('%p %I:%M'),
        }

        await self.create_chat_message(room_id, sender, contract_type)

        # 현재그룹에 send
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def chat_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event,
        })

    async def chat_message(self, event):
        text = json.loads(event['text'])
        room_id = text['room_id']
        sender = text['sender']
        status = text['status']
        date = text['date']
        time = text['time']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'room_id': room_id,
            'sender': sender,
            'status': status,
            'date': date,
            'time': time,
        }))

    @database_sync_to_async
    def create_chat_message(self, room_id, sender_id, contract_type):
        room_obj = ChatRoom.objects.get(id=room_id)
        user_obj = User.objects.get(id=sender_id)
        ChatMessage.objects.create(room=room_obj, user=user_obj, contract_type=contract_type, application=True)


# 알람 컨슈머
class AlertConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        
        user_id = self.scope['url_route']['kwargs']['user_id']
        chat_alert = f'user_chat_alert_{user_id}'
        self.chat_alert = chat_alert
        
        await self.channel_layer.group_add(
            chat_alert,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    # 웹소켓에 데이터 들어옴
    async def websocket_receive(self, event):
        
        received_data = json.loads(event['text'])
        receiver_id = received_data.get('receiver')

        # 데이터 가공
        sender = await self.get_user_object(received_data['sender'])  # 작성자 닉네임
        title = await self.get_title_object(received_data['room_id'])
        
        # 수신자에게 보낼 데이터
        response = {
            'sender': sender,
            'title': title,
            'room_id': received_data['room_id'],
            'status': received_data['status'],
        }
        
        # 상대방 온메시지에 보냄
        other_user_chat_alert = f'user_chat_alert_{receiver_id}'

        await self.channel_layer.group_send(
            other_user_chat_alert,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

    # 웹소켓 연결종료
    async def websocket_disconnect(self, event):
        print('disconnect', event)

    async def chat_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text'],
        })
    
    # 데이터 가공 (발신자 닉네임 조회)
    @database_sync_to_async
    def get_user_object(self, sender_id):
        qs = User.objects.get(id=sender_id)
        return qs.nickname

    # 데이터 가공 (채팅창 제목 조회)
    @database_sync_to_async
    def get_title_object(self, room_id):
        qs = ChatRoom.objects.get(id=room_id)
        return qs.item.title
