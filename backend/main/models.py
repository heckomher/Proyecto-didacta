from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('DOCENTE', 'Docente'),
        ('UTP', 'UTP'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='DOCENTE')

    def __str__(self):
        return f"{self.username} ({self.role})"

class Planificacion(models.Model):
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('PENDIENTE', 'Pendiente'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada'),
    ]
    TIPO_CHOICES = [
        ('CURSO', 'Curso'),
        ('TALLER', 'Taller'),
        ('SEMINARIO', 'Seminario'),
    ]
    
    autor = models.ForeignKey('main.User', on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='BORRADOR')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200)
    comentarios_validacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.autor.username}"

class PlanificacionDetalle(models.Model):
    planificacion = models.OneToOneField(Planificacion, on_delete=models.CASCADE)
    objetivos = models.JSONField()
    actividades = models.JSONField()
    recursos = models.JSONField()

    def __str__(self):
        return f"Detalle de {self.planificacion.titulo}"

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    creado_por = models.ForeignKey('main.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Calendario(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    eventos = models.ManyToManyField(Evento)
    planificaciones_aprobadas = models.ManyToManyField(Planificacion)

    def __str__(self):
        return self.nombre

# Create your models here.
