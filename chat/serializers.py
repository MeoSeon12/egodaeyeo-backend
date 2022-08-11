from rest_framework import serializers
from chat.models import (
    ChatRoom as ChatRoomModel,
    ChatMessage as ChatMessageModel
)
from contract.models import Contract as ContractModel
from django.db.models import Q
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
        fields = ['id', 'time', 'date', 'content', 'is_read',
                'room', 'user', 'application', 'contract_type']


class ChatSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    inquirer = serializers.SerializerMethodField()
    
    def get_author(self, obj):
        try:
            nickname = obj.author.nickname
            id = obj.author.id
            return {"id": id, "nickname": nickname}
        except:
            return {"nickname": "탈퇴유저"}

    def get_inquirer(self, obj):
        try:
            nickname = obj.inquirer.nickname
            id = obj.inquirer.id
            return {"id": id, "nickname": nickname}
        except:
            return {"nickname": "탈퇴유저"}

    class Meta:
        model = ChatRoomModel
        fields = ['id', 'inquirer', 'author']
        
        
class ChatRoomSerializer(serializers.ModelSerializer):
    chat_messages = ChatMessageSerializer(many=True, source='chatmessage_set')
    title = serializers.SerializerMethodField()
    item = serializers.SerializerMethodField()
    item_status = serializers.SerializerMethodField()
    is_reviewed = serializers.SerializerMethodField()
    contract_status = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    inquirer = serializers.SerializerMethodField()

    def get_title(self, obj):
        try:
            return obj.item.title
        except:
            return '삭제된 물품입니다'

    def get_item(self, obj):
        try:
            return obj.item.id
        except:
            return
    
    def get_item_status(self, obj):
        try:
            return obj.item.status
        except:
            return '삭제됨'
    
    def get_contract_status(self, obj):
        contract = obj.contract

        if contract:    
            return contract.status
        else:
            return
        

    def get_is_reviewed(self, obj):
        try:
            reviews = obj.item.review_set.values()
            review_authors = [review['user_id'] for review in reviews]
            
            return obj.inquirer.id in review_authors
        except:
            return

    def get_author(self, obj):
        try:
            nickname = obj.author.nickname
            id = obj.author.id
            return {"id": id, "nickname": nickname}
        except:
            return {"nickname": "탈퇴유저"}

    def get_inquirer(self, obj):
        try:
            nickname = obj.inquirer.nickname
            id = obj.inquirer.id
            return {"id": id, "nickname": nickname}
        except:
            return {"nickname": "탈퇴유저"}


    class Meta:
        model = ChatRoomModel
        fields = ['id', 'title', 'item', 'item_status', 'is_reviewed', 'contract_status', 'inquirer', 'author', 'chat_messages']