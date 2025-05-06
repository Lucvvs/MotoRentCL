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
    


class TipoUsuario(models.Model):
    codigo = models.IntegerField(unique=True)  # 0 = usuario, 1 = admin
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion


class UsuarioRegistro(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=12)
    nacionalidad = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=128)  # Encriptada
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.SET_NULL, null=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    

    def save(self, *args, **kwargs):
        # Encripta la contraseña antes de guardar (solo si no está encriptada aún)
        if not self.pk or not self.contrasena.startswith('pbkdf2_'):
            self.contrasena = make_password(self.contrasena)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.correo})"
    



class Contacto(models.Model):
    OPCIONES_ASUNTO = [
        ('reclamo',     'Reclamo'),
        ('sugerencia',  'Sugerencia'),
        ('consulta',    'Consulta'),
        ('otro',        'Otro'),
    ]

    nombre       = models.CharField(max_length=100)
    correo       = models.EmailField()
    celular      = models.CharField(max_length=15)
    asunto       = models.CharField(max_length=20, choices=OPCIONES_ASUNTO)
    mensaje = models.TextField()  
    fecha_envio  = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre} – {self.get_asunto_display()}"
    

ESTADOS_PAGO = [
    ('PENDIENTE', 'Pendiente'),
    ('PAGADO', 'Pagado'),
]

class Reserva(models.Model):
    motocicleta = models.ForeignKey(Motocicleta, on_delete=models.CASCADE)
    nombre_cliente = models.CharField(max_length=100)
    correo = models.EmailField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    creado = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(null=True, blank=True)  # Nuevo campo
    estado_pago = models.CharField(max_length=10, choices=ESTADOS_PAGO, default='PENDIENTE')

    def dias_reserva(self):
        return (self.fecha_fin - self.fecha_inicio).days + 1  # incluye ambos días

    def total_pagar(self):
        return self.dias_reserva() * self.motocicleta.precio

    def __str__(self):
        return f"Reserva de {self.motocicleta} por {self.nombre_cliente}"
    


class Pago(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
    ]
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, related_name='pago')
    estado = models.CharField(max_length=10, choices=ESTADOS, default='PENDIENTE')
    fecha_pago = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Pago de {self.reserva} - {self.estado}"

class AlteracionUsuario(models.Model):
    TIPOS = [
        ('modificacion', 'Modificación'),
        ('eliminacion',  'Eliminación'),
    ]
    usuario = models.ForeignKey(UsuarioRegistro, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.get_tipo_display()} - {self.fecha}"
    


