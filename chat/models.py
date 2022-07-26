from email.policy import default
from django.db import models
from user.models import User as UserModel
from item.models import Item as ItemModel


class ChatRoom(models.Model):
    sender = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='sender')
    receiver = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='receiver')
    item = models.ForeignKey(ItemModel, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "chatrooms"
        
    def __str__(self):
        return f"[채팅방] {self.item.title} / {self.receiver.nickname} / {self.sender.nickname}"


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    content = models.TextField("내용", max_length=1000)
    is_read = models.BooleanField("읽음/안읽음", default=False)
    created_at = models.DateTimeField("생성시간", auto_now_add=True)
    
    class Meta:
        db_table = "chat_messages"