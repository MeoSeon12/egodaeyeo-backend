from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from egodaeyeo.permissions import IsAddressOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from chat.models import (
    ChatRoom as ChatRoomModel,
    ChatMessage as ChatMessageModel
)
from item.models import Item as ItemModel
from django.db.models import Q

from chat.serializers import ChatSerializer, ChatRoomSerializer
class ChatView(APIView):
    permission_classes = [IsAddressOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        my_chat_rooms = ChatRoomModel.objects.filter(Q(inquirer=user.id) | Q(author=user.id))

        my_chat_rooms_serializer = ChatSerializer(my_chat_rooms, many=True)
        
        #채팅방 불러올시 is_read조회
        # for my_chat_room in my_chat_rooms:
        #     other_chats = ChatMessageModel.objects.filter(~Q(user=user.id) & Q(room=my_chat_room))
        #     print("상대 채팅",other_chats)
        #     for other_chat in other_chats:
        #         print("각채팅방의 채팅들의 is_read",other_chat.is_read)
        
        return Response(my_chat_rooms_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, item_id):
        inquirer = request.user
        item = ItemModel.objects.get(id=item_id)
        author = item.user
        
        try:
            #존재하는 채팅방이 있다면, 채팅방을 가져온다.
            chat_room = ChatRoomModel.objects.get(inquirer=inquirer.id, author=author.id, item=item.id)
            
            return Response({"msg": "채팅방 불러오기!"}, status=status.HTTP_200_OK)
        
        except ChatRoomModel.DoesNotExist:
            #존재하는 채팅방이 없다면, 새롭게 생성
            ChatRoomModel.objects.create(
                inquirer=inquirer, 
                author=author, 
                item=item
            )
            
            return Response({"msg": "채팅방 생성!"}, status=status.HTTP_200_OK)


class ChatRoomView(APIView):
    
    #각 채팅방 data 조회
    def get(self, request, room_id):
        user = request.user
        
        try:
            chat_room = ChatRoomModel.objects.get(id=room_id)
            chat_room_serializer = ChatRoomSerializer(chat_room)
            
            #채팅방 접속시, 채팅읽음 상태 만드는 로직
            other_chats = ChatMessageModel.objects.filter(~Q(user=user.id) & Q(room=chat_room))
            for other_chat in other_chats:
                other_chat.is_read = True
                other_chat.save()
                
        except ChatRoomModel.DoesNotExist:
            return Response({"msg": "채팅방이 더이상 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(chat_room_serializer.data, status=status.HTTP_200_OK)