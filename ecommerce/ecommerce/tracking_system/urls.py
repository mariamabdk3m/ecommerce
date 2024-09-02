from django.urls import path
from .views import (
    user_orders_view, ExcelView, AddOrderView, EditOrderView, 
    DeleteOrderView, update_order_status
)

urlpatterns = [
    path('user-orders/', user_orders_view, name='user-orders'),
    path('admin/orders/', ExcelView.as_view(), name='excel-view'),
    path('admin/orders/add/', AddOrderView.as_view(), name='add-order'),
    path('admin/orders/edit/<int:order_id>/', EditOrderView.as_view(), name='edit-order'),
    path('admin/orders/delete/<int:order_id>/', DeleteOrderView.as_view(), name='delete-order'),
    path('admin/orders/update-status/<int:order_id>/', update_order_status, name='update-order-status'),
]
