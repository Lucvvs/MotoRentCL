from django.db.models.signals import post_migrate
from django.dispatch import receiver
from alquiler.models import TipoUsuario

@receiver(post_migrate)
def crear_tipos_usuario(sender, **kwargs):
    if sender.name == 'alquiler':
        TipoUsuario.objects.get_or_create(codigo=0, descripcion='Usuario')
        TipoUsuario.objects.get_or_create(codigo=1, descripcion='Administrador')