from django.urls import path, include, re_path


urlpatterns = [
    re_path("bookstore/(?P<version>(v1|v2))/", include('order.urls')),
    re_path("bookstore/(?P<version>(v1|v2))/", include('product.urls')),
]
