from django.contrib import admin
from django.urls import path

from .views import Login, Registration, Logout, ListProducts, CreateBuy, ListBuyUsers, ReturnBuy, \
    ListReturnProduct, DeleteReturnProduct, DeleteBuy, UpdateProduct, CreateProduct

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('registration/', Registration.as_view(), name='registration'),
    path('loguot/', Logout.as_view(), name='logout'),

    path('', ListProducts.as_view(), name='list_product'),

    path('update/product/<int:pk>', UpdateProduct.as_view(), name='update_product'),
    path('create/product/', CreateProduct.as_view(), name='create_product'),

    path('delete/return/<int:pk>', DeleteReturnProduct.as_view(), name='delete_return_product'),
    path('delete/buy/<int:pk>', DeleteBuy.as_view(), name='delete_buy'),
    path('list/buy/return/', ListReturnProduct.as_view(), name='list_return_product'),

    path('buy/<int:pk>', CreateBuy.as_view(), name='create_buy'),
    path('buy/list/', ListBuyUsers.as_view(), name='list_buy'),
    path('buy/return/<int:pk>', ReturnBuy.as_view(), name='return_buy'),
]
