from rest_framework import serializers
from item.models import Item as ItemModel
from item.models import Category as CategoryModel


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