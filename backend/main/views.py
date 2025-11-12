from django.shortcuts import render
from django.http import Http404
from rest_framework import generics, status, serializers, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .serializers import (UserSerializer, LoginSerializer, PlanificacionSerializer, 
                         PlanificacionDetalleSerializer, EventoSerializer, CalendarioSerializer,
                         AnioAcademicoSerializer, PeriodoAcademicoSerializer, 
                         FeriadoSerializer, PeriodoVacacionesSerializer)
from .models import (Planificacion, PlanificacionDetalle, Evento, Calendario,
                    AnioAcademico, PeriodoAcademico, Feriado, PeriodoVacaciones)

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
    # Use SimpleJWT's serializer to return access/refresh tokens
    serializer_class = TokenObtainPairSerializer
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
        queryset = Planificacion.objects.select_related('anio_academico', 'autor')
        if self.request.user.role == 'UTP':
            return queryset
        return queryset.filter(autor=self.request.user)

    def perform_create(self, serializer):
        # Si no se proporciona año académico, asignar el activo
        anio_academico = serializer.validated_data.get('anio_academico')
        if not anio_academico:
            anio_activo = AnioAcademico.objects.filter(estado='ACTIVO').first()
            if not anio_activo:
                raise serializers.ValidationError({
                    "anio_academico": "No hay año académico activo. Debe configurarse un año académico antes de crear planificaciones."
                })
            serializer.save(autor=self.request.user, anio_academico=anio_activo)
        else:
            # Validar que no se puedan crear planificaciones en años cerrados
            if anio_academico.estado == 'CERRADO':
                raise serializers.ValidationError({
                    "anio_academico": "No se pueden crear planificaciones en un año académico cerrado."
                })
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
        return Evento.objects

    def perform_create(self, serializer):
        if self.request.user.role != 'UTP':
            raise serializers.ValidationError("Only UTP can create events.")
        serializer.save(creado_por=self.request.user.username)

class EventoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Evento.objects

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
        return Calendario.objects

class PlanificacionDetalleView(generics.RetrieveUpdateAPIView):
    serializer_class = PlanificacionDetalleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PlanificacionDetalle.objects

    def get_object(self):
        planificacion_id = self.kwargs.get('pk')
        try:
            return PlanificacionDetalle.objects.get(planificacion=planificacion_id)
        except PlanificacionDetalle.DoesNotExist:
            raise Http404

    def perform_update(self, serializer):
        planificacion_id = self.kwargs.get('pk')
        # Ensure the user owns the planificacion
        try:
            planificacion = Planificacion.objects.get(id=planificacion_id, autor=self.request.user)
        except Planificacion.DoesNotExist:
            raise serializers.ValidationError("Planificación no encontrada o no autorizada.")
        serializer.save()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verificar_anio_academico(request):
    """Verifica si hay un año académico activo configurado"""
    anio_activo = AnioAcademico.objects.filter(activo=True).first()
    return Response({
        "tiene_anio_activo": anio_activo is not None,
        "anio_academico": AnioAcademicoSerializer(anio_activo).data if anio_activo else None
    })

