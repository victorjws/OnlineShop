from django.views.generic import ListView
from django.views.generic import DetailView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from product.pagination import ProductPagination
from .models import Category
from .models import Product
from .serializer import CategorySerializer
from .serializer import ProductSerializer


# class ProductList(ListView):
#     model = Product
#     template_name = 'product/product.html'
#     context_object_name = 'product_list'


# class ProductDetail(DetailView):
#     template_name = 'product_detail.html'
#     queryset = Product.objects.all()
#     context_object_name = 'product'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = OrderForm(self.request)
#         return context


class ProductListAPI(ListAPIView):
    serializer_class = ProductSerializer

    # def get_queryset(self):
    #     return Product.objects.all().order_by('-pk')

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-pk')
        limit_count = self.request.query_params.get('limit_count', None)
        category = self.request.query_params.get('category', None)
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

