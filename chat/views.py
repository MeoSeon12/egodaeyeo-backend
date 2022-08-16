from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from egodaeyeo.permissions import IsAddressOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from item.models import Item as ItemModel
from chat.serializers import ChatSerializer, ChatRoomSerializer
from chat.models import (
    ChatRoom as ChatRoomModel,
    ChatMessage as ChatMessageModel
)


# 채팅방 리스트 뷰
class ChatView(APIView):
    permission_classes = [IsAddressOrReadOnly]
    authentication_classes = [JWTAuthentication]

    # 참여하고있는 전체 채팅방 정보 불러오기
    def get(self, request):
        user = request.user
        my_chat_rooms = ChatRoomModel.objects.filter(
            Q(inquirer=user.id) | Q(author=user.id))
        my_chat_rooms_serializer = ChatSerializer(my_chat_rooms, many=True)
        sorted_rooms = sorted(
            my_chat_rooms_serializer.data, key=lambda x: (x['created_at'] is not None, x['created_at']), reverse=True)
        return Response(sorted_rooms, status=status.HTTP_200_OK)

    # 채팅방 생성
    def post(self, request, item_id):
        inquirer = request.user
        item = ItemModel.objects.get(id=item_id)
        author = item.user

        #채팅방 생성시 이미 존재하는 채팅방의 contrat status 체크
        chat_rooms = ChatRoomModel.objects.filter(
            inquirer=inquirer.id, author=author.id, item=item.id)
        
        not_available_status_list = ['대여 중', '검토 중', '없음']
        chat_room_contract_status_list = []
        
        #조회된 채팅방의 contract가 있을시 list에 status추가, 
        #없을시 list에 '없음' 추가 (contract가 아직 없는 채팅방도 존재하기 때문)
        for chat_room in chat_rooms:
            if chat_room.contract:
                chat_room_contract_status_list.append(chat_room.contract.status)
            else:
                chat_room_contract_status_list.append('없음')

        #not_available_status_list에 있는 status가 포함된 채팅방이 존재할 경우 채팅방을 조회
        #그렇지 않을 경우 채팅방을 새롭게 생성하는 로직
        for not_available_status in not_available_status_list:
            if not_available_status in chat_room_contract_status_list:
                chat_room = {
                'status': '채팅방 조회됨',
                'id': chat_room.id,
                'author': {
                    'id': chat_room.author.id,
                    'nickname': chat_room.author.nickname
                },
                'inquirer': {
                    'id': chat_room.inquirer.id,
                    'nickname': chat_room.inquirer.nickname
                }
                }
                return Response(chat_room, status=status.HTTP_200_OK)
            else:
                continue
            
        chat_room = ChatRoomModel.objects.create(
                inquirer=inquirer,
                author=author,
                item=item
            )
        chat_room = {
            'status': '채팅방 생성됨',
            'id': chat_room.id,
            'author': {
                'id': chat_room.author.id,
                'nickname': chat_room.author.nickname
            },
            'inquirer': {
                'id': chat_room.inquirer.id,
                'nickname': chat_room.inquirer.nickname
            }
        }
        return Response(chat_room, status=status.HTTP_200_OK)


# 개별 채팅방 뷰
class ChatRoomView(APIView):

    # 각 채팅방 data 조회
    def get(self, request, room_id):
        user = request.user

        try:
            chat_room = ChatRoomModel.objects.get(id=room_id)
        except ChatRoomModel.DoesNotExist:
            return Response({"msg": "채팅방이 더이상 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        chat_room_serializer = ChatRoomSerializer(chat_room)

        # 채팅방 접속시, 채팅읽음 상태 만드는 로직
        other_chats = ChatMessageModel.objects.filter(
            ~Q(user=user.id) & Q(room=chat_room))
        for other_chat in other_chats:
            other_chat.is_read = True
            other_chat.save()
        return Response(chat_room_serializer.data, status=status.HTTP_200_OK)

    # 실시간으로 바로 읽은 메시지 읽음 처리
    def put(self, request, room_id):
        unread_messages = ChatMessageModel.objects.filter(
            room_id=room_id, is_read=False)
        for unread_message in unread_messages:
            unread_message.is_read = True
            unread_message.save()

        return Response(status=status.HTTP_200_OK)


# 채팅 알림 뷰
class ChatAlertView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 읽지않은 메시지 데이터 보내기
    def get(self, request, user_id):
        # 참가중인 채팅방
        joined_chatrooms = ChatRoomModel.objects.filter(
            Q(author=user_id) | Q(inquirer=user_id))
        if not joined_chatrooms.exists():
            return Response({'msg': '참가중인 채팅방이 없습니다'}, status=status.HTTP_204_NO_CONTENT)
        else:
            unread_message_list = []
            for joined_chatroom in joined_chatrooms:
                # 읽지않은 채팅
                latest_unread_chat = joined_chatroom.chatmessage_set.filter(
                    is_read=False, application=False).exclude(user=user_id)
                if latest_unread_chat.exists():
                    latest_unread_chat = latest_unread_chat.last()
                    latest_unread_chat = {
                        'room_id': joined_chatroom.id,
                        'title': joined_chatroom.item.title,
                        'sender': latest_unread_chat.user.nickname,
                        'created_at': latest_unread_chat.created_at,
                        'status': None,
                    }
                    unread_message_list.append(latest_unread_chat)
                # 읽지않은 거래상태
                latest_unread_contract = joined_chatroom.chatmessage_set.filter(
                    is_read=False, application=True).exclude(user=user_id)
                if latest_unread_contract.exists():
                    latest_unread_contract = latest_unread_contract.last()
                    latest_unread_contract = {
                        'room_id': joined_chatroom.id,
                        'title': joined_chatroom.item.title,
                        'sender': latest_unread_contract.user.nickname,
                        'created_at': latest_unread_contract.created_at,
                        'contract_type': latest_unread_contract.contract_type,
                    }
                    unread_message_list.append(latest_unread_contract)
            unread_message_list.sort(key=lambda x: x['created_at'])
            return Response(unread_message_list, status=status.HTTP_200_OK)
