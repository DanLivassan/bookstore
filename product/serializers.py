from rest_framework import serializers
from product.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title", "description", "slug", "active")


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, many=True)

    class Meta:
        model = Product
        fields = ("id", "title", "description", "category",
                  "price", "active", "category_ids")

    def create(self, validated_data):
        categories_data = validated_data.pop('category_ids')
        product = Product.objects.create(**validated_data)
        for category in categories_data:
            product.category.add(category)
        return product
