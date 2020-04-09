from rest_framework import viewsets, permissions, filters
from snippets.models import Farmer, Product, Certificate
from snippets.serializers import FarmerSerializer, ProductSerializer, CertificateSerializer, UserSerializer
from snippets.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from drf_multiple_model.views import ObjectMultipleModelAPIView
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'farmers': reverse('farmer-list', request=request, format=format),
        'products': reverse('product-list', request=request, format=format),
        'certificates': reverse('certificate-list', request=request, format=format),

    })


class FarmerViewSet(viewsets.ModelViewSet):
    """
    Displaying the farmer-list view, by selecting all of the Farmer objects and serializing them with FarmerSerializer
    class. Only the creator can edit it's data.
    """

    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LimitPagination(MultipleModelLimitOffsetPagination):
    """
    This class set a pagination limit to the class CertificateProductList.
    """

    default_limit = 2


class CertificateProductList(ObjectMultipleModelAPIView):
    """
    Displaying the farmer-highlight view, by grouping all of the products and certificates instances related to a
    specific farmer in a querylist, and displaying it on a unique view.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    pagination_class = LimitPagination

    def get_querylist(self):
        """
        This method get the primary key of a farmer by catching it from the URL argument, and setting it as a filter
        criteria.
        """

        pk = self.kwargs.get('pk')
        querylist = [
            {'queryset': Product.objects.filter(producers=pk), 'serializer_class': ProductSerializer},
            {'queryset': Certificate.objects.filter(certified_farmer=pk), 'serializer_class': CertificateSerializer},
        ]

        return querylist


class ProductViewSet(viewsets.ModelViewSet):
    """
    Displaying the Product view,  by selecting all of the Product objects and serializing them with ProductSerializer
    class. Only the creator can edit it's data.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CertificateViewSet(viewsets.ModelViewSet):
    """
    Displaying the Certificate view,  by selecting all of the Certificate objects and serializing them with
    CertificateSerializer class. Only the creator can edit it's data.
    """

    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['certificate_type']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Displaying the User view,  by selecting all of the User objects and serializing them with
    UserSerializer class.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer