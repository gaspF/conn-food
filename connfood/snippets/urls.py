from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views


router = DefaultRouter()
router.register(r'farmers', views.FarmerViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'certificates', views.CertificateViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('farmers/<int:pk>/certificate_products/', views.CertificateProductList.as_view(), name='farmer-highlight'),
]
