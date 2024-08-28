from django.urls import path
from . import views

urlpatterns = [
    path('api/orders/', views.OrderList.as_view(), name='api_order_list'),  # This should match the requested URL
    path('api/orders/<int:order_id>/', views.OrderDetail.as_view(), name='api_order_detail'),
]
