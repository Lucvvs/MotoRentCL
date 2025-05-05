from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class Motocicleta(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField(null=True, blank=True)
    power = models.CharField(max_length=100, null=True, blank=True)
    gearbox = models.CharField(max_length=100, null=True, blank=True)
    cooling = models.CharField(max_length=100, null=True, blank=True)
    precio = models.IntegerField(null=True, blank=True)
    tipo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"
    



class UsuarioRegistro(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=12)
    nacionalidad = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=128)  # Encriptada
    fecha_registro = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Encripta la contraseña antes de guardar (solo si no está encriptada aún)
        if not self.pk or not self.contrasena.startswith('pbkdf2_'):
            self.contrasena = make_password(self.contrasena)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.correo})"