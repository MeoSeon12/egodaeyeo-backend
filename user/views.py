from django import http
from django.views import View
import jwt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from user.serializers import UserSerializer
from user.models import User as UserModel

import requests
from django.shortcuts import redirect
from django.conf import settings
# from dj_rest_auth.registration.views import SocialLoginView
# from allauth.socialaccount.providers.kakao import views as kakao_view
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount

from user.jwt_claim_serializer import EgoTokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
import local_settings

SECRET_KEY = local_settings.SECRET['secret']
# BASE_URL = 'http://localhost:8000/'
# KAKAO_CALLBACK_URI = BASE_URL + 'users/kakao/callback/'

class UserView(APIView):
    permission_classes = [permissions.AllowAny]
    
    #TODO 회원정보 조회
    # def get(self, request):
    #     user = request.user
    #     user_serializer = UserSerializer(user, context={"request": request})
        
    #     return Response(user_serializer.data, status=status.HTTP_200_OK)
    
    #DONE 회원가입
    def post(self, request):
        user_serializer = UserSerializer(data=request.data, context={"request": request})
        
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #TODO 회원정보 수정
    def put(self, request, id):
        user = UserModel.objects.get(id=id)
        user_serializer = UserSerializer(user, data=request.data, partial=True, context={"request": request})
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #TODO 회원탈퇴
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "회원 탈퇴 완료!"})


#JWT 로그인
class EgoTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    #serializer_class 변수에 커스터마이징 된 시리얼라이저를 넣어 준다!
    serializer_class = EgoTokenObtainPairSerializer


class KakaoLoginView(APIView): #카카오 로그인

    def get(self, request):
        access_token = request.headers["Authorization"]
        headers      = ({'Authorization' : f"Bearer {access_token}"})
        url          = "https://kapi.kakao.com/v2/user/me" # Authorization(프론트에서 받은 토큰)을 이용해서 회원의 정보를 확인하기 위한 카카오 API 주소
        response     = requests.request("POST", url, headers=headers) # API를 요청하여 회원의 정보를 response에 저장
        user         = response.json()
        email        = user['kakao_account']['email']
        nickname     = user['properties']['nickname']
        print(f"토큰: {access_token}")
        print(f"리스폰스: {response}")
        print(f"유저: {user}")
        print(f"이메일: {email}")

        try:
            # 기존에 가입된 유저와 쿼리해서 존재하면서, socialaccount에도 존재하면 로그인
            user = UserModel.objects.get(email=email)
            social_user = SocialAccount.objects.filter(user=user).first()
            #로그인
            if social_user:
                refresh = RefreshToken.for_user(user)
                # encoded_jwt = jwt.encode({'user_id': user.id}, SECRET_KEY, algorithm='HS256') # jwt토큰 발급
                return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "msg" : "로그인 성공"}, status=status.HTTP_200_OK)
            
            # 동일한 이메일의 유저가 있지만, social계정이 아닐때 
            if social_user is None:
                return Response({"error": "email exists but not social user"}, status=status.HTTP_400_BAD_REQUEST)
            
            # 소셜계정이 카카오가 아닌 다른 소셜계정으로 가입했을때
            if social_user.provider != "kakao":
                return Response({"error": "no matching social type"}, status=status.HTTP_400_BAD_REQUEST)
    
        except UserModel.DoesNotExist:
            # 기존에 가입된 유저가 없으면 새로 가입
            new_user = UserModel.objects.create(
                nickname=nickname,
                email=email,
            )
            #소셜account에도 생성
            SocialAccount.objects.create(
                user_id=new_user.id,
            )
        
            return Response({"msg": "회원가입에 성공 했습니다."}, status=status.HTTP_200_OK)