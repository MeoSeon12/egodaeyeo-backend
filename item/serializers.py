from rest_framework import serializers
from item.models import Item as ItemModel
from item.models import Category as CategoryModel
from user.models import User as UserModel


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
# class UserDetailSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = UserModel
#         fields = ["nickname", "address", "image", "score"]


class ItemDetailSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    bookmark_length = serializers.SerializerMethodField()
    inquiry_length = serializers.SerializerMethodField()
    # reviews = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = {}
        nickname = obj.user.nickname
        address = obj.user.address
        user['nickname'] = nickname
        user['address'] = address

        return user

    def get_category(self, obj):
        return obj.category.name

    def get_bookmark_length(self, obj):
        bookmarks = obj.bookmark_set
        return bookmarks.count()

    def get_inquiry_length(self, obj):
        inquiries = obj.inquiry_set
        return inquiries.count()

    class Meta:
        model = ItemModel
        fields = ["id", "user", "section", "category", "status", "title", "images",
                    "content", "time_unit", "price", "created_at", "updated_at",
                    "bookmark_length", "inquiry_length",]

