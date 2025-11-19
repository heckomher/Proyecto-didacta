from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import mongoengine
from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField, DictField

class User(AbstractUser):
    ROLE_CHOICES = [
        ('DOCENTE', 'Docente'),
        ('UTP', 'UTP'),
        ('EQUIPO_DIRECTIVO', 'Equipo Directivo'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='DOCENTE')
    nombre = models.CharField(max_length=100, blank=True)
    apellido = models.CharField(max_length=100, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        full_name = f"{self.nombre} {self.apellido}".strip()
        return f"{full_name or self.username} ({self.role})"

    def login(self):
        """Método para lógica de login si es necesario en un futuro"""
        pass
    
    def logout(self):
        """Método para lógica de logout si es necesario en un futuro"""
        pass

class Rol(models.Model):
    """Roles del sistema según diagrama ER"""
    nombre_rol = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
    
    def __str__(self):
        return self.nombre_rol

class Docente(models.Model):
    """Perfil de Docente según diagrama de clases"""
    usuario = models.OneToOneField('User', on_delete=models.CASCADE, related_name='perfil_docente')
    rut = models.CharField(max_length=12, unique=True)
    especialidad = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.especialidad}"
    
    def crear_planificacion(self):
        """Crear nueva planificación"""
        pass
    
    def editar_planificacion(self, planificacion_id):
        """Editar planificación existente"""
        pass
    
    def visualizar_planificacion(self, planificacion_id):
        """Visualizar planificación"""
        pass
    
    def reprogramar_actividad(self, actividad_id):
        """Reprogramar actividad"""
        pass
    
    def registrar_cumplimiento_objetivos(self, objetivo_id, cumplimiento):
        """Registrar cumplimiento de objetivos"""
        pass

class EquipoDirectivo(models.Model):
    """Perfil de Equipo Directivo según diagrama de clases"""
    usuario = models.OneToOneField('User', on_delete=models.CASCADE, related_name='perfil_directivo')
    cargo = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'Equipo Directivo'
        verbose_name_plural = 'Equipo Directivo'
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.cargo}"
    
    def visualizar_reportes(self):
        """Visualizar reportes académicos"""
        pass
    
    def crear_usuario(self):
        """Crear nuevo usuario"""
        pass
    
    def gestionar_usuarios(self):
        """Gestionar usuarios del sistema"""
        pass

