from django.db import models
from user.models import User as UserModel
from item.models import Item as ItemModel
from contract.models import Contract as ContractModel


CONTRACT_MESSAGE_TYPE = (
    ('신청', '신청'), 
    ('거절', '거절'), 
    ('수락', '수락'),
    ('종료', '종료')
)

class ChatRoom(models.Model):
    inquirer = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='inquirer')
    author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='author')
    item = models.ForeignKey(ItemModel, on_delete=models.SET_NULL, null=True)
    contract = models.ForeignKey(ContractModel, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "chatrooms"
        
    def __str__(self):
        return f"[채팅방] {self.author.nickname} / {self.inquirer.nickname}"


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    content = models.TextField("내용", max_length=1000, null=True)
    is_read = models.BooleanField("읽음/안읽음", default=False)
    created_at = models.DateTimeField("생성시간", auto_now_add=True)
    application = models.BooleanField("신청", default=False)
    contract_type = models.CharField("신청 유형", choices=CONTRACT_MESSAGE_TYPE, max_length=6, null=True)
    
    class Meta:
        db_table = "chat_messages"
        ordering = ["id"]