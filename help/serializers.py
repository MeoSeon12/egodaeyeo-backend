from rest_framework import serializers
from .models import Feedback as FeedbackModel

class FeedbackSerializer(serializers.ModelSerializer):
            
    class Meta:
        model = FeedbackModel
        fields = "__all__"