from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email')
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
# 커스텀 유저 모델
class User(AbstractBaseUser):
    email = models.EmailField("이메일", max_length=50, unique=True)
    nickname = models.CharField("닉네임", max_length=15, unique=True)
    password = models.CharField("비밀번호", max_length=256)
    address = models.TextField("주소", max_length=256)
    image = models.ImageField("이미지", default="../static/profile.jpg", upload_to='profile/')
    score = models.PositiveIntegerField("유저 점수", blank=True, null=True, validators=[MaxValueValidator(100), MinValueValidator(1)])
    join_date = models.DateTimeField("가입일", auto_now_add=True)
    
    # 활성화 여부
    is_active = models.BooleanField("계정 활성화 여부", default=True)

    # 관리자 권한 여부
    is_admin = models.BooleanField("관리자 권한", default=False)

    class Meta:
        db_table = "users"

    # 실제 로그인에 사용되는 아이디
    USERNAME_FIELD = 'email'

    # 어드민 계정을 만들 때 입력받을 정보 ex) email
    # 사용하지 않더라도 선언이 되어야함
    # USERNAME_FIELD와 비밀번호는 기본적으로 포함되어있음
    REQUIRED_FIELDS = []

    # custom user 생성 시 필요
    objects = UserManager()

    # 어드민 페이지에서 데이터를 제목을 어떻게 붙여줄 것인지 지정
    def __str__(self):
        return f"[유저] pk: {self.id} / 이메일: {self.email} / 닉네임: {self.nickname}"

    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    # 일반적으로 선언만 해두고 건들지않는다
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
