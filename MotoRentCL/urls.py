from django.contrib import admin
from django.urls import path, include  
from . import api_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('alquiler.urls')),
    path('motos/',    api_views.lista_motos,    name='api-lista-motos'),
    path('reservas/', api_views.lista_reservas, name='api-lista-reservas'),
]