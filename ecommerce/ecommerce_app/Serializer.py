from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import *

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None


class CartItem_Serializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source='product.name',read_only=True)
    price=serializers.IntegerField(source="product.price",read_only=True)
    image=serializers.ImageField(source="product.image",read_only=True)

    class Meta:
        model=CartItem
        fields=["id","product_name","price","image","quantity","product"]

class Cart_serializer(ModelSerializer):
    items=CartItem_Serializer(many=True)

    class Meta:
        model=Cart
        fields=["id","items"]