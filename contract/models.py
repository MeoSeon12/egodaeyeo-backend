from django.db import models
from user.models import User as UserModel
from item.models import Item as ItemModel, RENTAL_STATUS

class Contract(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    status = models.CharField("상태", max_length=10, choices=RENTAL_STATUS)
    start_date = models.DateTimeField("시작일")
    end_date = models.DateTimeField("반납일")

    class Meta:
        db_table = "contracts"
        
    def __str__(self):
        return f"[대여] {self.id} / {self.user.nickname} / {self.item.title}"


class Review(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    contract = models.OneToOneField(Contract, on_delete=models.SET_NULL, null=True)
    content = models.TextField("내용", max_length=300)
    star = models.DecimalField("별점", decimal_places=1, max_digits=2)
    created_at = models.DateTimeField("작성일", auto_now_add=True)

    class Meta:
        db_table = "reviews"
        
    def __str__(self):
        return f"[리뷰] {self.id} / {self.user.nickname} / {self.item}"