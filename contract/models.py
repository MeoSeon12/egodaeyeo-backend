from django.db import models
from user.models import User as UserModel
from item.models import Item as ItemModel

class Contract(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    status = models.PositiveIntegerField("상태", choices=(('대여 종료', '대여 종료'), ('대여 가능','대여 가능'), ('예약 중', '예약 중'), ('대여 중', '대여 중')))
    start_date = models.DateTimeField("시작일")
    end_date = models.DateTimeField("반납일")

    class Meta:
        db_table = "contracts"
        
    def __str__(self):
        return f"[대여] {self.user.nickname} / {self.post.title}"


class ContractHistory(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "contract_histories"
        
    def __str__(self):
        return f": [대여내역] 유저: {self.user.nickname} / 상대: {self.contract.user.nickname} / {self.contract}"