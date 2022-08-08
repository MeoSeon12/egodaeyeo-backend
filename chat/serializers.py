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
    is_reviewed = serializers.SerializerMethodField()
    contract_status = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    inquirer = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.item.title

    def get_item(self, obj):
        return obj.item.id
    
    def get_item_status(self, obj):
        return obj.item.status
    
    def get_contract_status(self, obj):
        inquirer_id = obj.inquirer.id
        item_id = obj.item.id
        try:
            contract = ContractModel.objects.get(item=item_id, user=inquirer_id)
            return contract.status
        except ContractModel.DoesNotExist:
            return

    def get_is_reviewed(self, obj):
        reviews = obj.item.review_set.values()
        review_authors = [review['user_id'] for review in reviews]
        
        return obj.inquirer.id in review_authors

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
        fields = ['id', 'title', 'item', 'item_status', 'is_reviewed', 'contract_status', 'inquirer', 'author', 'chat_messages']