from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
import mongoengine
from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField, DictField
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Force default role for superusers
        extra_fields.setdefault('role', 'EQUIPO_DIRECTIVO')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


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

    objects = CustomUserManager()

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

# Choices para tipos de asignatura
TIPO_ASIGNATURA_CHOICES = [
    ('COMUN', 'Común'),
    ('ELECTIVO', 'Electivo'),
]

# Choices para planes diferenciados de Educación Media
PLAN_DIFERENCIADO_CHOICES = [
    ('', 'No aplica'),
    ('MEDIO_1_2', '1°-2° Medio'),
    ('CH', 'Científico-Humanista'),
    ('TP', 'Técnico Profesional'),
    ('ARTISTICO', 'Artístico'),
]

class Asignatura(models.Model):
    """Asignaturas según diagrama ER"""
    nombre_asignatura = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_ASIGNATURA_CHOICES, default='COMUN')
    plan_asociado = models.CharField(max_length=20, blank=True, default='', help_text='Plan al que pertenece (solo para electivos)')
    
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
    anio_academico = models.ForeignKey('AnioAcademico', on_delete=models.CASCADE, related_name='cursos', null=True)
    archivado = models.BooleanField(default=False, editable=False)
    capacidad_maxima = models.IntegerField(default=40)
    paralelo = models.CharField(max_length=10, blank=True)
    plan_diferenciado = models.CharField(
        max_length=20, 
        choices=PLAN_DIFERENCIADO_CHOICES, 
        blank=True, 
        default='',
        help_text='Plan diferenciado para Educación Media (3°-4°)'
    )
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['-anio_academico__fecha_inicio', 'nivel', 'nombre_curso']
    
    def __str__(self):
        return f"{self.nivel.nombre} - {self.nombre_curso} ({self.anio_academico.nombre})"
    
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
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, related_name='asignaturas_asignadas')
    asignatura = models.ForeignKey('Asignatura', on_delete=models.CASCADE)
    docente = models.ForeignKey('Docente', on_delete=models.SET_NULL, null=True, blank=True, related_name='asignaturas_asignadas')
    
    class Meta:
        unique_together = ['curso', 'asignatura']
        verbose_name = 'Curso-Asignatura'
        verbose_name_plural = 'Cursos-Asignaturas'
    
    def __str__(self):
        docente_info = f" - {self.docente.usuario.get_full_name()}" if self.docente else " (sin docente)"
        return f"{self.curso.nombre_curso}: {self.asignatura.nombre_asignatura}{docente_info}"
    
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
    # En lugar de relacionar con docente directamente, se relaciona con CursoAsignatura
    # Esto permite que la planificación permanezca aunque cambie el docente
    curso_asignatura = models.ForeignKey('CursoAsignatura', on_delete=models.CASCADE, related_name='planificaciones', null=True, blank=True)
    
    # Campos legacy - mantener por compatibilidad pero deprecados
    docente = models.ForeignKey('Docente', on_delete=models.SET_NULL, related_name='planificaciones_legacy', null=True, blank=True)
    curso = models.ForeignKey('Curso', on_delete=models.SET_NULL, related_name='planificaciones_legacy', null=True, blank=True)
    asignatura = models.ForeignKey('Asignatura', on_delete=models.SET_NULL, related_name='planificaciones_legacy', null=True, blank=True)
    
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
        null=True, blank=True  # Nullable en BD, pero requerido en serializer
    )
    semanas_duracion = models.IntegerField(default=4)
    
    class Meta:
        verbose_name = 'Planificación de Unidad'
        verbose_name_plural = 'Planificaciones de Unidad'
        ordering = ['numero_unidad']
    
    def save(self, *args, **kwargs):
        self.tipo = 'UNIDAD'
        # Heredar datos del padre para mantener normalización
        if self.planificacion_anual:
            self.curso = self.planificacion_anual.curso
            self.asignatura = self.planificacion_anual.asignatura
            self.docente = self.planificacion_anual.docente
            self.anio_academico = self.planificacion_anual.anio_academico
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
        null=True, blank=True  # Nullable en BD, pero requerido en serializer
    )
    horas_academicas = models.IntegerField(default=45)
    
    class Meta:
        verbose_name = 'Planificación Semanal'
        verbose_name_plural = 'Planificaciones Semanales'
        ordering = ['numero_semana']
    
    def save(self, *args, **kwargs):
        self.tipo = 'SEMANAL'
        # Heredar datos de la cadena de padres para mantener normalización
        if self.planificacion_unidad:
            self.curso = self.planificacion_unidad.curso
            self.asignatura = self.planificacion_unidad.asignatura
            self.docente = self.planificacion_unidad.docente
            self.anio_academico = self.planificacion_unidad.anio_academico
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


# Señales para archivar cursos automáticamente cuando se cierra un año académico
@receiver(post_save, sender=AnioAcademico)
def archivar_cursos_al_cerrar_anio(sender, instance, **kwargs):
    """Cuando un año académico se cierra, archiva todos sus cursos"""
    if instance.estado == 'CERRADO':
        Curso.objects.filter(anio_academico=instance, archivado=False).update(archivado=True)

# Signal para crear perfiles automáticamente cuando se crea un usuario
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """Crea automáticamente el perfil correspondiente según el rol del usuario"""
    if created:
        if instance.role == 'DOCENTE':
            # Verificar si ya existe un perfil de docente
            if not hasattr(instance, 'perfil_docente'):
                # Generar RUT temporal si no se proporciona
                rut_temp = f"pending-{instance.id}"
                Docente.objects.create(
                    usuario=instance,
                    rut=rut_temp,
                    especialidad="Sin especialidad"
                )
        elif instance.role == 'EQUIPO_DIRECTIVO':
            # Verificar si ya existe un perfil directivo
            if not hasattr(instance, 'perfil_directivo'):
                EquipoDirectivo.objects.create(
                    usuario=instance,
                    cargo="Sin cargo",
                    departamento="Sin departamento"
                )

# Create your models here.
