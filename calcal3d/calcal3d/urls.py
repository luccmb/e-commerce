from django.contrib import admin
from django.urls import path, include  # Importa include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tiendacalcal.urls')),  # Incluye las URLs de tu aplicación
]

