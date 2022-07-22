from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from item.pagination import PaginationHandlerMixin
from item.serializers import ItemSerializer, CategorySerializer, DetailSerializer, DetailReviewSerializer, ContractSerializer
from egodaeyeo.permissions import IsAddressOrReadOnly
from user.models import User as UserModel
from item.models import (
    Item as ItemModel,
    Category as CategoryModel,
    Bookmark as BookmarkModel,
    ItemImage as ItemImageModel,
    Review as ReviewModel
)


class ItemPagination(PageNumberPagination): # 👈 PageNumberPagination 상속
    page_size = 12
        
class ItemListView(APIView, PaginationHandlerMixin):
    permission_classes = [IsAddressOrReadOnly]
    authentication_classes = [JWTAuthentication]
    pagination_class = ItemPagination
    
    def get(self, request):
        user = request.user
        items = ItemModel.objects.filter(status="대여 가능").order_by('-created_at')
        categories = CategoryModel.objects.all()
        
        #유저가 주소를 설정 했을때 Query
        try:
            #시군구 까지 split해서 DB에서 쿼리 
            city = user.address.split(' ')[0]
            ward_county = user.address.split(' ')[1]
            address_query = Q(user__address__contains=city) & Q(user__address__contains=ward_county)
            items = items.filter(address_query)
        except:
            pass
        
        # 검색 입력값 Query Parameter로 가져오기
        search_value = request.GET.get('search', "")
        # 카테고리명 Query Parameter로 가져오기
        category_name = request.GET.get('category', "")
        # 섹션 Query Parameter로 가져오기
        section = request.GET.get('section', "")

        if search_value != "":
            search_query = Q(title__icontains=search_value)
            items = items.filter(search_query)
            
            
        if category_name != "":
            category_query = Q(category__name=category_name)
            items = items.filter(category_query)
            
        if section != "":
            section_query = Q(section=section)
            items = items.filter(section_query)


        page = self.paginate_queryset(items)
        
        if page is not None:
            item_serializer = self.get_paginated_response(ItemSerializer(page, many=True, context={"request": request}).data)
        else:
            item_serializer = ItemSerializer(items, many=True, context={"request": request})
        
        category_serializer = CategorySerializer(categories, many=True, context={"request": request})
        
        data = {
            'categories': category_serializer.data,
            'items': item_serializer.data,
        }
        
        return Response(data, status=status.HTTP_200_OK)

# 아이템 상세페이지 뷰
class DetailView(APIView):
    permission_classes = [IsAddressOrReadOnly]
    authentication_classes = [JWTAuthentication]

    # 페이지 접속시
    def get(self, request, item_id):
        
        try:
            item = ItemModel.objects.get(id=item_id)
        # 아이템 정보가 없을 시
        except:
            return Response({'error_msg': '아이템 정보가 없습니다'}, status=status.HTTP_404_NOT_FOUND)

        login_id = request.GET.get('user_id', '')
        detail_serializer = DetailSerializer(item, context={'login_id': login_id})

        return Response(detail_serializer.data, status=status.HTTP_200_OK)

    # 찜하기 버튼 클릭시
    def post(self, request, item_id):
        user_id = request.user.id
        user = UserModel.objects.get(id=user_id)
        item = ItemModel.objects.get(id=item_id)

        try:
            # 북마크 모델 존재 여부 체크
            bookmark_model_check = BookmarkModel.objects.get(user=user_id, item=item_id)
            # 북마크 모델 있을시 삭제
            bookmark_model_check.delete()
            # 로그인 유저 북마크 여부
            is_bookmark = False
            # 북마크 갯수 카운터
            bookmark_length = BookmarkModel.objects.filter(item=item_id).count()

            return Response({'is_bookmark': is_bookmark, 'bookmark_length': bookmark_length}, status=status.HTTP_200_OK)


        # 북마크 모델 없을시 저장
        except:
            new_bookmark = {
                'user': user,
                'item': item
            }
            BookmarkModel.objects.create(**new_bookmark)
            # 로그인 유저 북마크 여부
            is_bookmark = True
            # 북마크 갯수 갱신
            bookmark_length = BookmarkModel.objects.filter(item=item_id).count()
            return Response({'is_bookmark': is_bookmark, 'bookmark_length': bookmark_length}, status=status.HTTP_201_CREATED)


