from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tracking/', include('tracking_system.urls')),
    path('products/', include('products.urls')),
    path('mart/', include('mart.urls')), 
    path('', include('login.urls')), 
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
