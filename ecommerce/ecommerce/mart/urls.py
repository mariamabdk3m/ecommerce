from django.urls import path
from . import views

urlpatterns = [
    path('', views.mart, name='mart'),
    path('cart/', views.cart, name='cart'),
]