# ViewSets para configuración académica
class IsUTPOrReadOnly(IsAuthenticated):
    """
    Permiso personalizado: UTP puede crear/editar/eliminar, otros solo pueden leer
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        # Métodos seguros (GET, HEAD, OPTIONS) permitidos para todos
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Métodos de escritura solo para UTP o superuser
        return request.user.role == 'UTP' or request.user.is_superuser

class AnioAcademicoViewSet(viewsets.ModelViewSet):
    queryset = AnioAcademico.objects.all()
    serializer_class = AnioAcademicoSerializer
    permission_classes = [IsUTPOrReadOnly]
    
    def perform_update(self, serializer):
        """Bloquear modificaciones en años cerrados"""
        if serializer.instance.is_cerrado:
            raise serializers.ValidationError("No se puede modificar un año académico cerrado")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Bloquear eliminación de años cerrados"""
        if instance.is_cerrado:
            raise serializers.ValidationError("No se puede eliminar un año académico cerrado")
        instance.delete()
    
    @action(detail=False, methods=['get'])
    def activo(self, request):
        """Obtiene el año académico activo"""
        anio_activo = AnioAcademico.objects.filter(estado='ACTIVO').first()
        if anio_activo:
            serializer = self.get_serializer(anio_activo)
            return Response(serializer.data)
        return Response({"detail": "No hay año académico activo"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def borradores(self, request):
        """Obtiene todos los años académicos en estado borrador"""
        borradores = AnioAcademico.objects.filter(estado='BORRADOR')
        serializer = self.get_serializer(borradores, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activar(self, request, pk=None):
        """Activar un año académico (solo si está en borrador)"""
        anio = self.get_object()
        if anio.estado != 'BORRADOR':
            return Response({"detail": "Solo se pueden activar años académicos en estado borrador"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        anio.estado = 'ACTIVO'
        anio.save()
        
        serializer = self.get_serializer(anio)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cerrar(self, request, pk=None):
        """Cerrar un año académico para que sea solo lectura (requiere confirmación)"""
        anio = self.get_object()
        if anio.estado == 'CERRADO':
            return Response({"detail": "El año académico ya está cerrado"}, status=status.HTTP_400_BAD_REQUEST)
        
        if anio.estado == 'BORRADOR':
            return Response({"detail": "No se puede cerrar un año académico en estado borrador. Debe activarlo primero"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Validar contraseña de confirmación
        password = request.data.get('password')
        if not password:
            return Response({"detail": "Se requiere confirmación con contraseña"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        if not request.user.check_password(password):
            return Response({"detail": "Contraseña incorrecta"}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        anio.estado = 'CERRADO'
        anio.save()
        
        serializer = self.get_serializer(anio)
        return Response(serializer.data)

class PeriodoAcademicoViewSet(viewsets.ModelViewSet):
    queryset = PeriodoAcademico.objects.all()
    serializer_class = PeriodoAcademicoSerializer
    permission_classes = [IsUTPOrReadOnly]
    
    def perform_create(self, serializer):
        """Bloquear creación en años cerrados"""
        anio_academico = serializer.validated_data.get('anio_academico')
        if anio_academico and anio_academico.is_cerrado:
            raise serializers.ValidationError("No se pueden agregar periodos a un año académico cerrado")
        serializer.save()
    
    def perform_update(self, serializer):
        """Bloquear modificaciones en años cerrados"""
        if serializer.instance.anio_academico.is_cerrado:
            raise serializers.ValidationError("No se pueden modificar periodos de un año académico cerrado")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Bloquear eliminación en años cerrados"""
        if instance.anio_academico.is_cerrado:
            raise serializers.ValidationError("No se pueden eliminar periodos de un año académico cerrado")
        instance.delete()
    
    def get_queryset(self):
        queryset = PeriodoAcademico.objects.all()
        anio_id = self.request.query_params.get('anio_academico', None)
        if anio_id:
            queryset = queryset.filter(anio_academico_id=anio_id)
        return queryset

class FeriadoViewSet(viewsets.ModelViewSet):
    queryset = Feriado.objects.all()
    serializer_class = FeriadoSerializer
    permission_classes = [IsUTPOrReadOnly]
    
    def perform_create(self, serializer):
        """Bloquear creación en años cerrados"""
        anio_academico = serializer.validated_data.get('anio_academico')
        if anio_academico and anio_academico.is_cerrado:
            raise serializers.ValidationError("No se pueden agregar feriados a un año académico cerrado")
        serializer.save()
    
    def perform_update(self, serializer):
        """Bloquear modificaciones en años cerrados"""
        if serializer.instance.anio_academico and serializer.instance.anio_academico.is_cerrado:
            raise serializers.ValidationError("No se pueden modificar feriados de un año académico cerrado")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Bloquear eliminación en años cerrados"""
        if instance.anio_academico and instance.anio_academico.is_cerrado:
            raise serializers.ValidationError("No se pueden eliminar feriados de un año académico cerrado")
        instance.delete()
    
    def get_queryset(self):
        queryset = Feriado.objects.all()
        anio_id = self.request.query_params.get('anio_academico', None)
        if anio_id:
            queryset = queryset.filter(anio_academico_id=anio_id)
        return queryset

class PeriodoVacacionesViewSet(viewsets.ModelViewSet):
    queryset = PeriodoVacaciones.objects.all()
    serializer_class = PeriodoVacacionesSerializer
    permission_classes = [IsUTPOrReadOnly]
    
    def perform_create(self, serializer):
        """Bloquear creación en años cerrados"""
        anio_academico = serializer.validated_data.get('anio_academico')
        if anio_academico and anio_academico.is_cerrado:
            raise serializers.ValidationError("No se pueden agregar vacaciones a un año académico cerrado")
        serializer.save()
    
    def perform_update(self, serializer):
        """Bloquear modificaciones en años cerrados"""
        if serializer.instance.anio_academico.is_cerrado:
            raise serializers.ValidationError("No se pueden modificar vacaciones de un año académico cerrado")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Bloquear eliminación en años cerrados"""
        if instance.anio_academico.is_cerrado:
            raise serializers.ValidationError("No se pueden eliminar vacaciones de un año académico cerrado")
        instance.delete()
    
    def get_queryset(self):
        queryset = PeriodoVacaciones.objects.all()
        anio_id = self.request.query_params.get('anio_academico', None)
        if anio_id:
            queryset = queryset.filter(anio_academico_id=anio_id)
        return queryset

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verificar_configuracion_academica(request):
    """
    Verificar si hay configuración académica válida para crear planificaciones
    """
    # Verificar si hay año académico activo
    anio_activo = AnioAcademico.objects.filter(estado='ACTIVO').first()
    
    if not anio_activo:
        return Response({
            'configurado': False,
            'mensaje': 'No hay año académico activo configurado',
            'accion_requerida': 'configurar_anio_academico'
        })
    
    return Response({
        'configurado': True,
        'anio_academico': {
            'id': anio_activo.id,
            'nombre': anio_activo.nombre,
            'estado': anio_activo.estado,
            'fecha_inicio': anio_activo.fecha_inicio,
            'fecha_fin': anio_activo.fecha_fin
        }
    })
