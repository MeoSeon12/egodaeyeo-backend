from rest_framework import serializers
from datetime import datetime
from contract.models import Contract as ContractModel
from item.models import (
    Item as ItemModel,
    Category as CategoryModel,
    Review as ReviewModel,
    Bookmark as BookmarkModel
)


# 아이템 페이지 직렬화
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CategoryModel
        fields = ["name"]

class ItemSerializer(serializers.ModelSerializer):
    user_address = serializers.SerializerMethodField()
    item_bookmarks = serializers.SerializerMethodField()
    item_inquiries = serializers.SerializerMethodField()
    
    def get_user_address(self, obj):
        #아이템 등록자 주소
        return obj.user.address
    
    def get_item_bookmarks(self, obj):
        #아이템 찜 수
        return obj.bookmark_set.count()
    
    def get_item_inquiries(self, obj):
        #아이템 문의 수
        return obj.inquiry_set.count()
    
    
    class Meta:
        model = ItemModel
        fields = ["id", "section", "category", "title", "images", "price", "time_unit", "user_address", "item_bookmarks", "item_inquiries"]



# 아이템 상세 페이지 직렬화
# 리뷰 직렬화
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
        period = ContractModel.objects.get(item=obj.item, user=obj.user)
        period = str(period.end_date - period.start_date)
        
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
        fields = ["image", "nickname", "content", "created_at", "period"]


# 아이템 직렬화
class DetailSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    remain_time = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    is_bookmark = serializers.SerializerMethodField()
    bookmark_length = serializers.SerializerMethodField()
    inquiry_length = serializers.SerializerMethodField()
    reviews = DetailReviewSerializer(many=True, source='review_set')

    def get_user(self, obj):
        user = {}
        image = obj.user.image.url
        nickname = obj.user.nickname
        address = obj.user.address
        score = obj.user.score
        user['image'] = image
        user['nickname'] = nickname
        user['address'] = address
        user['score'] = score

        return user

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
        except:
            return False

    def get_bookmark_length(self, obj):
        bookmarks = obj.bookmark_set
        return bookmarks.count()

    def get_inquiry_length(self, obj):
        inquiries = obj.inquiry_set
        return inquiries.count()


    class Meta:
        model = ItemModel
        fields = ["id", "user", "section", "category", "status", "remain_time", "title", "images",
                    "content", "time_unit", "price", "created_at", "updated_at",
                    "is_bookmark", "bookmark_length", "inquiry_length", "reviews"]

