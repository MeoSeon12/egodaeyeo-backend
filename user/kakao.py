from django.conf import settings
from accounts.models import User
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
import requests
from rest_framework import status
from json.decoder import JSONDecodeError

views.py
class KakaoLoginView(View): #카카오 로그인

    def get(self, request):
        access_token = request.headers["Authorization"]
        headers      =({'Authorization' : f"Bearer {access_token}"})
        url          = "https://kapi.kakao.com/v1/user/me" # Authorization(프론트에서 받은 토큰)을 이용해서 회원의 정보를 확인하기 위한 카카오 API 주소
        response     = requests.request("POST", url, headers=headers) # API를 요청하여 회원의 정보를 response에 저장
        user         = response.json()

        if User.objects.filter(social_login_id = user['id']).exists(): #기존에 소셜로그인을 했었는지 확인
            user_info          = User.objects.get(social_login_id=user['id'])
            encoded_jwt        = jwt.encode({'id': user_info.id}, wef_key, algorithm='HS256') # jwt토큰 발행

            return JsonResponse({ #jwt토큰, 이름, 타입 프론트엔드에 전달
                'access_token' : encoded_jwt.decode('UTF-8'),
                'user_name'    : user_info.name,
                'user_pk'      : user_info.id
            }, status = 200)            
        else:
            new_user_info = User(
                social_login_id = user['id'],
                name            = user['properties']['nickname'],
                social          = SocialPlatform.objects.get(platform ="kakao"),
                email           = user['properties'].get('email', None)
            )
            new_user_info.save()
            encoded_jwt         = jwt.encode({'id': new_user_info.id}, wef_key, algorithm='HS256') # jwt토큰 발행
            none_member_type    = 1
            return JsonResponse({
                'access_token' : encoded_jwt.decode('UTF-8'),
                'user_name'    : new_user_info.name,
                'user_pk'      : new_user_info.id,
                }, status = 200)


models.py          
class SocialPlatform(models.Model):
    platform = models.CharField(max_length=20, default=0)

    class Meta:
        db_table = "social_platform"

class User(models.Model):
    ~중략~
    social          = models.ForeignKey(SocialPlatform, on_delete=models.CASCADE, max_length=20, blank=True, default=1)
    social_login_id = models.CharField(max_length=50, blank=True)
    ~중략~

urls.py
from .views import UserView, LoginView, GoogleLoginView, KakaoLoginView
urlpatterns = [
    path('/login/google',GoogleLoginView.as_view()),
    path('/login/kakao',KakaoLoginView.as_view())
]