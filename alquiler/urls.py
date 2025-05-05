from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('contacto/', views.contacto_usuario, name='contacto'),
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('arrendar/', views.arrendar, name='arrendar'),
    path('logout/', views.logout_usuario, name='logout'),
    path('reserva/<int:moto_id>/', views.reserva_moto, name='reserva'),
    path('api/', include('MotoRentCL.api_urls')),
    
]