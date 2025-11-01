from django.shortcuts import render
from rest_framework import generics, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, LoginSerializer, PlanificacionSerializer, PlanificacionDetalleSerializer, EventoSerializer, CalendarioSerializer
from .models import Planificacion, PlanificacionDetalle, Evento, Calendario

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        if User.objects.exists() and (not request.user.is_authenticated or request.user.role != 'UTP'):
            return Response({"error": "Only UTP can register new users."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    # For JWT, logout is handled on client side by removing token
    return Response({"message": "Logged out successfully."})

class PlanificacionListCreateView(generics.ListCreateAPIView):
    serializer_class = PlanificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'UTP':
            return Planificacion.objects.all()
        return Planificacion.objects.filter(autor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)

class PlanificacionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlanificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'UTP':
            return Planificacion.objects.all()
        return Planificacion.objects.filter(autor=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enviar_a_validacion(request, pk):
    try:
        planificacion = Planificacion.objects.get(pk=pk, autor=request.user)
        if planificacion.estado == 'BORRADOR':
            planificacion.estado = 'PENDIENTE'
            planificacion.save()
            return Response({"message": "Enviado a validación."})
        return Response({"error": "No se puede enviar."}, status=400)
    except Planificacion.DoesNotExist:
        return Response({"error": "Planificación no encontrada."}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validar_planificacion(request, pk):
    if request.user.role != 'UTP':
        return Response({"error": "No autorizado."}, status=403)
    try:
        planificacion = Planificacion.objects.get(pk=pk)
        accion = request.data.get('accion')
        comentarios = request.data.get('comentarios', '')
        if accion == 'aprobar':
            planificacion.estado = 'APROBADA'
        elif accion == 'rechazar':
            planificacion.estado = 'RECHAZADA'
        planificacion.comentarios_validacion = comentarios
        planificacion.save()
        return Response({"message": f"Planificación {accion}da."})
    except Planificacion.DoesNotExist:
        return Response({"error": "Planificación no encontrada."}, status=404)

class EventoListCreateView(generics.ListCreateAPIView):
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Evento.objects.all()

    def perform_create(self, serializer):
        if self.request.user.role != 'UTP':
            raise serializers.ValidationError("Only UTP can create events.")
        serializer.save(creado_por=self.request.user)

class EventoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Evento.objects.all()

    def perform_update(self, serializer):
        if self.request.user.role != 'UTP':
            raise serializers.ValidationError("Only UTP can update events.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role != 'UTP':
            raise serializers.ValidationError("Only UTP can delete events.")
        instance.delete()

class CalendarioListView(generics.ListAPIView):
    serializer_class = CalendarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Calendario.objects.all()

class PlanificacionDetalleView(generics.RetrieveUpdateAPIView):
    serializer_class = PlanificacionDetalleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PlanificacionDetalle.objects.filter(planificacion__autor=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
