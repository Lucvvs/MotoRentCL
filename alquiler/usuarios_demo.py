from django.utils import timezone
from django.contrib.auth.hashers import make_password
from alquiler.models import UsuarioRegistro, TipoUsuario

def crear_usuario_demo():
    if not TipoUsuario.objects.exists():
        TipoUsuario.objects.create(codigo=0, descripcion='usuario')
        TipoUsuario.objects.create(codigo=1, descripcion='admin')

    tipo_usuario = TipoUsuario.objects.get(codigo=0)

    if not UsuarioRegistro.objects.filter(correo='demo@email.com').exists():
        UsuarioRegistro.objects.create(
            nombre='Usuario Demo',
            correo='demo@email.com',
            telefono='123456789',
            nacionalidad='Chile',
            contrasena=make_password('123123aA'),
            tipo_usuario=tipo_usuario,
            fecha_registro=timezone.now()
        )
        print("✅ Usuario de prueba creado")
    else:
        print("⚠️ El usuario ya existe")