from django.urls import path
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('farmers/', views.FarmerList.as_view(), name='farmer-list'),
    path('farmers/<int:pk>/', views.FarmerDetail.as_view(), name='farmer-detail'),
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    path('certificates/', views.CertificateList.as_view(), name='certificate-list'),
    path('certificates/<int:pk>/', views.CertificateDetail.as_view(), name='certificate-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail')
])
