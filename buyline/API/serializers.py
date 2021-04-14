from rest_framework import serializers

from buyline.models import MyUser, Product, Buy, Author, Book, ReturnProduct

GENDER = [
    ('N', 'None'),
    ('M', 'Man'),
    ('W', 'Woman'),
]
LANGUAGE = [
    (0, 'A1 - Elementary'),
    (1, 'A2 - Pre Intermediate'),
    (2, 'B1 - Intermediate'),
    (3, 'B2 - Upper Intermediate'),
    (4, 'C1 - Advanced'),
    (5, 'C2 - Proficient'),
]


class LanguageReady(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    gender = serializers.ChoiceField(choices=GENDER)
    language = serializers.ChoiceField(choices=LANGUAGE)

    def validate(self, attrs):
        if (attrs['age'] > 20 and attrs['gender'] == 'M' and attrs['language'] > 2) or \
                (attrs['age'] > 22 and attrs['gender'] == 'W' and attrs['language'] > 1):
            return attrs
        raise serializers.ValidationError("You don't success")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity']

    def validate(self, attrs):
        if attrs['price'] < 0:
            raise serializers.ValidationError("Price don't success")
        elif attrs['quantity'] < 0:
            raise serializers.ValidationError("Quantity don't success")
        else:
            return attrs


class BuySerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Buy
        fields = ['user', 'product', 'quantity', 'buy_at']

    def validate(self, attrs):
        if attrs['quantity'] <= 0:
            raise serializers.ValidationError("Don't have quantity")
        return attrs


class ListBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buy
        fields = ['user', 'product', 'quantity', 'buy_at']


class UserSerializer(serializers.ModelSerializer):
    buys = ListBuySerializer(many=True, source='buy_user')

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'password', 'money', 'is_staff', 'is_active', 'buys']

    def validate(self, attrs):
        if attrs['money'] < 0:
            raise serializers.ValidationError("Money don't success")
        if not attrs['is_staff']:
            print('do not is staff')
        if not attrs['is_active']:
            print("don't is active")
        return attrs

# 38

class AuthorBookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'age']


class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author']


class AuthorBookIdSerializers(serializers.ModelSerializer):
    books = serializers.PrimaryKeyRelatedField(many=True, source='author_book', read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'age', 'books']

# modul
# Admin

class AdminReturnProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReturnProduct
        fields = ['id', 'buy', 'return_product_at']


class AdminProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity']

# User

class BuyUserSerializers(serializers.ModelSerializer):
    buy_at = serializers.DateTimeField(required=False)

    class Meta:
        model = Buy
        fields = ['id', 'product', 'user', 'quantity', 'buy_at']


class UserCreateReturnProductSerializers(serializers.ModelSerializer):
    return_product_at = serializers.DateTimeField(required=False)

    class Meta:
        model = ReturnProduct
        fields = ['id', 'buy', 'return_product_at']

# All

class ListProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity']






