from dataclasses import fields
from rest_framework import serializers
from item.serializers import MyPageItemSerializer
from contract.models import Contract as ContractModel

from django.utils import timezone
from datetime import datetime, timedelta

class MyPageContractSerializer(serializers.ModelSerializer):
    item = MyPageItemSerializer()
    time_remaining = serializers.SerializerMethodField()

    # 대여 종료일까지 시간
    def get_time_remaining(self, obj):
        time_remaining = obj.end_date - timezone.now()
        return time_remaining

    class Meta:
        model = ContractModel
        fields = ["id", "start_date", "end_date", "time_remaining", "item"]
