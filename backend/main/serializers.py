from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import (Planificacion, PlanificacionDetalle, Evento, Calendario, AnioAcademico, 
                    PeriodoAcademico, Feriado, PeriodoVacaciones, Rol, Docente, EquipoDirectivo,
                    NivelEducativo, Asignatura, Curso, CursoAsignatura, ObjetivoAprendizaje,
                    RecursoPedagogico, PlanificacionAnual, PlanificacionUnidad, PlanificacionSemanal)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    full_name = serializers.SerializerMethodField()
    perfil_docente = serializers.SerializerMethodField()
    perfil_directivo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'nombre', 'apellido', 
                 'role', 'activo', 'full_name', 'perfil_docente', 'perfil_directivo',
                 'password', 'password2', 'is_superuser', 'is_staff')
        read_only_fields = ('is_superuser', 'is_staff', 'full_name', 'perfil_docente', 'perfil_directivo')
    
    def get_full_name(self, obj):
        return f"{obj.nombre} {obj.apellido}".strip() or obj.get_full_name()
    
    def get_perfil_docente(self, obj):
        if hasattr(obj, 'perfil_docente'):
            return {'rut': obj.perfil_docente.rut, 'especialidad': obj.perfil_docente.especialidad}
        return None
    
    def get_perfil_directivo(self, obj):
        if hasattr(obj, 'perfil_directivo'):
            return {'cargo': obj.perfil_directivo.cargo, 'departamento': obj.perfil_directivo.departamento}
        return None

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class PlanificacionSerializer(serializers.ModelSerializer):
    autor = serializers.StringRelatedField(read_only=True)
    anio_academico = serializers.PrimaryKeyRelatedField(queryset=AnioAcademico.objects.all(), required=False, allow_null=True)
    anio_academico_nombre = serializers.CharField(source='anio_academico.nombre', read_only=True)
    docente = serializers.PrimaryKeyRelatedField(queryset=Docente.objects.all(), required=False, allow_null=True)
    docente_nombre = serializers.SerializerMethodField()
    curso_nombre = serializers.CharField(source='curso.nombre_curso', read_only=True)
    asignatura_nombre = serializers.CharField(source='asignatura.nombre_asignatura', read_only=True)
    objetivos_count = serializers.SerializerMethodField()
    recursos_count = serializers.SerializerMethodField()

    class Meta:
        model = Planificacion
        fields = ['id', 'titulo', 'descripcion', 'tipo', 'estado', 'fecha_creacion', 'fecha_modificacion',
                 'fecha_inicio', 'fecha_fin', 'comentarios_validacion', 'anio_academico', 'anio_academico_nombre',
                 'docente', 'docente_nombre', 'curso', 'curso_nombre', 'asignatura', 'asignatura_nombre',
                 'objetivos_aprendizaje', 'objetivos_count', 'recursos_pedagogicos', 'recursos_count', 'autor']
    
    def get_docente_nombre(self, obj):
        if obj.docente:
            return f"{obj.docente.usuario.nombre} {obj.docente.usuario.apellido}".strip() or obj.docente.usuario.username
        return None
    
    def get_objetivos_count(self, obj):
        return obj.objetivos_aprendizaje.count()
    
    def get_recursos_count(self, obj):
        return obj.recursos_pedagogicos.count()
    
    def validate(self, data):
        """Validaciones adicionales a nivel de objeto"""
        # Si no hay año académico en los datos, verificar que hay uno activo
        if 'anio_academico' not in data or not data['anio_academico']:
            # Buscar año académico activo por defecto
            anio_activo = AnioAcademico.objects.filter(estado='ACTIVO').first()
            if not anio_activo:
                raise serializers.ValidationError(
                    "No hay año académico activo. Debe configurar un año académico antes de crear planificaciones."
                )
            data['anio_academico'] = anio_activo
        else:
            # Validar que el año académico no está cerrado
            if data['anio_academico'].estado == 'CERRADO':
                raise serializers.ValidationError(
                    "No se pueden crear planificaciones en un año académico cerrado"
                )
        
        return data

class PlanificacionDetalleSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    planificacion = serializers.CharField()
    objetivos = serializers.DictField()
    actividades = serializers.DictField()
    recursos = serializers.DictField()

    def create(self, validated_data):
        return PlanificacionDetalle(**validated_data).save()

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        return instance.save()

class EventoSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    titulo = serializers.CharField(max_length=200)
    descripcion = serializers.CharField()
    fecha_inicio = serializers.DateTimeField()
    fecha_fin = serializers.DateTimeField()
    creado_por = serializers.CharField(read_only=True)

    def create(self, validated_data):
        return Evento(**validated_data).save()

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        return instance.save()

class CalendarioSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField()
    eventos = serializers.ListField(child=serializers.CharField(), read_only=True)  # List of Evento IDs
    planificaciones_aprobadas = serializers.ListField(child=serializers.CharField(), read_only=True)  # List of Planificacion IDs

    def create(self, validated_data):
        return Calendario(**validated_data).save()

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        return instance.save()
class FeriadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feriado
        fields = ['id', 'nombre', 'fecha', 'anio_academico', 'tipo']

class PeriodoVacacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodoVacaciones
        fields = ['id', 'nombre', 'fecha_inicio', 'fecha_fin', 'anio_academico', 'tipo']

class PeriodoAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodoAcademico
        fields = ['id', 'nombre', 'numero', 'fecha_inicio', 'fecha_fin', 'anio_academico']

class AnioAcademicoSerializer(serializers.ModelSerializer):
    periodos = PeriodoAcademicoSerializer(many=True, read_only=True)
    feriados = FeriadoSerializer(many=True, read_only=True)
    vacaciones = PeriodoVacacionesSerializer(many=True, read_only=True)
    
    class Meta:
        model = AnioAcademico
        fields = ['id', 'nombre', 'fecha_inicio', 'fecha_fin', 'estado', 'activo', 'cerrado', 'tipo_periodo', 
                  'periodos', 'feriados', 'vacaciones', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'activo', 'cerrado']

# Serializers para nuevos modelos
class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre_rol', 'descripcion']

class DocenteSerializer(serializers.ModelSerializer):
    usuario_info = UserSerializer(source='usuario', read_only=True)
    usuario_nombre = serializers.SerializerMethodField()
    planificaciones_count = serializers.SerializerMethodField()
    asignaturas_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Docente
        fields = ['id', 'usuario', 'usuario_info', 'usuario_nombre', 'rut', 'especialidad', 'planificaciones_count', 'asignaturas_count']
    
    def get_usuario_nombre(self, obj):
        """Return full name from nombre/apellido or username as fallback"""
        nombre = obj.usuario.nombre or ""
        apellido = obj.usuario.apellido or ""
        
        if nombre and apellido:
            return f"{nombre} {apellido}"
        elif nombre:
            return nombre
        elif apellido:
            return apellido
        return obj.usuario.username
    
    def get_planificaciones_count(self, obj):
        # Count planificaciones through curso_asignatura relationship
        from django.db.models import Count
        return Planificacion.objects.filter(
            curso_asignatura__docente=obj
        ).count()
    
    def get_asignaturas_count(self, obj):
        # Count assigned asignaturas
        return obj.asignaturas_asignadas.count()

class EquipoDirectivoSerializer(serializers.ModelSerializer):
    usuario_info = UserSerializer(source='usuario', read_only=True)
    
    class Meta:
        model = EquipoDirectivo
        fields = ['id', 'usuario', 'usuario_info', 'cargo', 'departamento']

class NivelEducativoSerializer(serializers.ModelSerializer):
    cursos_count = serializers.SerializerMethodField()
    
    class Meta:
        model = NivelEducativo
        fields = ['id', 'nombre', 'descripcion', 'cursos_count']
    
    def get_cursos_count(self, obj):
        return obj.cursos.count()