class NivelEducativo(models.Model):
    """Niveles educativos según diagrama de clases"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Nivel Educativo'
        verbose_name_plural = 'Niveles Educativos'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    def agregar(self):
        """Agregar nuevo nivel"""
        pass
    
    def modificar(self):
        """Modificar nivel existente"""
        pass
    
    def eliminar(self):
        """Eliminar nivel"""
        pass

class Asignatura(models.Model):
    """Asignaturas según diagrama ER"""
    nombre_asignatura = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'
        ordering = ['nombre_asignatura']
    
    def __str__(self):
        return self.nombre_asignatura

class Curso(models.Model):
    """Cursos según diagrama de clases y ER"""
    nombre_curso = models.CharField(max_length=100)
    nivel = models.ForeignKey('NivelEducativo', on_delete=models.CASCADE, related_name='cursos')
    docente_jefe = models.ForeignKey('Docente', on_delete=models.SET_NULL, null=True, blank=True, related_name='cursos_a_cargo')
    asignaturas = models.ManyToManyField('Asignatura', through='CursoAsignatura', related_name='cursos')
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['nivel', 'nombre_curso']
    
    def __str__(self):
        return f"{self.nivel.nombre} - {self.nombre_curso}"
    
    def agregar(self):
        """Agregar nuevo curso"""
        pass
    
    def modificar(self):
        """Modificar curso existente"""
        pass
    
    def eliminar(self):
        """Eliminar curso"""
        pass

class CursoAsignatura(models.Model):
    """Tabla intermedia entre Curso y Asignatura según diagrama ER"""
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE)
    asignatura = models.ForeignKey('Asignatura', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['curso', 'asignatura']
        verbose_name = 'Curso-Asignatura'
        verbose_name_plural = 'Cursos-Asignaturas'
    
    def __str__(self):
        return f"{self.curso.nombre_curso} - {self.asignatura.nombre_asignatura}"

class ObjetivoAprendizaje(models.Model):
    """Objetivos de aprendizaje según diagrama de clases"""
    descripcion = models.TextField()
    nivel = models.CharField(max_length=50)
    nivel_educativo = models.ForeignKey('NivelEducativo', on_delete=models.CASCADE, related_name='objetivos')
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, related_name='objetivos')
    
    class Meta:
        verbose_name = 'Objetivo de Aprendizaje'
        verbose_name_plural = 'Objetivos de Aprendizaje'
    
    def __str__(self):
        return f"{self.curso} - {self.descripcion[:50]}..."
    
    def agregar(self):
        """Agregar nuevo objetivo"""
        pass
    
    def modificar(self):
        """Modificar objetivo existente"""
        pass
    
    def eliminar(self):
        """Eliminar objetivo"""
        pass

class RecursoPedagogico(models.Model):
    """Recursos pedagógicos según diagrama de clases"""
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Recurso Pedagógico'
        verbose_name_plural = 'Recursos Pedagógicos'
        ordering = ['tipo', 'nombre']
    
    def __str__(self):
        return f"{self.tipo} - {self.nombre}"
    
    def agregar(self):
        """Agregar nuevo recurso"""
        pass
    
    def modificar(self):
        """Modificar recurso existente"""
        pass
    
    def eliminar(self):
        """Eliminar recurso"""
        pass

class Planificacion(models.Model):
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('PENDIENTE', 'Pendiente'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada'),
    ]
    TIPO_CHOICES = [
        ('ANUAL', 'Planificación Anual'),
        ('UNIDAD', 'Planificación de Unidad'),
        ('SEMANAL', 'Planificación Semanal'),
    ]
    
    # Campos básicos
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='BORRADOR')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    comentarios_validacion = models.TextField(blank=True, null=True)
    
    # Relaciones obligatorias según diagrama de clases
    anio_academico = models.ForeignKey('AnioAcademico', on_delete=models.CASCADE, related_name='planificaciones')
    docente = models.ForeignKey('Docente', on_delete=models.CASCADE, related_name='planificaciones', null=True, blank=True)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, related_name='planificaciones', null=True, blank=True)
    asignatura = models.ForeignKey('Asignatura', on_delete=models.CASCADE, related_name='planificaciones', null=True, blank=True)
    
    # Relaciones con objetivos y recursos
    objetivos_aprendizaje = models.ManyToManyField('ObjetivoAprendizaje', blank=True, related_name='planificaciones')
    recursos_pedagogicos = models.ManyToManyField('RecursoPedagogico', blank=True, related_name='planificaciones')
    
    # Campo legacy para compatibilidad
    autor = models.ForeignKey('User', on_delete=models.CASCADE, related_name='planificaciones_creadas')
    
    class Meta:
        verbose_name = 'Planificación'
        verbose_name_plural = 'Planificaciones'
        ordering = ['-fecha_creacion']
        # unique_together = ['anio_academico', 'docente', 'curso', 'asignatura', 'tipo']  # Temporalmente deshabilitado para migración
    
    def __str__(self):
        return f"{self.titulo} - {self.curso} - {self.anio_academico}"
    
    def clean(self):
        super().clean()
        if not self.anio_academico:
            raise ValidationError('La planificación debe tener un año académico asignado.')
        if self.anio_academico.estado == 'CERRADO':
            raise ValidationError('No se puede crear planificaciones para años académicos cerrados.')
        if self.docente and self.autor and self.docente.usuario != self.autor:
            raise ValidationError('El docente asignado debe coincidir con el autor de la planificación.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def generar(self):
        """Generar planificación según diagrama de clases"""
        pass
    
    def editar(self):
        """Editar planificación existente"""
        pass
    
    def eliminar(self):
        """Eliminar planificación"""
        pass
    
    def listar(self):
        """Listar planificaciones"""
        pass

class PlanificacionDetalle(Document):
    planificacion = StringField(required=True)  # Planificacion ID
    objetivos = mongoengine.DictField()  # JSON-like
    actividades = mongoengine.DictField()
    recursos = mongoengine.DictField()

    meta = {'collection': 'planificacion_detalles'}

    def __str__(self):
        return f"Detalle de {self.planificacion}"

# Modelos de herencia según diagrama de clases
class PlanificacionAnual(Planificacion):
    """Planificación Anual - Hereda de Planificación"""
    meses_academicos = models.IntegerField(default=12)
    periodos_evaluacion = models.IntegerField(default=4)
    
    class Meta:
        verbose_name = 'Planificación Anual'
        verbose_name_plural = 'Planificaciones Anuales'
    
    def save(self, *args, **kwargs):
        self.tipo = 'ANUAL'
        super().save(*args, **kwargs)
    
    def planificar_anio(self):
        """Método específico para planificación anual"""
        pass
    
    def distribuir_contenidos(self):
        """Distribuir contenidos a lo largo del año"""
        pass

class PlanificacionUnidad(Planificacion):
    """Planificación de Unidad - Hereda de Planificación"""
    numero_unidad = models.IntegerField()
    planificacion_anual = models.ForeignKey(
        'PlanificacionAnual', 
        on_delete=models.CASCADE, 
        related_name='unidades',
        null=True, blank=True
    )
    semanas_duracion = models.IntegerField(default=4)
    
    class Meta:
        verbose_name = 'Planificación de Unidad'
        verbose_name_plural = 'Planificaciones de Unidad'
        ordering = ['numero_unidad']
    
    def save(self, *args, **kwargs):
        self.tipo = 'UNIDAD'
        super().save(*args, **kwargs)
    
    def planificar_unidad(self):
        """Método específico para planificación de unidad"""
        pass
    
    def secuenciar_contenidos(self):
        """Secuenciar contenidos de la unidad"""
        pass

class PlanificacionSemanal(Planificacion):
    """Planificación Semanal - Hereda de Planificación"""
    numero_semana = models.IntegerField()
    planificacion_unidad = models.ForeignKey(
        'PlanificacionUnidad', 
        on_delete=models.CASCADE, 
        related_name='semanas',
        null=True, blank=True
    )
    horas_academicas = models.IntegerField(default=45)
    
    class Meta:
        verbose_name = 'Planificación Semanal'
        verbose_name_plural = 'Planificaciones Semanales'
        ordering = ['numero_semana']
    
    def save(self, *args, **kwargs):
        self.tipo = 'SEMANAL'
        super().save(*args, **kwargs)
    
    def planificar_semana(self):
        """Método específico para planificación semanal"""
        pass
    
    def programar_actividades(self):
        """Programar actividades semanales"""
        pass

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
