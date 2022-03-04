from numpy import product
from rest_framework import serializers
from product.serializers import ProductSerializer

from order.models import Order
from product.models import Product


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True, many=True)
    products_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, many=True)
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        total = sum([product.price for product in instance.products.all()])
        return total

    class Meta:
        model = Order
        fields = ["products", "total", 'products_ids', 'user']
        extra_kwargs = {'product': {'required': False}}

    def create(self, validated_data):
        product_data = validated_data.pop('products_ids')
        order = Order.objects.create(**validated_data)
        for product in product_data:
            order.products.add(product)
        return order
