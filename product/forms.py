from django import forms
from .models import *
from django.forms import ModelForm


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
        exclude = ['username', 'product_name']