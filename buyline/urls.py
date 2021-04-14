from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from .API.resorces import AuthorViewSet, BookViewSet, ExampleView, UserSetView, ListProductView, \
    CreateReturnProductView, SuperuserReturnProductView, AdminProductView
from .views import Login, Registration, Logout, ListProducts, CreateBuy, ListBuyUsers, ReturnBuy, \
    ListReturnProduct, DeleteReturnProduct, DeleteBuy, UpdateProduct, CreateProduct

router = routers.SimpleRouter()
router.register(r'author', AuthorViewSet)
router.register(r'book', BookViewSet)
# Modul REST
router.register(r'admin', SuperuserReturnProductView)
router.register(r'cuproduct', AdminProductView)

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('api/', include(router.urls)),
    path('example/', ExampleView.as_view()),

    # Modul REST

    path('api/list/', ListProductView.as_view()),
    path('api/user/', UserSetView.as_view()),
    path('api/user/return/', CreateReturnProductView.as_view()),

    # Modul Django

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
