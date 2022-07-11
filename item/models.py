from django.db import models
from user.models import User as UserModel


class Category(models.Model):
    name = models.CharField(max_length=30)
    
    class Meta:
        db_table = "categories"
        
    def __str__(self):
        return f"[카테고리] {self.name}"


class Item(models.Model):
    section = models.CharField("섹션", max_length=10, choices=(('빌려요', 'borrow'), ('빌려드려요', 'lend')))
    title = models.CharField("제목", max_length=30)
    content = models.TextField("내용", max_length=300)
    images = models.FileField("이미지", null=True, upload_to='develop/')
    time_unit = models.CharField("시간 단위", max_length=2, choices=(('시간', 'hour'), ('일', 'day'), ('월', 'month')), null=True)
    price = models.PositiveIntegerField("가격", null=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now = True)
    status = models.PositiveIntegerField("상태", choices=(('0', '거래 종료'), ('1','거래 가능'), ('2', '예약 중'), ('3', '거래 중')))
    
    class Meta:
        db_table = "items"
        
    def __str__(self):
        return f"[아이템] {self.user.nickname} / {self.title} / {self.section}"


class Bookmark(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        db_table = "bookmarks"
        
    def __str__(self):
        return f"[북마크] {self.user.nickname} / {self.item} 북마크"
        

class Inquiry(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        db_table = "inquiries"
        
    def __str__(self):
        return f"[문의] {self.user.nickname} / {self.item}"


class Review(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    content = models.TextField("내용", max_length=300)
    star = models.DecimalField("별점", decimal_places=1, max_digits=2)
    created_at = models.DateTimeField("작성일", auto_now_add=True)

    class Meta:
        db_table = "reviews"
        
    def __str__(self):
        return f"[리뷰] {self.user.nickname} / {self.item}"