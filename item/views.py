from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from django.forms.models import model_to_dict

from item.models import Item as ItemModel
from item.models import Category as CategoryModel
from item.serializers import ItemSerializer, CategorySerializer, ItemDetailSerializer
from user.models import User as UserModel


class ItemView(APIView):
    
    def get(self, request):
        user = request.user
        items = ItemModel.objects.all().order_by('-created_at')
        categories = CategoryModel.objects.all()
        
        #유저가 주소를 설정 했을때 Query
        try:
            address_query = Q(item__user__address__contains=user.address)
            items = items.filter(address_query)
        except:
            pass
        # 카테고리명 Query Parameter로 가져오기
        category_name = request.GET.get('category', "")
        # 섹션 Query Parameter로 가져오기
        section = request.GET.get('section', "")
        
        if category_name is not "":
            category_query = Q(category__name=category_name)
            items = items.filter(category_query)
            
        if section is not "":
            section_query = Q(section=section)
            items = items.filter(section_query)
            
            
        item_serializer = ItemSerializer(items, many=True, context={"request": request})
        category_serializer = CategorySerializer(categories, many=True, context={"request": request})
        data = {
            'categories': category_serializer.data,
            'items': item_serializer.data,
        }
        
        
        return Response(data, status=status.HTTP_200_OK)
        

# 아이템 상세페이지 뷰
class DetailView(APIView):

    # 페이지 접속시
    def get(self, request, item_id):
        try:
            item = ItemModel.objects.get(id=item_id)
        except:
            return Response({'msg': '아이템 상세 페이지가 존재하지않습니다'}, status=status.HTTP_404_NOT_FOUND)

        item_detail_serializer = ItemDetailSerializer(item)
        return Response(item_detail_serializer.data, status=status.HTTP_200_OK)