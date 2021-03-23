from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils.timezone import make_aware


class MyUser(AbstractUser):
    money = models.IntegerField(null=False, blank=False, default=10000)

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(money__gte=0), name='money_gte_0'),
        ]


class Product(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=False, blank=False, default=0)
    picture = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)

    class Meta:
        ordering = ['name']
        constraints = [
            models.CheckConstraint(check=Q(price__gte=0), name='price_gte_0'),
            models.CheckConstraint(check=Q(quantity__gte=0),  name='product_quantity_gte_0')
        ]


class Buy(models.Model):
    product = models.ForeignKey(Product, related_name='product', on_delete=models.PROTECT)
    user = models.ForeignKey(MyUser, related_name='user', on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=1)
    buy_at = models.DateTimeField()

    class Meta:
        ordering = ['-buy_at', 'product']
        constraints = [
            models.CheckConstraint(check=Q(quantity__gte=0), name='buy_quantity_gte_0'),
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.buy_at = make_aware(datetime.now())
        return super().save(*args, **kwargs)


class ReturnProduct(models.Model):
    buy = models.ForeignKey(Buy, related_name='buy', on_delete=models.CASCADE)
    return_product_at = models.DateTimeField()

    class Meta:
        ordering = ['-return_product_at']

    def save(self, *args, **kwargs):
        if not self.id:
            self.return_product_at = make_aware(datetime.now())
        return super().save(*args, **kwargs)