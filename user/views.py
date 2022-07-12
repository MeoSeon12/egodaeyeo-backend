from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from user.serializers import UserSerializer
from user.models import User as UserModel

from user.jwt_claim_serializer import FarmTokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication

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
class FarmTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    #serializer_class 변수에 커스터마이징 된 시리얼라이저를 넣어 준다!
    serializer_class = FarmTokenObtainPairSerializer

