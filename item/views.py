from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Item as ItemModel
from user.models import User as UserModel


class DetailView(APIView):

    def get(self, request):
        items = ItemModel.objects.all().values()
        print(items)
        
        # user = UserModel.objects.get(id=request.user)
        # print(user)
        return Response(items)