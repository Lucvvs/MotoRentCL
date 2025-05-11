from django.urls import path
from .api_views import lista_motos, lista_reservas, lista_contactos

urlpatterns = [
    path('motos/',    lista_motos,    name='api-lista-motos'),
    path('reservas/', lista_reservas, name='api-lista-reservas'),
    path('contacto/', lista_contactos, name='api-lista-contactos'),
    path('token/', obtain_auth_token, name='obtener_token'),
]