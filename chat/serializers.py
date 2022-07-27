from rest_framework import serializers
from chat.models import (
    ChatRoom as ChatRoomModel,
    ChatMessage as ChatMessageModel
)
import locale
locale.setlocale(locale.LC_TIME, 'ko_KR')
# now_time = datetime.now().strftime('%p %I:%M')


class ChatMessageSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    def get_time(self, obj):
        return obj.created_at.strftime('%p %I:%M')
    
    def get_date(self, obj):
        return obj.created_at.strftime('%Y년 %m월 %d일 %A')
    class Meta:
        model = ChatMessageModel
        fields = ['id', 'time', 'date', 'content', 'is_read', 'room', 'user']

class ChatSerializer(serializers.ModelSerializer):
    receiver = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()
    
    def get_receiver(self, obj):
        nickname = obj.receiver.nickname
        id = obj.receiver.id
        return {"id": id, "nickname": nickname}

    def get_sender(self, obj):
        nickname = obj.sender.nickname
        id = obj.sender.id
        return {"id": id, "nickname": nickname}

    class Meta:
        model = ChatRoomModel
        fields = ['id', 'sender', 'receiver']
        
class ChatRoomSerializer(serializers.ModelSerializer):
    chat_messages = ChatMessageSerializer(many=True, source='chatmessage_set')
    title = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.item.title
    
    def get_receiver(self, obj):
        nickname = obj.receiver.nickname
        id = obj.receiver.id
        return {"id": id, "nickname": nickname}

    def get_sender(self, obj):
        nickname = obj.sender.nickname
        id = obj.sender.id
        return {"id": id, "nickname": nickname}

    class Meta:
        model = ChatRoomModel
        fields = ['id', 'title', 'sender', 'receiver', 'chat_messages']