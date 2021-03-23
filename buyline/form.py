from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from buyline.models import MyUser, Product, Buy, ReturnProduct


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'picture']


class BuyForm(ModelForm):
    class Meta:
        model = Buy
        fields = ['quantity']


class CreationMyUserForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ("username",)
        field_classes = {'username': UsernameField}


class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'quantity',)


class UpdateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'quantity',)
