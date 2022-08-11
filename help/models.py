from unicodedata import category
from django.db import models
from user.models import User as UserModel
from item.models import Item as ItemModel

REPORT_CATEGORY = (
    ('판매 금지 물품이에요', '판매 금지 물품이에요'),
    ('중고거래 게시글이 아니에요', '중고거래 게시글이 아니에요'),
    ('전문 판매업자 같아요', '전문 판매업자 같아요'),
    ('사기 글이에요', '사기 글이에요'),
    ('기타', '기타')
)

class Feedback(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=70)
    content = models.TextField("피드백 내용", max_length=512)

    class Meta:
        db_table = "feedbacks"
        
    def __str__(self):
        return f"[피드백] {self.title} / {self.user}"
    
class Report(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(ItemModel, on_delete=models.SET_NULL, null=True)
    category = models.CharField("신고 카테고리", max_length=20, choices=REPORT_CATEGORY)
    content = models.TextField("신고 내용", max_length=512, blank=True)
    class Meta:
        db_table = "reports"
        
    def __str__(self):
        return f"[신고] {self.content} / {self.category}"