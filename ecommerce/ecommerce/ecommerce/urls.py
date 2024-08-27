from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tracking_system/', include('tracking_system.urls')),  # Ensure this line is correctly included
]
