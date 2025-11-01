from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Planificacion, PlanificacionDetalle, Evento, Calendario

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'password', 'password2')

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

    class Meta:
        model = Planificacion
        fields = '__all__'

class PlanificacionDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanificacionDetalle
        fields = '__all__'

class EventoSerializer(serializers.ModelSerializer):
    creado_por = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Evento
        fields = '__all__'

class CalendarioSerializer(serializers.ModelSerializer):
    eventos = EventoSerializer(many=True, read_only=True)
    planificaciones_aprobadas = PlanificacionSerializer(many=True, read_only=True)

    class Meta:
        model = Calendario
        fields = '__all__'