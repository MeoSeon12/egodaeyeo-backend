from rest_framework import serializers
from item.models import Item as ItemModel
from item.models import Category as CategoryModel


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CategoryModel
        fields = ["name"]

class ItemSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = ItemModel
        fields = "__all__"