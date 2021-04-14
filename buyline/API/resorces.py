from rest_framework import permissions, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.mixins import ListModelMixin, DestroyModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSetMixin, GenericViewSet

from buyline.API.serializers import AuthorBookSerializers, BookSerializers, AuthorBookIdSerializers, \
    BuyUserSerializers, ListProductSerializers, UserCreateReturnProductSerializers, \
    AdminReturnProductSerializers, AdminProductSerializers
from buyline.models import Author, Book, ReturnProduct, Buy, Product


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorBookSerializers

    def list(self, request, *args, **kwargs):
        book_name = request.query_params.get('book_name', False)
        if book_name:
            self.queryset = Author.objects.filter(author_book__title__icontains=book_name)
        return super().list(request, *args, **kwargs)

    @action(detail=True)
    def author_books_id(self, request, pk=None):
        author = self.get_object()
        serializer = AuthorBookIdSerializers(author)
        return Response(serializer.data)


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializers

    def list(self, request, *args, **kwargs):
        age = request.query_params.get('author_age', False)
        if age:
            self.queryset = Book.objects.filter(author__age__gte=age)
        return super().list(request, *args, **kwargs)


class ExampleView(APIView):
    authentication_classes = [BasicAuthentication]

    def get(self, request, format=None):
        content = {
            'user': request.user.username,
            'auth': request.auth,
        }
        return Response(content)




# modul

# Admin

class SuperuserReturnProductView(DestroyModelMixin, ListModelMixin, GenericViewSet, ViewSetMixin):
    queryset = ReturnProduct.objects.all()
    serializer_class = AdminReturnProductSerializers
    permission_classes = [permissions.IsAdminUser]
    http_method_names = [u'get', u'delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.retrieve = request.data.get('retrieve', False)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete(keep_parents=self.retrieve)


class AdminProductView(CreateModelMixin, UpdateModelMixin, GenericViewSet, ViewSetMixin):
    queryset = Product.objects.all()
    serializer_class = AdminProductSerializers
    permission_classes = [permissions.IsAdminUser]

# User

class UserSetView(ListCreateAPIView):
    queryset = Buy.objects.all()
    serializer_class = BuyUserSerializers
    permission_classes = [permissions.IsAuthenticated]

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)


class CreateReturnProductView(CreateAPIView):
    queryset = ReturnProduct.objects.all()
    serializer_class = UserCreateReturnProductSerializers
    permission_classes = [permissions.IsAuthenticated]

# All

class ListProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ListProductSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


