from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from user.serializers import UserSerializer, MyBookmarkSerializer
from user.models import User as UserModel
from item.models import (
    Item as ItemModel,
    Bookmark as BookmarkModel,
)
from item.serializers import MyPageItemSerializer
from contract.models import Contract as ContractModel
from contract.serializers import MyPageContractSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount
from user.jwt_claim_serializer import EgoTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from django.contrib.auth.hashers import check_password

class UserView(APIView):
    permission_classes = [permissions.AllowAny]
    
    #회원정보 조회
    def get(self, request, id):
        user = UserModel.objects.get(id=id)
        user_image = user.image.url
        user_nickname = user.nickname
        user_score = user.score
        user_address = user.address
        
        data = {
            "image": user_image,
            "nickname": user_nickname,
            "score": user_score,
            "address": user_address
        }

        return Response(data, status=status.HTTP_200_OK)
    
    #회원가입
    def post(self, request):
        user_serializer = UserSerializer(data=request.data, context={"request": request})
        
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #회원정보 수정
    def put(self, request):
        user_id = request.user.id
        user = UserModel.objects.get(id=user_id)
        data = request.data
            
        try:
            image = request.data['image']
            password = request.data['password']
            current_pw = request.data['current_password']
            social_user = SocialAccount.objects.filter(user=user).first()

            
            if social_user and password != "":
                return Response({"social_error": "소셜회원은 비밀번호를 수정 하실 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            if current_pw:
                #현재 비밀번호와 입력한 현재비밀번호가 일치하지 않을시 return
                if check_password(current_pw, user.password) == False:
                    return Response({"msg": "입력하신 현재 비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            #image 수정안할시 예외처리
            if image == 'undefined':
                data = data.copy()
                data.pop('image')
                
            #password Blank일시 예외처리
            if password == "":
                data = data.copy()
                data.pop('password')
                
            user_serializer = UserSerializer(user, data=data, partial=True, context={"request": request})    
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
        except:
            user_serializer = UserSerializer(user, data=data, partial=True, context={"request": request})    
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #회원탈퇴
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"msg": "회원 탈퇴 되었습니다. 그동안 서비스를 이용해주셔서 감사합니다."})


#JWT 로그인
class EgoTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = EgoTokenObtainPairSerializer

class KakaoLoginView(APIView):

    def post(self, request):
        email = request.data.get("email")
        nickname = request.data.get("nickname")

        try:
            # 기존에 가입된 유저와 쿼리해서 존재하면서, socialaccount에도 존재하면 로그인
            user = UserModel.objects.get(email=email)
            social_user = SocialAccount.objects.filter(user=user).first()
            print(social_user.provider)
            
            
            # 로그인
            if social_user:
                # 소셜계정이 카카오가 아닌 다른 소셜계정으로 가입한 유저일때(구글, 네이버)
                if social_user.provider != "kakao":
                    return Response({"error": "카카오로 가입한 유저가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)
                
                refresh = RefreshToken.for_user(user)
                return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "msg" : "로그인 성공"}, status=status.HTTP_200_OK)
            
            # 동일한 이메일의 유저가 있지만, social계정이 아닐때 
            if social_user is None:
                return Response({"error": "이메일이 존재하지만, 소셜유저가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)
            
        except UserModel.DoesNotExist:
            # 기존에 가입된 유저가 없으면 새로 가입
            new_user = UserModel.objects.create(
                nickname=nickname,
                email=email,
            )
            #소셜account에도 생성
            SocialAccount.objects.create(
                user_id=new_user.id,
                uid=new_user.email,
                provider="kakao",
            )

            refresh = RefreshToken.for_user(new_user)
                
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "msg" : "회원가입 성공"}, status=status.HTTP_201_CREATED)


class MyPageView(APIView):

    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]

    # 마이페이지 거래내역 / 찜 리스트 조회
    def get(self, request):
        user_id = request.user.id
        tab = request.GET.get('tab', '')
        user = UserModel.objects.get(id=user_id)

        if tab == "ongoing":
            my_ongoing_contracts = ContractModel.objects.filter(Q(status='대여 중') & Q(user=user.id)).order_by('-id')
            ongoing_contract_serializer = MyPageContractSerializer(my_ongoing_contracts, many=True)
            return Response(ongoing_contract_serializer.data, status=status.HTTP_200_OK)

        if tab == "closed":
            my_closed_contracts = ContractModel.objects.filter(Q(status='대여 종료') & Q(user=user.id)).order_by('-id')
            closed_contract_serializer = MyPageContractSerializer(my_closed_contracts, many=True)
            return Response(closed_contract_serializer.data, status=status.HTTP_200_OK)

        if tab == "bookmarks":
            my_bookmarks = BookmarkModel.objects.filter(user=user.id).order_by('-id')
            my_bookmarks_serializer = MyBookmarkSerializer(my_bookmarks, many=True)
            return Response(my_bookmarks_serializer.data, status=status.HTTP_200_OK)

        if tab == "myitems":
            my_items = ItemModel.objects.filter(user=user.id).order_by('-id')
            my_items_serialiizer = MyPageItemSerializer(my_items, many=True)
            data_list = []
            for data in my_items_serialiizer.data:
                data_dict = {}
                data_dict['item'] = data
                data_list.append(data_dict)
            return Response(data_list, status=status.HTTP_200_OK)
        
        return Response({"msg": "해당내역 없음"}, status=status.HTTP_204_NO_CONTENT)


        
        

    

        
