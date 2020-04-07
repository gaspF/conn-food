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

    class Meta:
        model = Farmer
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):
    certified_farmer = serializers.SlugRelatedField(slug_field='farmer_name', queryset=Farmer.objects.all())
    owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    certificate_type = serializers.ChoiceField(choices=CERTIFICATE_CHOICES, default='ORIGINE')

    class Meta:
        model = Certificate
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(read_only=True, slug_field='username')
    producers = serializers.SlugRelatedField(many=True, slug_field='farmer_name', queryset=Farmer.objects.all())

    class Meta:
        model = Product
        fields = '__all__'
