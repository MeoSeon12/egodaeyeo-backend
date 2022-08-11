from rest_framework import serializers
from chat.models import (
    ChatRoom as ChatRoomModel,
    ChatMessage as ChatMessageModel
)
import locale

# locale.setlocale(locale.LC_TIME, 'kor')
# locale.setlocale(locale.LC_TIME, 'ko_KR.UTF-8')
locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')

class ChatMessageSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    def get_time(self, obj):
        am_pm = obj.created_at.strftime('%p')            
        created_time = obj.created_at.strftime('%I:%M')            
        if am_pm == 'AM':
            created_time = f"오전 {created_time}"
        else:
            created_time = f"오후 {created_time}"
        return created_time
    
    def get_date(self, obj):
        return obj.created_at.strftime('%Y년 %m월 %d일 %A')

    class Meta:
        model = ChatMessageModel
        fields = ['id', 'time', 'date', 'content', 'is_read',
                'room', 'user', 'application', 'contract_type']


class ChatSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    inquirer = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    
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

    def get_created_at(self, obj):
        try:
            latest_chat_messages = ChatMessageModel.objects.filter(room=obj).order_by('-id').first()
            return latest_chat_messages.created_at
        except:
            return 

    class Meta:
        model = ChatRoomModel
        fields = ['id', 'inquirer', 'author', 'created_at']
        
        
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