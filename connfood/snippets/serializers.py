from rest_framework import serializers
from snippets.models import Farmer, Product, Certificate, CERTIFICATE_CHOICES
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    farmers = serializers.PrimaryKeyRelatedField(many=True, queryset=Farmer.objects.all())
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())
    certificates = serializers.PrimaryKeyRelatedField(many=True, queryset=Certificate.objects.all())

    class Meta:
        model = User
        fields = '__all__'


class FarmerSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    certificate_products = serializers.HyperlinkedIdentityField(view_name='farmer-highlight', format='html')

    class Meta:
        model = Farmer
        fields = ['url', 'id', 'owner', 'farmer_name', 'farmer_siret_number', 'farmer_address', 'certificate_products']


class CertificateSerializer(serializers.ModelSerializer):
    certified_farmer = serializers.SlugRelatedField(slug_field='farmer_name', queryset=Farmer.objects.all())
    owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    certificate_type = serializers.ChoiceField(choices=CERTIFICATE_CHOICES, default='ORIGINE')

    class Meta:
        model = Certificate
        fields = ['url', 'id', 'owner', 'certificate_name', 'certificate_name', 'certificate_type', 'certified_farmer']


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    producers = serializers.SlugRelatedField(many=True, slug_field='farmer_name', queryset=Farmer.objects.all())

    class Meta:
        model = Product
        fields = ['url', 'id', 'owner', 'product_name', 'product_unit', 'international_food_code', 'producers']
