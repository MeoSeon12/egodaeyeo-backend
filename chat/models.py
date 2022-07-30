from email.policy import default
from django.db import models
from user.models import User as UserModel
from item.models import Item as ItemModel


class ChatRoom(models.Model):
    inquirer = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='inquirer')
    author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='author')
    item = models.ForeignKey(ItemModel, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "chatrooms"
        
    def __str__(self):
        return f"[채팅방] {self.item.title} / {self.author.nickname} / {self.inquirer.nickname}"


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    content = models.TextField("내용", max_length=1000, null=True)
    is_read = models.BooleanField("읽음/안읽음", default=False)
    created_at = models.DateTimeField("생성시간", auto_now_add=True)
    application = models.BooleanField("신청", default=False)
    status = models.CharField('상태', choices=(('신청 전', '신청 전'), ('검토 중', '검토 중'), ('수락', '수락'), ('거래 종료', '거래 종료')), max_length=6, null=True)
    
    class Meta:
        db_table = "chat_messages"