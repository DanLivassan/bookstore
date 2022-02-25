from unicodedata import category
from rest_framework import serializers
from product.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title", "description", "slug", "active")


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True, many=True)

    class Meta:
        model = Product
        fields = ("id", "title", "description", "category", "price", "active")
