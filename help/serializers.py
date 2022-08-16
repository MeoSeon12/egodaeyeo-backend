from rest_framework import serializers
from .models import (
    Feedback as FeedbackModel,
    Report as ReportModel
)

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackModel
        fields = ["id", "user", "title", "content"]
        
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportModel
        fields = ["id", "user", "item", "category", "content"]