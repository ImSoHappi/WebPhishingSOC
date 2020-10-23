from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('client/', include('webphishingClient.urls')),
    path('api/', include('webphishingApi.urls')),
    path('auth/', include('webphishingAuth.urls')),
    path('admin/', admin.site.urls),
    path('', include('webphishingCore.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