class AsignaturaSerializer(serializers.ModelSerializer):
    cursos_count = serializers.SerializerMethodField()
    nivel_educativo_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = Asignatura
        fields = ['id', 'nombre_asignatura', 'descripcion', 'tipo', 'plan_asociado', 'nivel_educativo_nombre', 'cursos_count']
    
    def get_cursos_count(self, obj):
        return obj.cursos.count()
    
    def get_nivel_educativo_nombre(self, obj):
        # Extraer el nivel del nombre de la asignatura
        # Formato esperado: "Nombre - Nivel" o simplemente retornar un valor por defecto
        if 'Parvularia' in obj.nombre_asignatura:
            return 'Educación Parvularia'
        elif 'Básica' in obj.descripcion or 'Básico' in obj.descripcion:
            return 'Educación Básica'
        elif 'Media' in obj.descripcion:
            return 'Educación Media'
        elif 'Adultos' in obj.descripcion:
            return 'Educación de Adultos'
        return 'Sin clasificar'

class CursoAsignaturaSerializer(serializers.ModelSerializer):
    curso_nombre = serializers.CharField(source='curso.nombre_curso', read_only=True)
    asignatura_nombre = serializers.CharField(source='asignatura.nombre_asignatura', read_only=True)
    docente_info = DocenteSerializer(source='docente', read_only=True)
    docente_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = CursoAsignatura
        fields = ['id', 'curso', 'curso_nombre', 'asignatura', 'asignatura_nombre', 
                 'docente', 'docente_info', 'docente_nombre']
    
    def get_docente_nombre(self, obj):
        if obj.docente:
            return f"{obj.docente.usuario.nombre} {obj.docente.usuario.apellido}".strip() or obj.docente.usuario.username
        return None

class CursoSerializer(serializers.ModelSerializer):
    nivel_nombre = serializers.CharField(source='nivel.nombre', read_only=True)
    docente_jefe_info = DocenteSerializer(source='docente_jefe', read_only=True)
    asignaturas_info = AsignaturaSerializer(source='asignaturas', many=True, read_only=True)
    asignaturas_asignadas = CursoAsignaturaSerializer(many=True, read_only=True)
    planificaciones_count = serializers.SerializerMethodField()
    anio_academico_nombre = serializers.CharField(source='anio_academico.nombre', read_only=True)
    # Campo escribible explícito para asignaturas
    asignaturas = serializers.PrimaryKeyRelatedField(many=True, queryset=Asignatura.objects.all(), required=False)
    
    class Meta:
        model = Curso
        fields = ['id', 'nombre_curso', 'nivel', 'nivel_nombre', 'docente_jefe', 'docente_jefe_info',
                 'asignaturas', 'asignaturas_info', 'asignaturas_asignadas', 'planificaciones_count', 
                 'anio_academico', 'anio_academico_nombre', 'archivado', 'capacidad_maxima', 'paralelo',
                 'plan_diferenciado']
    
    def get_planificaciones_count(self, obj):
        return obj.planificaciones_legacy.count() + sum(ca.planificaciones.count() for ca in obj.asignaturas_asignadas.all())
    
    def create(self, validated_data):
        asignaturas = validated_data.pop('asignaturas', [])
        curso = Curso.objects.create(**validated_data)
        if asignaturas:
            curso.asignaturas.set(asignaturas)
        return curso
    
    def update(self, instance, validated_data):
        asignaturas = validated_data.pop('asignaturas', None)
        
        print(f"[SERIALIZER UPDATE] validated_data: {validated_data}")
        print(f"[SERIALIZER UPDATE] asignaturas extraídas: {asignaturas}")
        
        # Actualizar campos básicos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        print(f"[SERIALIZER UPDATE] Curso guardado, ahora actualizando asignaturas...")
        
        # Actualizar asignaturas si se proporcionaron
        if asignaturas is not None:
            print(f"[SERIALIZER UPDATE] Asignando {len(asignaturas)} asignaturas al curso")
            instance.asignaturas.set(asignaturas)
            print(f"[SERIALIZER UPDATE] Asignaturas después de set: {list(instance.asignaturas.all())}")
        
        return instance

