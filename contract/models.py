from django.db import models
from user.models import User as UserModel
from item.models import Item as ItemModel

class Contract(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    status = models.CharField("상태", max_length=10, choices=(('대여 가능', '대여 가능'), ('검토 중', '검토 중'), ('대여 중', '대여 중'), ('대여 종료', '대여 종료')))
    start_date = models.DateTimeField("시작일")
    end_date = models.DateTimeField("반납일")

    class Meta:
        db_table = "contracts"
        
    def __str__(self):
        return f"[대여] {self.id} / {self.user.nickname} / {self.item.title}"


class ContractHistory(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "contract_histories"
        
    def __str__(self):
        return f": [대여내역] 유저: {self.id} / {self.user.nickname} / 상대: {self.contract.user.nickname} / {self.contract}"