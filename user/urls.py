from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView # JWT refresh 토큰 발급 view 인증토큰을 재발급받기위한 또 다른 토큰 
from user.views import (
    KakaoLoginView,
    EgoTokenObtainPairView,
    UserView,
    MyPageView
)

urlpatterns = [
    path('', UserView.as_view()),
    path('api/token', EgoTokenObtainPairView.as_view(), name='access_token'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/kakao/', KakaoLoginView.as_view(), name='kakao_login'),
    path('mypages', MyPageView.as_view()),
    path('<int:id>/', UserView.as_view()),

]