from datetime import datetime, timedelta

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
    product = models.ForeignKey(Product, related_name='buy_product', on_delete=models.PROTECT)
    user = models.ForeignKey(MyUser, related_name='buy_user', on_delete=models.CASCADE)
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
            if self.product.quantity >= self.quantity and self.user.money >= self.product.price * self.quantity:
                self.product.quantity -= self.quantity
                self.user.money -= self.product.price
                self.product.save()
                self.user.save()
            else:
                raise Exception(None, "You don`t have money or store don`t have quantity product")
        return super().save(*args, **kwargs)


class ReturnProduct(models.Model):
    buy = models.ForeignKey(Buy, related_name='return_buy', on_delete=models.CASCADE)
    return_product_at = models.DateTimeField()

    class Meta:
        ordering = ['-return_product_at']

    def save(self, *args, **kwargs):
        try:
            ReturnProduct.objects.get(buy=self.buy_id)
        except self.DoesNotExist:
            if not self.id:
                self.return_product_at = make_aware(datetime.now())
                if (self.return_product_at - timedelta(minutes=10)) < self.buy.buy_at:
                    return super().save(*args, **kwargs)
                else:
                    raise Exception(None, "Return time is out ")
        else:
            raise Exception(None, "The object already exists")

    def delete(self, using=None, keep_parents=False):
        if keep_parents:
            self.buy.user.money += self.buy.product.price * self.buy.quantity
            self.buy.product.quantity += self.buy.quantity
            self.buy.user.save()
            self.buy.product.save()
            self.buy.delete()
        return super().delete()


# 38

class Author(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    age = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['name']


class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(Author, related_name='author_book', on_delete=models.CASCADE)

    class Meta:
        ordering = ['title']

    def save(self, *args, **kwargs):
        self.title = self.title + '!'
        return super().save(*args, **kwargs)







