from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from rest_framework import status


class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code=status_code
        super().__init__(detail=detail, code=code)
        
        
class IsAddressOrReadOnly(BasePermission):
    """
    admin 사용자, 혹은 회원가입하고 주소입력한 사용자는 모든 request 가능,
    비로그인 사용자는 조회만 가능
    """

    SAFE_METHODS = ('GET', )
    message = '서비스를 이용하기 위해 주소를 입력 해주세요.'

    def has_permission(self, request, view):
        user = request.user
        
        if request.method in self.SAFE_METHODS:
            return True
        if not user.is_authenticated:
            response = {
                'detail': "로그인한 사용자만 이용하실 수 있는 서비스입니다."
            }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)
        
        if (user.is_authenticated and user.is_admin) or user.address:
            return True

        return False