from rest_framework.viewsets import ModelViewSet
from order.models import Order
from order.serializers import OrderSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class OrderViewSet(ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
