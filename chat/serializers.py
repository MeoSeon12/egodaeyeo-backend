from rest_framework import serializers
from chat.models import (
    ChatRoom as ChatRoomModel,
    ChatMessage as ChatMessageModel
)
import locale
locale.setlocale(locale.LC_TIME, 'ko_KR')

class ChatMessageSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    def get_time(self, obj):
        return obj.created_at.strftime('%p %I:%M')
    
    def get_date(self, obj):
        return obj.created_at.strftime('%Y년 %m월 %d일 %A')
    class Meta:
        model = ChatMessageModel
        fields = ['id', 'time', 'date', 'content', 'is_read', 'room', 'user', 'application']

class ChatSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    inquirer = serializers.SerializerMethodField()
    
    def get_author(self, obj):
        nickname = obj.author.nickname
        id = obj.author.id
        return {"id": id, "nickname": nickname}

    def get_inquirer(self, obj):
        nickname = obj.inquirer.nickname
        id = obj.inquirer.id
        return {"id": id, "nickname": nickname}

    class Meta:
        model = ChatRoomModel
        fields = ['id', 'inquirer', 'author']
        
class ChatRoomSerializer(serializers.ModelSerializer):
    chat_messages = ChatMessageSerializer(many=True, source='chatmessage_set')
    title = serializers.SerializerMethodField()
    item = serializers.SerializerMethodField()
    item_status = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    inquirer = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.item.title

    def get_item(self, obj):
        return obj.item.id
    
    def get_item_status(self, obj):
        return obj.item.status
    
    def get_author(self, obj):
        nickname = obj.author.nickname
        id = obj.author.id
        return {"id": id, "nickname": nickname}

    def get_inquirer(self, obj):
        nickname = obj.inquirer.nickname
        id = obj.inquirer.id
        return {"id": id, "nickname": nickname}

    class Meta:
        model = ChatRoomModel
        fields = ['id', 'title', 'item', 'item_status', 'inquirer', 'author', 'chat_messages']