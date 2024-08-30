from django.urls import path
from .views import products_list, product_detail

urlpatterns = [
    path('', products_list, name='products-list'),
    path('<int:product_id>/', product_detail, name='product-detail'),
]
