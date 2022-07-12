from django.db import models
from user.models import User as UserModel
from item.models import Item as ItemModel

class Deal(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    status = models.PositiveIntegerField("상태", choices=(('거래 종료', '거래 종료'), ('거래 가능','거래 가능'), ('예약 중', '예약 중'), ('거래 중', '거래 중')))
    start_date = models.DateTimeField("시작일")
    end_date = models.DateTimeField("반납일")

    class Meta:
        db_table = "deals"
        
    def __str__(self):
        return f"[거래] {self.user.nickname} / {self.post.title}"


class DealHistory(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    deal = models.ForeignKey(Deal, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "deal_histories"
        
    def __str__(self):
        return f": [거래내역] 유저: {self.user.nickname} / 상대: {self.deal.user.nickname} / {self.deal}"