class ObjetivoAprendizajeSerializer(serializers.ModelSerializer):
    nivel_educativo_nombre = serializers.CharField(source='nivel_educativo.nombre', read_only=True)
    curso_nombre = serializers.CharField(source='curso.nombre_curso', read_only=True)
    
    class Meta:
        model = ObjetivoAprendizaje
        fields = ['id', 'descripcion', 'nivel', 'nivel_educativo', 'nivel_educativo_nombre',
                 'curso', 'curso_nombre']

class RecursoPedagogicoSerializer(serializers.ModelSerializer):
    planificaciones_count = serializers.SerializerMethodField()
    
    class Meta:
        model = RecursoPedagogico
        fields = ['id', 'nombre', 'tipo', 'descripcion', 'planificaciones_count']
    
    def get_planificaciones_count(self, obj):
        return obj.planificaciones.count()

class PlanificacionAnualSerializer(serializers.ModelSerializer):
    docente_info = DocenteSerializer(source='docente', read_only=True)
    curso_info = CursoSerializer(source='curso', read_only=True)
    asignatura_info = AsignaturaSerializer(source='asignatura', read_only=True)
    anio_academico_nombre = serializers.CharField(source='anio_academico.nombre', read_only=True)
    unidades_count = serializers.SerializerMethodField()
    
    class Meta:
        model = PlanificacionAnual
        fields = ['id', 'titulo', 'descripcion', 'tipo', 'estado', 'fecha_creacion', 'fecha_modificacion',
                 'fecha_inicio', 'fecha_fin', 'anio_academico', 'anio_academico_nombre', 'docente', 'docente_info',
                 'curso', 'curso_info', 'asignatura', 'asignatura_info', 'meses_academicos', 'periodos_evaluacion',
                 'unidades_count', 'objetivos_aprendizaje', 'recursos_pedagogicos']
    
    def get_unidades_count(self, obj):
        return obj.unidades.count()

class PlanificacionUnidadSerializer(serializers.ModelSerializer):
    docente_info = DocenteSerializer(source='docente', read_only=True)
    curso_info = CursoSerializer(source='curso', read_only=True)
    asignatura_info = AsignaturaSerializer(source='asignatura', read_only=True)
    anio_academico_nombre = serializers.CharField(source='anio_academico.nombre', read_only=True)
    planificacion_anual_titulo = serializers.CharField(source='planificacion_anual.titulo', read_only=True)
    semanas_count = serializers.SerializerMethodField()
    
    class Meta:
        model = PlanificacionUnidad
        fields = ['id', 'titulo', 'descripcion', 'tipo', 'estado', 'fecha_creacion', 'fecha_modificacion',
                 'fecha_inicio', 'fecha_fin', 'anio_academico', 'anio_academico_nombre', 'docente', 'docente_info',
                 'curso', 'curso_info', 'asignatura', 'asignatura_info', 'numero_unidad', 'planificacion_anual',
                 'planificacion_anual_titulo', 'semanas_duracion', 'semanas_count', 'objetivos_aprendizaje', 'recursos_pedagogicos']
    
    def get_semanas_count(self, obj):
        return obj.semanas.count()

class PlanificacionSemanalSerializer(serializers.ModelSerializer):
    docente_info = DocenteSerializer(source='docente', read_only=True)
    curso_info = CursoSerializer(source='curso', read_only=True)
    asignatura_info = AsignaturaSerializer(source='asignatura', read_only=True)
    anio_academico_nombre = serializers.CharField(source='anio_academico.nombre', read_only=True)
    planificacion_unidad_titulo = serializers.CharField(source='planificacion_unidad.titulo', read_only=True)
    
    class Meta:
        model = PlanificacionSemanal
        fields = ['id', 'titulo', 'descripcion', 'tipo', 'estado', 'fecha_creacion', 'fecha_modificacion',
                 'fecha_inicio', 'fecha_fin', 'anio_academico', 'anio_academico_nombre', 'docente', 'docente_info',
                 'curso', 'curso_info', 'asignatura', 'asignatura_info', 'numero_semana', 'planificacion_unidad',
                 'planificacion_unidad_titulo', 'horas_academicas', 'objetivos_aprendizaje', 'recursos_pedagogicos']
