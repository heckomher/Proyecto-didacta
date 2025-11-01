from django.db import models
from django.contrib.auth.models import AbstractUser
import mongoengine
from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField

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

class PlanificacionDetalle(Document):
    planificacion = StringField(required=True)  # Planificacion ID
    objetivos = mongoengine.DictField()  # JSON-like
    actividades = mongoengine.DictField()
    recursos = mongoengine.DictField()

    meta = {'collection': 'planificacion_detalles'}

    def __str__(self):
        return f"Detalle de {self.planificacion}"

class Evento(Document):
    titulo = StringField(max_length=200, required=True)
    descripcion = StringField()
    fecha_inicio = DateTimeField(required=True)
    fecha_fin = DateTimeField(required=True)
    creado_por = StringField(max_length=150, required=True)  # Username

    meta = {'collection': 'eventos'}

    def __str__(self):
        return self.titulo

class Calendario(Document):
    nombre = StringField(max_length=100, required=True)
    descripcion = StringField()
    eventos = ListField(ReferenceField(Evento))
    planificaciones_aprobadas = ListField(StringField())  # Planificacion IDs

    meta = {'collection': 'calendarios'}

    def __str__(self):
        return self.nombre

# Create your models here.
