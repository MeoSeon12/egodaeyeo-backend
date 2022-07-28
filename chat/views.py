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
    
    def get(self, request, room_id):
        chat_room = ChatRoomModel.objects.get(id=room_id)
        chat_room_serializer = ChatRoomSerializer(chat_room)

        return Response(chat_room_serializer.data, status=status.HTTP_200_OK)