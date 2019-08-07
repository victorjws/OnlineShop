from django.urls import path

# from .views import ProductList
from django.views.generic import TemplateView

from product.views import ProductList
from .views import ProductListAPI
from .views import ProductDetailAPI

urlpatterns = [
    # path('test/', TemplateView.as_view(template_name='product/product_detail.html')),
    # path('', TemplateView.as_view(template_name='product/product.html'),
    #      name='product_list'),
    path('', ProductList.as_view(), name='product_list'),
    path('list-api/', ProductListAPI.as_view(), name='product_list_api'),
    path('detail-api/<int:pk>/', ProductDetailAPI.as_view(),
         name='product_detail_api'),
]
