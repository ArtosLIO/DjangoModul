from django.test import TestCase
from rest_framework.test import APIClient

from buyline.models import MyUser, Product, Buy


class TestLoginUser(TestCase):

    def setUp(self):
        MyUser.objects.create_user(username='test', password='1q2w3e')
        # self.client = APIClient()

    def test_login(self):
        user = self.client.login(username='test', password='1q2w3e')
        self.assertTrue(user)

    def test_false_username(self):
        user = self.client.login(username='tes', password='1q2w3e')
        self.assertFalse(user)

    def test_false_password(self):
        user = self.client.login(username='test', password='1q2w3')
        self.assertFalse(user)

    def test_false_user_pass(self):
        user = self.client.login(username='tes', password='1q2w3')
        self.assertFalse(user)


class TestBuy(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create_user(username='test', password='1q2w3e', money=50000)
        self.product = Product.objects.create(name='test case', price=2000, quantity=10)
        self.buy = Buy.objects.create(user=self.user, product=self.product)

    def test_buy_default(self):
        self.assertEqual(self.buy.quantity, 1)

    def test_buy_user(self):
        self.assertEqual(self.buy.user.money, 48000)

    def test_buy_quantity(self):
        self.assertEqual(self.buy.product.quantity, 9)
