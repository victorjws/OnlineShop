from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView

from product.models import Review
from product.serializer import ReviewSerializer
from .models import Category
from .models import Product
from .serializer import CategorySerializer
from .serializer import ProductSerializer


class ProductListAPI(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-pk')
        limit_count = self.request.query_params.get('limit_count', None)
        category = self.request.query_params.get('category', None)
        # limit_count = self.request.data['limit_count']
        # category = self.request.data['category']
        if limit_count:
            queryset = queryset[:int(limit_count)]
        if category:
            queryset = queryset.filter(categories=category)
        return queryset


class ProductDetailAPI(RetrieveAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('pk')


class CategoryListAPI(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all().order_by('pk')


class ReviewListAPI(ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product = self.request.query_params.get('product-id', None)
        return Review.objects.filter(product=product)
