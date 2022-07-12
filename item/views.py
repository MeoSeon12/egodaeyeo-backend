from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q

from item.models import Item as ItemModel
from item.models import Category as CategoryModel
from item.serializers import ItemSerializer, CategorySerializer


class ItemView(APIView):
    
    def get(self, request):
        user = request.user
        items = ItemModel.objects.all()
        categories = CategoryModel.objects.all()
        
        item_serializer = ItemSerializer(items, many=True, context={"request": request})
        category_serializer = CategorySerializer(categories, many=True, context={"request": request})
        data = {
            'categories': category_serializer.data,
            'items': item_serializer.data,
        }
        
        
        return Response(data, status=status.HTTP_200_OK)
