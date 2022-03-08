from django.urls import path, include, re_path
from rest_framework.authtoken import views


urlpatterns = [
    re_path("bookstore/(?P<version>(v1|v2))/", include('order.urls')),
    re_path("bookstore/(?P<version>(v1|v2))/", include('product.urls')),
]
urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]
