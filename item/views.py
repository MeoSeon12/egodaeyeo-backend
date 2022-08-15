from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from item.pagination import PaginationHandlerMixin
from item.serializers import (
    ItemSerializer, CategorySerializer, DetailSerializer, ItemImageSerializer,
    DetailReviewSerializer, ContractSerializer, ItemPostSerializer
)
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
        user_id = request.GET.get('user', "")
        user_address = ""
        items = ItemModel.objects.filter(status="대여 가능").order_by('-created_at')
        categories = CategoryModel.objects.all()
        
        #유저가 주소를 설정 했을때 Query
        try:
            user = UserModel.objects.get(id=user_id)
            address_split = user.address.split()[:2]
            user_address = ' '.join(address_split)
            #시군구 까지 split해서 DB에서 쿼리 
            city = user.address.split()[0]
            ward_county = user.address.split()[1]
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
            'user_address': user_address,
        }
        
        return Response(data, status=status.HTTP_200_OK)
    

# 물품 상세페이지 뷰
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

    # 게시글 삭제
    def delete(self, request, item_id):

        item_obj = ItemModel.objects.get(id=item_id)
        item_obj.delete()

        return Response(status=status.HTTP_200_OK)


# 물품 등록 페이지 뷰
class ItemPostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 업로드 페이지 뷰 (카테고리 데이터)
    def get(self, request):
        categories = CategoryModel.objects.all().values('name')

        return Response(categories, status=status.HTTP_200_OK)

    # 물품 등록하기 기능
    def post(self, request):

        price = request.data['price']
        time_unit = request.data['time']

        # 가격 입력하지 않았을 경우
        if price == '':
            price = None

        # 시간 단위 입력하지 않았을 경우
        if time_unit == '-- 기간 --':
            time_unit = None

        item_data = {
            'section': request.data['section'],
            'title': request.data['title'],
            'content': request.data['content'],
            'time_unit': time_unit,
            'price': price,
            'user': request.user.id,
            'category': CategoryModel.objects.get(name=request.data['category']).id,
            'status': '대여 가능'
        }

        item_serializer = ItemPostSerializer(data=item_data)

        # 아이템 모델 벨리데이션 합격하면 저장
        if item_serializer.is_valid():
            item_obj = item_serializer.save()

            # 이미지 포함하는지 체크
            if not 'image' in request.data:
                return Response(item_obj.id, status=status.HTTP_200_OK)
            else:
                images = request.data.pop('image')

                passed_item_image_data_list = []
                for image in images:
                    item_image_data = {
                        'item': item_obj.id,
                        'image': image,
                    }

                    item_image_serializer = ItemImageSerializer(data=item_image_data)

                    # 아이템 이미지 모델 벨리데이션 합격하면 합격 리스트에 추가
                    if item_image_serializer.is_valid():
                        passed_item_image_data_list.append(item_image_serializer)
                
                    # 아이템 이미지 모델 벨리데이션 불합격하면 아이템 모델 삭제
                    else:
                        item_obj.delete()
                        return Response(item_image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                # 모든 이미지가 벨리데이션에 합격했다면 저장
                for passed_item_image_data in passed_item_image_data_list:
                    passed_item_image_data.save()

                return Response(item_obj.id, status=status.HTTP_200_OK)
        
        # 아이템 모델 벨리데이션 불합격
        else:
            return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, item_id):
        user = request.user
        status_ = request.data.get('status')
        
        try:
            item = ItemModel.objects.get(id=item_id, user=user)
            
            if item.status == "대여 가능":
                return Response({"msg": "이미 재등록한 물품입니다."}, status=status.HTTP_208_ALREADY_REPORTED)
            
            item.status = status_
            item.save()
            
            return Response({"msg": "물품이 재등록 되었습니다."}, status=status.HTTP_200_OK)
        except ItemModel.DoesNotExist:
            return Response({"msg": "물품이 더이상 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        


# 물품 수정 페이지
class ItemUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 페이지 로드 데이터 얻기
    def get(self, request, item_id):

        # 데이터 가져오기
        images_data = ItemImageModel.objects.filter(item=item_id).values()
        item_data = ItemModel.objects.get(id=item_id)
        category_data = CategoryModel.objects.all().values('name')

        # 이미지 데이터 다듬기
        image_list = []
        for image_data in images_data:
            del image_data['item_id']
            image_list.append(image_data)

        # 아이템 데이터 다듬기
        item_data = {
            'section': item_data.section,
            'category': item_data.category.name,
            'time_unit': item_data.time_unit,
            'price': item_data.price,
            'status': item_data.status,
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

    # 수정하기
    def put(self, request, item_id):

        # 카테고리 ID 조회
        category = CategoryModel.objects.get(name=request.data['category'])

        # 수정사항 반영
        target_item = ItemModel.objects.get(id=item_id)

        # 시간, 가격 null 처리
        if request.data['time'] == '-- 기간 --':
            target_item.time_unit = None
        else:
            target_item.time_unit = request.data['time']

        if request.data['price'] == '':
            target_item.price = None
        else:
            target_item.price = request.data['price']

        target_item.section = request.data['section']
        target_item.category = category
        target_item.status = request.data['status']
        target_item.title = request.data['title']
        target_item.content = request.data['content']
        target_item.save()

        # 저장할 이미지 DB 저장
        save_images = request.data.getlist('save_image')
        for save_image in save_images:
            item_obj = ItemModel.objects.get(id=item_id)
            ItemImageModel.objects.create(item=item_obj, image=save_image)

        # 삭제할 이미지 DB 삭제
        delete_images = request.data.getlist('delete_image')
        for delete_image in delete_images:
            ItemImageModel.objects.get(id=delete_image).delete()

        return Response(status=status.HTTP_200_OK)
        
        
class ReviewView(APIView):
    permission_classes = [IsAddressOrReadOnly]
    authentication_classes = [JWTAuthentication]

    # 리뷰작성 버튼 클릭시
    def post(self, request, item_id):
        user_id = request.user.id
        content = request.data.get("content")
        rating = request.data.get("rating")
        item = ItemModel.objects.get(id=item_id)
        # 리뷰 평점 유저 스코어에 반영
        # 리뷰 평점/평균 평점을 가져온 후 다시 평균 계산해서 저장
        item.user.score = int(item.user.score or 0) #유저 스코어가 null일 경우에 0으로 반환
        item.user.get_reviews_count = int(item.user.get_reviews_count or 0) 
        item.user.score = ((item.user.score * item.user.get_reviews_count) + (int(rating) * 20)) / (item.user.get_reviews_count + 1)
        item.user.get_reviews_count += 1
        item.user.save()

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