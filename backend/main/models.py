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
    anio_academico = models.ForeignKey('main.AnioAcademico', on_delete=models.PROTECT, related_name='planificaciones')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='BORRADOR')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200)
    comentarios_validacion = models.TextField(blank=True, null=True)

    def __str__(self):
        anio_nombre = self.anio_academico.nombre if self.anio_academico else 'Sin año'
        return f"{self.titulo} - {self.autor.username} ({anio_nombre})"

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

class AnioAcademico(models.Model):
    """Configuración del año académico"""
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('ACTIVO', 'Activo'),
        ('CERRADO', 'Cerrado'),
    ]
    
    nombre = models.CharField(max_length=100, unique=True)  # e.g., "2025"
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='BORRADOR')
    
    # Campos legacy para compatibilidad - se derivarán del estado
    activo = models.BooleanField(default=False, editable=False)
    cerrado = models.BooleanField(default=False, editable=False)
    
    TIPO_PERIODO_CHOICES = [
        ('SEMESTRE', 'Semestral'),
        ('TRIMESTRE', 'Trimestral'),
        ('ANUAL', 'Anual'),
    ]
    tipo_periodo = models.CharField(max_length=10, choices=TIPO_PERIODO_CHOICES, default='SEMESTRE')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Año Académico'
        verbose_name_plural = 'Años Académicos'
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.nombre} ({self.get_estado_display()})"

    def save(self, *args, **kwargs):
        # Actualizar campos legacy basados en estado
        self.activo = (self.estado == 'ACTIVO')
        self.cerrado = (self.estado == 'CERRADO')
        
        # Solo un año académico puede estar activo a la vez
        if self.estado == 'ACTIVO':
            AnioAcademico.objects.filter(estado='ACTIVO').exclude(pk=self.pk).update(
                estado='BORRADOR', activo=False
            )
        
        super().save(*args, **kwargs)
        
    @property
    def is_borrador(self):
        return self.estado == 'BORRADOR'
        
    @property
    def is_activo(self):
        return self.estado == 'ACTIVO'
        
    @property
    def is_cerrado(self):
        return self.estado == 'CERRADO'

class PeriodoAcademico(models.Model):
    """Periodos dentro de un año académico (semestres, trimestres, etc.)"""
    anio_academico = models.ForeignKey(AnioAcademico, on_delete=models.CASCADE, related_name='periodos')
    nombre = models.CharField(max_length=100)  # e.g., "Primer Semestre", "Segundo Trimestre"
    numero = models.IntegerField()  # 1, 2, 3, etc.
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    class Meta:
        verbose_name = 'Periodo Académico'
        verbose_name_plural = 'Periodos Académicos'
        ordering = ['anio_academico', 'numero']
        unique_together = ['anio_academico', 'numero']

    def __str__(self):
        return f"{self.anio_academico.nombre} - {self.nombre}"

class Feriado(models.Model):
    """Feriados y días no laborables"""
    nombre = models.CharField(max_length=200)
    fecha = models.DateField()
    anio_academico = models.ForeignKey(AnioAcademico, on_delete=models.CASCADE, related_name='feriados', null=True, blank=True)
    
    TIPO_CHOICES = [
        ('FERIADO', 'Feriado Nacional'),
        ('INSTITUCIONAL', 'Día Institucional'),
        ('RECESO', 'Receso Académico'),
    ]
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='FERIADO')
    
    class Meta:
        verbose_name = 'Feriado'
        verbose_name_plural = 'Feriados'
        ordering = ['fecha']

    def __str__(self):
        return f"{self.nombre} - {self.fecha}"

class PeriodoVacaciones(models.Model):
    """Periodos de vacaciones"""
    nombre = models.CharField(max_length=200)  # e.g., "Vacaciones de Invierno 2025"
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    anio_academico = models.ForeignKey(AnioAcademico, on_delete=models.CASCADE, related_name='vacaciones')
    
    TIPO_CHOICES = [
        ('INVIERNO', 'Vacaciones de Invierno'),
        ('VERANO', 'Vacaciones de Verano'),
        ('RECESO', 'Receso Académico'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    
    class Meta:
        verbose_name = 'Periodo de Vacaciones'
        verbose_name_plural = 'Periodos de Vacaciones'
        ordering = ['fecha_inicio']

    def __str__(self):
        return f"{self.nombre} ({self.fecha_inicio} - {self.fecha_fin})"

# Create your models here.
