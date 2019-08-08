from django.views.generic import ListView
from django.views.generic import DetailView
from rest_framework import generics
from rest_framework import mixins

from .models import Product
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


class ProductListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('-pk')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProductDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('pk')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
