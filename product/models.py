from django.db import models
from django.core import validators
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    quantity = models.IntegerField()
    made_in_country = models.CharField(max_length=20)
    image_url = models.FileField(upload_to='static/images/uploads')

    def __str__(self):
        return self.name


class Order(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    phone_number = models.CharField(max_length=10, validators=[validators.MinLengthValidator(10)])
    address = models.CharField(max_length=100)