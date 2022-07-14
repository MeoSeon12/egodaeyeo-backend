from rest_framework import serializers
from user.models import User as UserModel

VALID_EMAIL_LIST = ["naver.com", "gmail.com", "daum.net"]


class UserSerializer(serializers.ModelSerializer):
    
    def validate(self, data):
        if data.get("email", "").split('@')[-1] not in VALID_EMAIL_LIST:
            raise serializers.ValidationError(
                detail={"error": "naver, gmail, daum 이메일 주소만 사용 가능합니다."}
            )
        return data
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()
        
        return user
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)
            
        instance.save()
        
        return instance
            
    class Meta:
        model = UserModel
        fields = ["id", "nickname", "email", "password", "address"]
        
        extra_kwargs = {
            'password' : {'write_only': True}
        }

class KakaoUserSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        user = UserModel(**validated_data)
        user.save()
        
        return user
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)
            
        instance.save()
        
        return instance
            
    class Meta:
        model = UserModel
        fields = ["id", "nickname", "email", "password"]
        
        # extra_kwargs = {
        #     'password' : {'write_only': True}
        # }