# 아이템 등록 페이지 뷰
class ItemPostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 업로드 페이지 뷰 (카테고리 데이터)
    def get(self, request):
        categories = CategoryModel.objects.all().values('name')

        return Response(categories, status=status.HTTP_200_OK)

    # 아이템 등록하기 기능
    def post(self, request):

        price = request.data['price']
        time_unit = request.data['time']

        # 가격 입력하지 않았을 경우
        if price == '':
            price = None

        # 시간 단위 입력하지 않았을 경우
        if time_unit == '-- 기간 --':
            time_unit = None

        # 아이템 모델에 저장
        item = ItemModel.objects.create(
            section = request.data['section'],
            title = request.data['title'],
            content = request.data['content'],
            time_unit = time_unit,
            price = price,
            user = UserModel.objects.get(id=request.user.id),
            category = CategoryModel.objects.get(name=request.data['category']),
            status = '대여 가능'
        )

        # 아이템 이미지 모델에 저장
        try:    # 이미지가 있을 경우
            images = request.data.pop('image')

            for image in images:

                ItemImageModel.objects.create(
                    item = ItemModel.objects.get(id=item.id),
                    image = image
                )

        except: # 이미지가 없을 경우
            ItemImageModel.objects.create(
                item = ItemModel.objects.get(id=item.id)
            )

        return Response(item.id, status=status.HTTP_200_OK)


# 물품 수정 페이지
class ItemUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 페이지 로드 데이터 얻기
    def get(self, request, item_id):

        # 데이터 가져오기
        images_data = ItemImageModel.objects.filter(item=item_id).values('image')
        item_data = ItemModel.objects.get(id=item_id)
        category_data = CategoryModel.objects.all().values('name')

        # 이미지 데이터 다듬기
        image_list = []
        for image_data in images_data:
            image_list.append(image_data['image'])

        # 아이템 데이터 다듬기
        item_data = {
            'section': item_data.section,
            'category': item_data.category.name,
            'time_unit': item_data.time_unit,
            'price': item_data.price,
            'title': item_data.title,
            'content': item_data.content,
        }

        # 카테고리 데이터 다듬기
        category_list = []
        for category in category_data:
            category_list.append(category['name'])

        return Response({
                'image_list': image_list,
                'item_data': item_data,
                'category_list': category_list,
            }, status=status.HTTP_200_OK)
        
        
class ReviewView(APIView):
    permission_classes = [IsAddressOrReadOnly]
    authentication_classes = [JWTAuthentication]

    # 리뷰작성 버튼 클릭시
    def post(self, request, item_id):
        user_id = request.user.id
        content = request.data.get("content")
        rating = request.data.get("rating")
        item = ItemModel.objects.get(id=item_id)

        review_data = {
            "user": user_id,
            "item": item.id,
            "content": content,
            "star": rating
        }

        review_serializer = DetailReviewSerializer(data=review_data, context={"request": request})
    
        if review_serializer.is_valid():
            review_serializer.save()
            return Response(review_serializer.data, status=status.HTTP_200_OK)
    
        return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractView(APIView):
    permission_classes = [IsAddressOrReadOnly]
    authentication_classes = [JWTAuthentication]

    # 대여 신청 버튼 클릭시
    def post(self, request, item_id):
        user_id = request.user.id
        start_date = request.data.get("rentalStartTime")
        end_date = request.data.get("rentalEndTime")
        item = ItemModel.objects.get(id=item_id)

        contract_data = {
            "user": user_id,
            "item": item.id,
            "start_date": start_date,
            "end_date": end_date
        }

        contract_serializer = ContractSerializer(data=contract_data, context={"request": request})
    
        if contract_serializer.is_valid():
            contract_serializer.save()
            return Response(contract_serializer.data, status=status.HTTP_200_OK)
    
        return Response(contract_serializer.errors, status=status.HTTP_400_BAD_REQUEST)