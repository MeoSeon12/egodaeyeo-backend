from rest_framework import serializers
from item.serializers import MyPageItemSerializer
from contract.models import Contract as ContractModel
from chat.models import ChatRoom as ChatRoomModel
from datetime import datetime

class ContractSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        contract = ContractModel(**validated_data)
        contract.save()
        
        query_data = {
            "inquirer": contract.user,
            "author": contract.item.user,
            "item": contract.item,
        }
        
        chat_rooms = ChatRoomModel.objects.filter(**query_data)
        for chat_room in chat_rooms:
            if not chat_room.contract:
                chat_room.contract = contract
                chat_room.save()
        
        return contract

    class Meta:
        model = ContractModel
        fields = ['id', 'user', 'item', 'start_date', 'end_date', 'status']

class MyPageContractSerializer(serializers.ModelSerializer):
    item = MyPageItemSerializer()
    time_remaining = serializers.SerializerMethodField()
    rental_date = serializers.SerializerMethodField()
    room_id = serializers.SerializerMethodField()
    is_reviewed = serializers.SerializerMethodField()

    # 대여 종료일까지 시간
    def get_time_remaining(self, obj):
        time_string = str(obj.end_date - datetime.now())

        if 'day' in time_string and 'days' not in time_string:
            time_string = time_string.replace('day', 'days')

        elif 'days' not in time_string:
            time_string = '0 days, ' + time_string

        time_string = time_string.split(",")

        days = time_string[0]
        days = days[:-5]

        times = time_string[1]
        times = times[1:]
        times = times.split(":")
        hours = times[0]
        minutes = times[1]

        time_remaining = f"{days}일 {hours}시간 {minutes}분"

        return time_remaining

    #대여 기간
    def get_rental_date(self, obj):
        start_date = str(obj.start_date)
        start_date = start_date.split(' ')[0]
        end_date = str(obj.end_date)
        end_date = end_date.split(' ')[0]
        return f"{start_date} ~ {end_date}"
    
    #방id
    def get_room_id(self, obj):
        try:
            chat_room_id = obj.item.chatroom_set.filter(inquirer=obj.user).last().id
            return chat_room_id
        except AttributeError:
            return 
        
    #리뷰 작성 여부
    def get_is_reviewed(self, obj):
        try:
            reviews = obj.item.review_set.values()
            review_authors = [review['user_id'] for review in reviews]
            
            return obj.user.id in review_authors
        except AttributeError:
            return

    class Meta:
        model = ContractModel
        fields = ["id", "rental_date", "time_remaining", "item", "room_id", "is_reviewed"]
