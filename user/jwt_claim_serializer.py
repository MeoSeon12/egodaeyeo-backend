from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 

# TokenObtainPairSerializer를 상속하여 클레임 설정
# access 토큰에 관한 정보를 커스텀할수있음.
class EgoTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user): 
		# 생성된 토큰 가져오기
        token = super().get_token(user)

        # 사용자 지정 클레임
        token['nickname'] = user.nickname
        token['image'] = user.image
        
        # +a 로 넣어서 커스텀 가능

        return token