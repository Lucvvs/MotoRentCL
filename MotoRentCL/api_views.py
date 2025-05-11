from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from alquiler.models import Motocicleta, Reserva, Contacto
from .serializers import MotocicletaSerializer, ReservaSerializer, ContactoSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def lista_motos(request):
    if request.method == 'GET':
        motos = Motocicleta.objects.all()
        serializer = MotocicletaSerializer(motos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MotocicletaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def lista_reservas(request):
    if request.method == 'GET':
        reservas = Reserva.objects.all()
        ser       = ReservaSerializer(reservas, many=True)
        return Response(ser.data)

    # POST
    ser = ReservaSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)
    return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def lista_contactos(request):
    if request.method == 'GET':
        contactos = Contacto.objects.all().order_by('-fecha_envio')
        serializer = ContactoSerializer(contactos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ContactoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
