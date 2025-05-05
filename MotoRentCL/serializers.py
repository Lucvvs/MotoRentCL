from rest_framework import serializers
from alquiler.models import Motocicleta, Reserva, Contacto

class MotocicletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motocicleta
        fields = ['id', 'make', 'model', 'year', 'power', 'gearbox', 'cooling', 'precio', 'tipo']

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Reserva
        fields = ['id', 'motocicleta', 'nombre_cliente', 'correo',
                  'fecha_inicio', 'fecha_fin', 'total', 'creado']
        
class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = ['id', 'nombre', 'correo', 'celular', 'asunto', 'mensaje', 'fecha_envio']