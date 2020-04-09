from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from .models import Farmer, Product, Certificate
from django.contrib.auth.models import User


class URLTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('snippets.urls')),
    ]

    def test_farmer_list(self):
        url = reverse('farmer-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_certificate_list(self):
        url = reverse('certificate-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_farmer_highlights(self):
        url = reverse('farmer-highlight', kwargs={'pk': 3})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)


class CreateDataTestCase(APITestCase):
    def setUp(self):
        self.user = User()
        self.user.username = "gaspf"
        self.user.email = "fouchegaspard@gmail.com"
        self.user.password = "Pagode22101949"
        self.user.url = reverse('user-list')
        self.user.save()

        self.farmer = Farmer()
        self.farmer.owner = self.user
        self.farmer.url = reverse('farmer-list')
        self.farmer.farmer_name = "Pierre"
        self.farmer.farmer_siret_number = "839293718392"
        self.farmer.farmer_address = "23 rue Diaz"
        self.farmer.save()

        self.certificate = Certificate()
        self.certificate.owner = self.user
        self.certificate_name = "VLOG"
        self.certificate_type = "Origine"
        self.certificate.url = reverse('certificate-list')
        self.certificate.certified_farmer = self.farmer
        self.certificate.save()

    def test_user_creation(self):
        self.client.login(username=self.user.username,
                          password=self.user.password
                          )
        response = self.client.get(self.user.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(User.objects.count(), 1)

    def test_farmer_creation(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.farmer.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(Farmer.objects.count(), 1)

    def test_product_creation(self):
        product = Product.objects.create(owner=self.user,
                                       product_name="Pomme",
                                       product_unit="839293718392",
                                       )

        product.url = reverse('product-list')
        product.producers.add(self.farmer)
        product.save()
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(product.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(User.objects.count(), 1)

    def test_certificate_creation(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.certificate.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(Certificate.objects.count(), 1)
