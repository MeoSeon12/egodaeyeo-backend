from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView # JWT refresh 토큰 발급 view 인증토큰을 재발급받기위한 또 다른 토큰 
from user.views import (
    TokenRefreshView,
    EgoTokenObtainPairView,
    UserView,
    KakaoLogin
)

from . import views

urlpatterns = [
    path('', UserView.as_view()),
    path('api/token', EgoTokenObtainPairView.as_view(), name='access_token'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('kakao/login/finish/', KakaoLogin.as_view(), name='kakao_login_todjango'),
]