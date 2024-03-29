from rest_framework import serializers
from datetime import datetime
from contract.models import Contract as ContractModel, Review as ReviewModel
from item.models import (
    Item as ItemModel,
    Category as CategoryModel,
    Bookmark as BookmarkModel,
    ItemImage as ItemImageModel,
)


# 아이템 모델 직렬화 (물품 등록 페이지)
class ItemPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemModel
        fields = ["id", "section", "title", "content", "time_unit", "price", 
                  "user", "category", "created_at", "updated_at", "status"]


# 아이템 이미지 모델 직렬화
class ItemImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ItemImageModel
        fields = ["id", "item", "image"]


# 카테고리 모델 직렬화
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CategoryModel
        fields = ["name"]


# 아이템 모델 직렬화
class ItemSerializer(serializers.ModelSerializer):
    item_bookmarks = serializers.SerializerMethodField()
    item_inquiries = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    
    def get_item_bookmarks(self, obj):
        #아이템 찜 수
        return obj.bookmark_set.count()
    
    def get_item_inquiries(self, obj):
        #아이템 문의 수
        return obj.chatroom_set.count()
    
    def get_image(self, obj):
        #아이템의 첫번째 이미지 한개
        try:
            main_image = obj.itemimage_set.first().image.url
            return main_image
        except AttributeError:
            return None
        
    class Meta:
        model = ItemModel
        fields = ["id", "section", "category", "image", "title", "price", 
                "time_unit", "item_bookmarks", "item_inquiries"]


# 아이템 모델 직렬화 (마이페이지)
class MyPageItemSerializer(serializers.ModelSerializer):
    # images = ItemImageSerializer(many=True, source='itemimage_set')
    image = serializers.SerializerMethodField()
    
    def get_image(self, obj):
        #아이템의 첫번째 이미지 한개
        try:
            main_image = obj.itemimage_set.first().image.url
            return main_image
        except AttributeError:
            return None
    
    class Meta:
        model = ItemModel
        fields = ["id", "user", "section", "image", "title", "status"]


# Contract 모델 직렬화
class ContractSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ContractModel
        fields = ["id", "item", "status", "user", "start_date", "end_date"]


# 리뷰 모델 직렬화 (물품 상세 페이지)
class DetailReviewSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    period = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    def get_image(self, obj):
        image = obj.user.image
        return image.url

    def get_nickname(self, obj):
        nickname = obj.user.nickname
        return nickname

    def get_period(self, obj):
        contract = obj.contract
        period = str(contract.end_date - contract.start_date)
        
        # 대여 기간 계산
        if period.find('day') != -1:
            period = period.split(',')[0]
            # 1일 이상 대여 시
            period = f"{period.split(' ')[0]}일 대여"
        
        else :
            # 1일 미만 대여 시
            period = f"{period.split(':')[0]}시간 대여"
        
        return period

    def get_created_at(self, obj):
        created_at = str(datetime.now() - obj.created_at)
        
        # 작성 기간 계산
        if created_at.find('day') != -1:
            created_at = created_at.split(',')[0]
            # 작성한지 1일 이상
            created_at = f"{created_at.split(' ')[0]}일 전"
        
        elif int(created_at.split(':')[0]) >= 1:
            # 작성한지 1일 미만
            created_at = f"{created_at.split(':')[0]}시간 전"

        elif int(created_at.split(':')[0]) < 1:
            # 작성한지 1시간 미만
            created_at = "방금 전"

        return created_at


    class Meta:
        model = ReviewModel
        fields = ["image", "user", "item", "contract", "nickname", "content", "created_at", "star", "period"]

    extra_kwargs = {
            'star' : {'write_only': True}
        }


# 아이템 모델 직렬화 (물품 상세 페이지)
class DetailSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    remain_time = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    is_bookmark = serializers.SerializerMethodField()
    bookmark_length = serializers.SerializerMethodField()
    chatroom_length = serializers.SerializerMethodField()
    reviews = DetailReviewSerializer(many=True, source='review_set')

    def get_user(self, obj):
        user = {}
        image = obj.user.image.url
        id =obj.user.id
        nickname = obj.user.nickname
        address = obj.user.address
        user['score'] = obj.user.score
        user['image'] = image
        user['id'] = id
        user['nickname'] = nickname
        user['address'] = address

        return user

    def get_images(self, obj):
        image_list = obj.itemimage_set.values('image')
        images = [f"https://egodaeyeo.s3.amazonaws.com/{image['image']}" for image in image_list]

        return images

    def get_remain_time(self, obj):
        
        if obj.status == '대여 중':
            contract = ContractModel.objects.get(item=obj.id, status='대여 중')
            remain_time = str(contract.end_date - contract.start_date)
            
            # 대여 남은 시간 계산
            if remain_time.find('day') != -1:
                remain_time = remain_time.split(',')[0]
                # 1일 이상 남음
                remain_time = f"{remain_time.split(' ')[0]}일 남음"
            
            elif int(remain_time.split(':')[0]) >= 1:
                # 1일 미만 남음
                remain_time = f"{remain_time.split(':')[0]}시간 남음"

            elif int(remain_time.split(':')[0]) < 1:
                # 1시간 미만 남음
                remain_time = "반납 임박"

            return remain_time
            
        else :
            return

    def get_created_at(self, obj):
        created_at = str(datetime.now() - obj.created_at)

        # 포스트 작성 시간 계산
        if created_at.find('day') != -1:
            created_at = created_at.split(',')[0]
            # 작성한지 1일 이상
            created_at = f"{created_at.split(' ')[0]}일 전"

        elif int(created_at.split(':')[0]) >= 1:
            # 작성한지 1일 미만
            created_at = f"{created_at.split(':')[0]}시간 전"

        elif int(created_at.split(':')[0]) < 1:
            # 작성한지 1시간 미만
            created_at = "방금 전"

        return created_at

    def get_category(self, obj):
        return obj.category.name

    def get_is_bookmark(self, obj):
        # 해당 아이템에 로그인 유저가 찜했는지 여부 체크
        try:
            BookmarkModel.objects.get(item=obj.id, user=self.context['login_id'])
            return True
        # 찜하지 않았을 시
        except BookmarkModel.DoesNotExist:
            return False
        except ValueError:
            return False

    def get_bookmark_length(self, obj):
        bookmarks = obj.bookmark_set
        return bookmarks.count()

    def get_chatroom_length(self, obj):
        chatrooms = obj.chatroom_set
        return chatrooms.count()

    class Meta:
        model = ItemModel
        fields = ["id", "user", "section", "category", "status", "remain_time", "title", "images",
                    "content", "time_unit", "price", "created_at", "updated_at",
                    "is_bookmark", "bookmark_length", "chatroom_length", "reviews"]