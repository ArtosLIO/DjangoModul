from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from buyline.form import CreationMyUserForm, BuyForm, CreateProductForm, UpdateProductForm
from buyline.models import Product, Buy, MyUser, ReturnProduct


class Login(LoginView):
    template_name = 'login.html'


class Registration(CreateView):
    form_class = CreationMyUserForm
    template_name = 'registration.html'
    success_url = '/'


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'


class ListProducts(ListView):
    model = Product
    template_name = 'list_product.html'
    extra_context = {'buy_form': BuyForm()}

# Superuser

class UpdateProduct(UserPassesTestMixin, UpdateView):
    model = Product
    form_class = UpdateProductForm
    template_name = 'update_product.html'
    http_method_names = ['post', 'get']
    success_url = '/'

    def test_func(self):
        return self.request.user.is_staff


class CreateProduct(UserPassesTestMixin, CreateView):
    form_class = CreateProductForm
    template_name = 'create_product.html'
    http_method_names = ['post', 'get']
    success_url = '/'

    def test_func(self):
        return self.request.user.is_staff


class ListReturnProduct(UserPassesTestMixin, ListView):
    model = ReturnProduct
    template_name = 'list_return_product.html'

    def test_func(self):
        return self.request.user.is_staff


class DeleteReturnProduct(UserPassesTestMixin, DeleteView):
    model = ReturnProduct
    success_url = '/list/buy/return/'

    def test_func(self):
        return self.request.user.is_staff


class DeleteBuy(UserPassesTestMixin, DeleteView):
    model = Buy
    success_url = '/list/buy/return/'

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.product.quantity += self.object.quantity
        self.object.user.money += self.object.product.price * self.object.quantity
        self.object.product.save()
        self.object.user.save()
        self.object.delete()
        return HttpResponseRedirect(success_url)

# Users

class CreateBuy(LoginRequiredMixin, CreateView):
    form_class = BuyForm
    template_name = 'create_buy.html'
    http_method_names = ['post', 'get']
    success_url = '/'

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        id_product = kwargs.get('pk')

        if form.is_valid():
            buy = form.save(commit=False)
            buy.product = Product.objects.get(pk=id_product)
            buy.user = request.user
            buy.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class ListBuyUsers(LoginRequiredMixin, ListView):
    model = Buy
    template_name = 'list_buy.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

class ReturnBuy(LoginRequiredMixin, CreateView):
    model = ReturnProduct
    fields = ['buy']
    http_method_names = ['get']
    template_name = 'list_buy.html'
    success_url = '/buy/list/'

    def get(self, request, *args, **kwargs):
        buy_id = kwargs.get('pk')
        end_time = datetime.now() - timedelta(minutes=30)
        obj_buy = Buy.objects.filter(pk=buy_id, buy_at__gte=end_time)
        self.extra_context = {'object_list': Buy.objects.filter(user=self.request.user)}

        if len(obj_buy):
            obj_return_product = ReturnProduct.objects.filter(buy=obj_buy[0])
            request.session['has_already'] = False
            request.session['buy_at'] = (False, buy_id)

            if len(obj_return_product):
                request.session['has_already'] = True
                return super().get(request, *args, **kwargs)
            rp = ReturnProduct()
            rp.buy = obj_buy[0]
            rp.save()
            return super().get(request, *args, **kwargs)
        else:
            request.session['has_already'] = False
            request.session['buy_at'] = (True, buy_id)
            return super().get(request, *args, **kwargs)