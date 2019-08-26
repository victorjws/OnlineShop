from django.urls import path
from django.views.generic import TemplateView

from .views import CategoryListAPI
from .views import ProductListAPI
from .views import ProductDetailAPI

app_name = 'product'
urlpatterns = [
    path('', TemplateView.as_view(template_name='product/product-list.html'),
         name='list'),
    path('<int:pk>/',
         TemplateView.as_view(template_name='product/product-detail.html'),
         name='detail'),
    path('list-api/', ProductListAPI.as_view(), name='list-api'),
    path('detail-api/<int:pk>/', ProductDetailAPI.as_view(),
         name='detail-api'),
    path('category-list-api/', CategoryListAPI.as_view(), name='category-api'),
]
