from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from ecommerce import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('compte/', include('compte.urls')),
    path('', include('boutique.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
