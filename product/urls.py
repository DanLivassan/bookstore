from rest_framework.routers import SimpleRouter as Router
from django.urls import path, include
from product.views import CategoryViewSet, ProductViewSet


router = Router()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'category', CategoryViewSet, basename='category')

urlpatterns = [
    path("", include(router.urls)),
]
