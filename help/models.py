from django.db import models
from user.models import User as UserModel

class Feedback(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=70)
    content = models.TextField("피드백 내용", max_length=512)

    class Meta:
        db_table = "feedbacks"
        
    def __str__(self):
        return f"[피드백] {self.title} / {self.user}"
