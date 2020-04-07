from django.urls import path
from snippets import views
from snippets.views import FarmerViewSet, UserViewSet, ProductViewSet, CertificateViewSet
from rest_framework.urlpatterns import format_suffix_patterns


farmer_list = FarmerViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
farmer_detail = FarmerViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
product_list = ProductViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
product_detail = ProductViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
certificate_list = CertificateViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
certificate_detail = CertificateViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})


urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('farmers/', farmer_list, name='farmer-list'),
    path('farmers/<int:pk>/', farmer_detail, name='farmer-detail'),
    path('products/', product_list, name='product-list'),
    path('products/<int:pk>/', product_detail, name='product-detail'),
    path('certificates/', certificate_list, name='certificate-list'),
    path('certificates/<int:pk>/', certificate_detail, name='certificate-detail'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
])

