from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Planificacion, PlanificacionDetalle, Evento, Calendario, AnioAcademico, PeriodoAcademico, Feriado, PeriodoVacaciones

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'password', 'password2', 'is_superuser', 'is_staff')
        read_only_fields = ('is_superuser', 'is_staff')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class PlanificacionSerializer(serializers.ModelSerializer):
    autor = serializers.StringRelatedField(read_only=True)
    anio_academico_nombre = serializers.CharField(source='anio_academico.nombre', read_only=True)

    class Meta:
        model = Planificacion
        fields = '__all__'
    
    def validate_anio_academico(self, value):
        """Validar que el año académico existe y no está cerrado"""
        if not value:
            raise serializers.ValidationError("El año académico es obligatorio")
        
        if value.is_cerrado:
            raise serializers.ValidationError("No se pueden crear planificaciones en un año académico cerrado")
        
        return value
    
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
        fields = ['id', 'nombre', 'numero', 'fecha_inicio', 'fecha_fin']

class AnioAcademicoSerializer(serializers.ModelSerializer):
    periodos = PeriodoAcademicoSerializer(many=True, read_only=True)
    feriados = FeriadoSerializer(many=True, read_only=True)
    vacaciones = PeriodoVacacionesSerializer(many=True, read_only=True)
    
    class Meta:
        model = AnioAcademico
        fields = ['id', 'nombre', 'fecha_inicio', 'fecha_fin', 'estado', 'activo', 'cerrado', 'tipo_periodo', 
                  'periodos', 'feriados', 'vacaciones', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'activo', 'cerrado']
