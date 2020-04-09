from django.db import models

CERTIFICATE_CHOICES = (
    ('BIOLOGIQUE', 'Biologique'),
    ('SANS_OGM', 'Sans OGM'),
    ('ORIGINE', 'Origine'),
)


class Farmer(models.Model):
    """
    Data model of a Farmer instance
    """

    owner = models.ForeignKey('auth.User', related_name='farmers', on_delete=models.CASCADE)
    farmer_creation_date = models.DateTimeField(auto_now_add=True)
    farmer_name = models.CharField(max_length=100, blank=False)
    farmer_siret_number = models.PositiveIntegerField(blank=False)
    farmer_address = models.TextField(blank=False)

    class Meta:
        ordering = ['farmer_creation_date']

    def __str__(self):
        return '{}'.format(self.farmer_name)


class Product(models.Model):
    """
    Data model of a Product instance
    """

    owner = models.ForeignKey('auth.User', related_name='products', on_delete=models.CASCADE)
    product_creation_date = models.DateTimeField(auto_now_add=True)
    product_name = models.CharField(max_length=100, blank=False)
    product_unit = models.PositiveIntegerField(blank=False)
    international_food_code = models.TextField(max_length=15, blank=False)
    producers = models.ManyToManyField(Farmer)

    class Meta:
        ordering = ['product_creation_date']

    def __str__(self):
        return '{} {} {} {}'.format(self.product_name, self.product_unit, self.international_food_code, self.producers)


class Certificate(models.Model):
    """
    Data model of a Certificate instance
    """

    owner = models.ForeignKey('auth.User', related_name='certificates', on_delete=models.CASCADE)
    certificate_creation_date = models.DateTimeField(auto_now_add=True)
    certificate_name = models.CharField(max_length=100, blank=False)
    certificate_type = models.CharField(max_length=10, default='ORIGINE', choices=CERTIFICATE_CHOICES)
    certified_farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE,)

    class Meta:
        ordering = ['certificate_creation_date']

    def __str__(self):
        return '{}: {} {} {}'.format(self.certificate_creation_date, self.certified_farmer, self.certificate_name, self.certificate_type.name)