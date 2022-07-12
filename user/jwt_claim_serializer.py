from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 

# TokenObtainPairSerializer를 상속하여 클레임 설정
# access 토큰에 관한 정보를 커스텀할수있음.
class FarmTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user): 
		# 생성된 토큰 가져오기
        token = super().get_token(user)

        # 사용자 지정 클레임
        token['nickname'] = user.nickname
        #로그인 하는 id를 넣어 커스텀 가능
        
        # +a 로 넣어서 커스텀 가능

        return token