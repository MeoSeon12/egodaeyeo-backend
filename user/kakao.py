# from django.conf import settings
# from accounts.models import User
# from allauth.socialaccount.models import SocialAccount
# from django.conf import settings
# from dj_rest_auth.registration.views import SocialLoginView
# from allauth.socialaccount.providers.google import views as google_view
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from django.http import JsonResponse
# import requests
# from rest_framework import status
# from json.decoder import JSONDecodeError
# from egodaeyeo.settings import SECRET_KEY
# import local_settings

# SECRET_KEY = local_settings.SECRET['secret']
# views.py
# class KakaoLoginView(View): #카카오 로그인

#     def get(self, request):
#         access_token = request.headers["Authorization"]
#         headers      =({'Authorization' : f"Bearer {access_token}"})
#         url          = "https://kapi.kakao.com/v1/user/me" # Authorization(프론트에서 받은 토큰)을 이용해서 회원의 정보를 확인하기 위한 카카오 API 주소
#         response     = requests.request("POST", url, headers=headers) # API를 요청하여 회원의 정보를 response에 저장
#         user         = response.json()

#         if User.objects.filter(social_login_id = user['id']).exists(): #기존에 소셜로그인을 했었는지 확인
#             user_info          = User.objects.get(social_login_id=user['id'])
#             encoded_jwt        = jwt.encode({'id': user_info.id}, wef_key, algorithm='HS256') # jwt토큰 발행

#             return JsonResponse({ #jwt토큰, 이름, 타입 프론트엔드에 전달
#                 'access_token' : encoded_jwt.decode('UTF-8'),
#                 'user_name'    : user_info.name,
#                 'user_pk'      : user_info.id
#             }, status = 200)            
#         else:
#             new_user_info = User(
#                 social_login_id = user['id'],
#                 name            = user['properties']['nickname'],
#                 social          = SocialPlatform.objects.get(platform ="kakao"),
#                 email           = user['properties'].get('email', None)
#             )
#             new_user_info.save()
#             encoded_jwt         = jwt.encode({'id': new_user_info.id}, SECRET_KEY, algorithm='HS256') # jwt토큰 발행
#             none_member_type    = 1
#             return JsonResponse({
#                 'access_token' : encoded_jwt.decode('UTF-8'),
#                 'user_name'    : new_user_info.name,
#                 'user_pk'      : new_user_info.id,
#                 }, status = 200)


# models.py          
# class SocialPlatform(models.Model):
#     platform = models.CharField(max_length=20, default=0)

#     class Meta:
#         db_table = "social_platform"

# class User(models.Model):
#     ~중략~
#     social          = models.ForeignKey(SocialPlatform, on_delete=models.CASCADE, max_length=20, blank=True, default=1)
#     social_login_id = models.CharField(max_length=50, blank=True)
#     ~중략~

# urls.py
# from .views import UserView, LoginView, GoogleLoginView, KakaoLoginView
# urlpatterns = [
#     path('/login/google',GoogleLoginView.as_view()),
#     path('/login/kakao',KakaoLoginView.as_view())
# ]
# # encoded_jwt = jwt.encode({'user_id': user.id}, SECRET_KEY, algorithm='HS256') # jwt토큰 발급

# # #카카오 로그인(카카오 자체에 로그인)
# # def kakao_login(request):
# #     rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
# #     return redirect(
# #         f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
# #     )

# # #카카오에서 인증되면 콜백
# # def kakao_callback(request):
# #     rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
# #     code = request.GET.get("code")
# #     print(f"코드! : {code}")
# #     redirect_uri = KAKAO_CALLBACK_URI
# #     """
# #     Access Token Request
# #     """
# #     token_request = requests.get(
# #         f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}")
# #     token_request_json = token_request.json()
# #     print(f"토큰 리퀘스트 제슨! : {token_request_json}")
# #     error = token_request_json.get("error")
    
# #     if error is not None:
# #         raise JSONDecodeError(error)
# #     access_token = token_request_json.get("access_token")
# #     """
# #     Email Request
# #     """
# #     profile_request = requests.get(
# #         "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
# #     profile_json = profile_request.json()
# #     error = profile_json.get("error")
# #     if error is not None:
# #         raise JSONDecodeError(error)
# #     kakao_account = profile_json.get('kakao_account')
# #     """
# #     kakao_account에서 이메일, 닉네임 정보 가져옴
# #     """
# #     email = kakao_account.get('email')
# #     nickname = kakao_account['profile']['nickname']
# #     """
# #     Signup or Signin Request
# #     """
# #     try:
# #         # 기존에 가입된 유저와 쿼리해서 존재하면서, socialaccount에도 존재하면 로그인
# #         user = UserModel.objects.get(email=email)
# #         social_user = SocialAccount.objects.filter(user=user).first()
# #         #로그인
# #         if social_user:
# #             encoded_jwt = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256') # jwt토큰 발급
# #             # return redirect("http://127.0.0.1:5500/", {"encoded_jwt": encoded_jwt})
# #             return JsonResponse({
# #                     "access_token" : encoded_jwt,
# #                     "msg" : "로그인 성공"
# #                     }, status=status.HTTP_200_OK)
            
# #         # 동일한 이메일의 유저가 있지만, social계정이 아닐때 
# #         if social_user is None:
# #             return JsonResponse({"err_msg": "email exists but not social user"}, status=status.HTTP_400_BAD_REQUEST)
        
# #         # 소셜계정이 카카오가 아닌 다른 소셜계정으로 가입했을때
# #         if social_user.provider != "kakao":
# #             return JsonResponse({"err_msg": "no matching social type"}, status=status.HTTP_400_BAD_REQUEST)
    
# #     except UserModel.DoesNotExist:
# #         # 기존에 가입된 유저가 없으면 새로 가입
# #         new_user = UserModel.objects.create(
# #             nickname=nickname,
# #             email=email,
# #         )
# #         #소셜account에도 생성
# #         SocialAccount.objects.create(
# #             user_id=new_user.id,
# #         )
        
# #         return JsonResponse({"msg": "회원가입에 성공 했습니다."}, status=status.HTTP_200_OK)