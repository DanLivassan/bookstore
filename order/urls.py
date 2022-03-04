from rest_framework.routers import SimpleRouter as Router
from django.urls import path, include
from order.views import OrderViewSet


router = Router()
router.register(r'order', OrderViewSet, basename='order')

urlpatterns = [
    path("", include(router.urls)),
]
