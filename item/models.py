from django.db import models
from user.models import User as UserModel
from django.core.validators import MaxValueValidator


RENTAL_STATUS = (
    ('대여 가능','대여 가능'),
    ('검토 중', '검토 중'),
    ('대여 중', '대여 중'),
    ('대여 종료', '대여 종료'),
)

class Category(models.Model):
    name = models.CharField(max_length=30)
    
    class Meta:
        db_table = "categories"
        
    def __str__(self):
        return f"[카테고리] {self.id} / {self.name}"


class Item(models.Model):
    section = models.CharField("섹션", max_length=10, choices=(('빌려요', '빌려요'), ('빌려드려요', '빌려드려요')))
    title = models.CharField("제목", max_length=23)
    content = models.TextField("내용", max_length=1000)
    time_unit = models.CharField("시간 단위", max_length=5, choices=(('시간', '시간'), ('일', '일'), ('월', '월')), null=True, blank=True)
    price = models.PositiveIntegerField(
        "가격", blank=True, null=True,
        validators=[
            MaxValueValidator(10000000)
        ])
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now = True)
    status = models.CharField("상태", blank=True, max_length=10, choices=RENTAL_STATUS)
    
    class Meta:
        db_table = "items"
        
    def __str__(self):
        return f"[아이템] {self.id} / {self.user.nickname} / {self.title} / {self.section}"


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item/')

    class Meta:
        db_table = "item_images"

    def __str__(self):
        return f"[아이템 사진] {self.id} / {self.image} / {self.item.title}"


class Bookmark(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        db_table = "bookmarks"
        
    def __str__(self):
        return f"[북마크] {self.id} / {self.user.nickname} / {self.item} 북마크"