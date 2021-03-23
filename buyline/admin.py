from django.contrib import admin

from buyline.models import MyUser, Product, Buy, ReturnProduct


admin.site.register(MyUser)
admin.site.register(Product)
admin.site.register(Buy)
admin.site.register(ReturnProduct)