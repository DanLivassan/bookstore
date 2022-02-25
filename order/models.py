from django.db import models

from product.models import Product
from django.contrib.auth import get_user_model


class Order(models.Model):
    products = models.ManyToManyField(Product, blank=False)
    user = models.ForeignKey(
        get_user_model(), blank=False, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.email} with {self.products.count()} products"
