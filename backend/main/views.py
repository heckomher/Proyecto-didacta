from django.shortcuts import render
from django.http import Http404
from rest_framework import generics, status, serializers, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
from .serializers import (UserSerializer, LoginSerializer, PlanificacionSerializer, 
                         PlanificacionDetalleSerializer, EventoSerializer, CalendarioSerializer,
                         AnioAcademicoSerializer, PeriodoAcademicoSerializer, 
                         FeriadoSerializer, PeriodoVacacionesSerializer, RolSerializer,
                         DocenteSerializer, EquipoDirectivoSerializer, NivelEducativoSerializer,
                         AsignaturaSerializer, CursoSerializer, CursoAsignaturaSerializer,
                         ObjetivoAprendizajeSerializer,
                         RecursoPedagogicoSerializer, PlanificacionAnualSerializer,
                         PlanificacionUnidadSerializer, PlanificacionSemanalSerializer)
from .models import (Planificacion, PlanificacionDetalle, Evento, Calendario,
                    AnioAcademico, PeriodoAcademico, Feriado, PeriodoVacaciones,
                    Rol, Docente, EquipoDirectivo, NivelEducativo, Asignatura, Curso,
                    ObjetivoAprendizaje, RecursoPedagogico, PlanificacionAnual,
                    PlanificacionUnidad, PlanificacionSemanal)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        logger.error(f"[REGISTER] Datos recibidos: {request.data}")
        logger.error(f"[REGISTER] Usuario autenticado: {request.user.is_authenticated}, Role: {getattr(request.user, 'role', None)}")
        
        if User.objects.exists() and (not request.user.is_authenticated or (request.user.role not in ['UTP', 'EQUIPO_DIRECTIVO'] and not request.user.is_superuser)):
            logger.error("[REGISTER] Permiso denegado: Usuario no es UTP ni superusuario")
            return Response({"error": "Only UTP or superusers can register new users."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"[REGISTER] Errores de validación: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        logger.error(f"[REGISTER] Serializer válido, creando usuario...")
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

@api_view(['POST'])
@permission_classes([AllowAny])
def check_username(request):
    """
    Verifica si un nombre de usuario ya existe.
    Retorna { "exists": true/false }
    """
    username = request.data.get('username')
    if not username:
        return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    exists = User.objects.filter(username=username).exists()
    return Response({"exists": exists})

class PlanificacionListCreateView(generics.ListCreateAPIView):
    serializer_class = PlanificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Planificacion.objects.select_related('anio_academico', 'autor')
        if self.request.user.role in ['UTP', 'EQUIPO_DIRECTIVO']:
            return queryset
        return queryset.filter(autor=self.request.user)
    
    def create(self, request, *args, **kwargs):
        print(f"DEBUG - Request data: {request.data}")
        print(f"DEBUG - User: {request.user}, Role: {request.user.role}")
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(f"DEBUG - Serializer errors: {serializer.errors}")
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Si no se proporciona año académico, asignar el activo
        anio_academico = serializer.validated_data.get('anio_academico')
        if not anio_academico:
            anio_activo = AnioAcademico.objects.filter(estado='ACTIVO').first()
            if not anio_activo:
                raise serializers.ValidationError({
                    "anio_academico": "No hay año académico activo. Debe configurarse un año académico antes de crear planificaciones."
                })
            serializer.validated_data['anio_academico'] = anio_activo
        else:
            # Validar que no se puedan crear planificaciones en años cerrados
            if anio_academico.estado == 'CERRADO':
                raise serializers.ValidationError({
                    "anio_academico": "No se pueden crear planificaciones en un año académico cerrado."
                })
        
        # Si el usuario es docente y no se especifica docente, asignar automáticamente
        docente = serializer.validated_data.get('docente')
        if not docente and self.request.user.role == 'DOCENTE':
            try:
                docente_perfil = Docente.objects.get(usuario=self.request.user)
                serializer.validated_data['docente'] = docente_perfil
            except Docente.DoesNotExist:
                raise serializers.ValidationError({
                    "docente": "El usuario no tiene un perfil de docente asociado."
                })
        
        serializer.save(autor=self.request.user)

class PlanificacionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlanificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role in ['UTP', 'EQUIPO_DIRECTIVO']:
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
    if request.user.role not in ['UTP', 'EQUIPO_DIRECTIVO']:
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
        if self.request.user.role not in ['UTP', 'EQUIPO_DIRECTIVO']:
            raise serializers.ValidationError("Only UTP can create events.")
        serializer.save(creado_por=self.request.user.username)

class EventoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Evento.objects

    def perform_update(self, serializer):
        if self.request.user.role not in ['UTP', 'EQUIPO_DIRECTIVO']:
            raise serializers.ValidationError("Only UTP can update events.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role not in ['UTP', 'EQUIPO_DIRECTIVO']:
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
            # For POST/PUT on non-existent detalle, return None to trigger creation
            return None

    def update(self, request, *args, **kwargs):
        planificacion_id = self.kwargs.get('pk')
        
        # Verify planificacion ownership
        try:
            planificacion = Planificacion.objects.get(id=planificacion_id, autor=request.user)
        except Planificacion.DoesNotExist:
            return Response(
                {"error": "Planificación no encontrada o no autorizada."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Try to get existing detalle, or create new one
        detalle = PlanificacionDetalle.objects.filter(planificacion=planificacion_id).first()
        
        if detalle:
            # Update existing detalle
            serializer = self.get_serializer(detalle, data=request.data, partial=False)
        else:
            # Create new detalle
            serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save(planificacion=planificacion)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """Allow POST method for creating detalle"""
        return self.update(request, *args, **kwargs)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    """Lista todos los usuarios - solo para UTP y superuser"""
    if not (request.user.role in ['UTP', 'EQUIPO_DIRECTIVO'] or request.user.is_superuser):
        return Response({"detail": "No tiene permisos para ver usuarios"}, status=status.HTTP_403_FORBIDDEN)
    
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, pk):
    """Actualiza un usuario - solo para UTP, EQUIPO_DIRECTIVO y superuser"""
    if not (request.user.role in ['UTP', 'EQUIPO_DIRECTIVO'] or request.user.is_superuser):
        return Response({"detail": "No tiene permisos para editar usuarios"}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    # No permitir cambiar username
    data = request.data.copy()
    data.pop('username', None)
    data.pop('password', None)  # No cambiar password desde aquí
    
    serializer = UserSerializer(user, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def toggle_user_active(request, pk):
    """Activa/desactiva un usuario"""
    if not (request.user.role in ['UTP', 'EQUIPO_DIRECTIVO'] or request.user.is_superuser):
        return Response({"detail": "No tiene permisos"}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    # Si se está desactivando (no activando), verificar que no sea el último admin
    if user.activo:  # Se va a desactivar
        # Contar admins activos que NO sean este usuario
        from django.db.models import Q
        other_active_admins = User.objects.filter(
            activo=True
        ).filter(
            Q(role__in=['UTP', 'EQUIPO_DIRECTIVO']) | Q(is_superuser=True)
        ).exclude(pk=pk).count()
        
        if other_active_admins == 0:
            return Response({
                "detail": "No puede desactivar al último administrador activo del sistema"
            }, status=status.HTTP_400_BAD_REQUEST)
    
    user.activo = not user.activo
    user.save()
    return Response({"activo": user.activo, "message": f"Usuario {'activado' if user.activo else 'desactivado'}"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, pk):
    """Elimina un usuario"""
    if not (request.user.role in ['UTP', 'EQUIPO_DIRECTIVO'] or request.user.is_superuser):
        return Response({"detail": "No tiene permisos para eliminar usuarios"}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    # Verificar si es un admin (tiene permisos de gestión)
    is_admin = user.role in ['UTP', 'EQUIPO_DIRECTIVO'] or user.is_superuser
    
    if is_admin and user.activo:
        # Contar otros admins activos
        from django.db.models import Q
        other_active_admins = User.objects.filter(
            activo=True
        ).filter(
            Q(role__in=['UTP', 'EQUIPO_DIRECTIVO']) | Q(is_superuser=True)
        ).exclude(pk=pk).count()
        
        if other_active_admins == 0:
            return Response({
                "detail": "No puede eliminar al último administrador activo del sistema"
            }, status=status.HTTP_400_BAD_REQUEST)
    
    username = user.username
    user.delete()
    return Response({"message": f"Usuario '{username}' eliminado correctamente"})


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
        return request.user.role in ['UTP', 'EQUIPO_DIRECTIVO'] or request.user.is_superuser

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

# ViewSets para nuevos modelos
class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsUTPOrReadOnly]

class DocenteViewSet(viewsets.ModelViewSet):
    queryset = Docente.objects.select_related('usuario').all()
    serializer_class = DocenteSerializer
    permission_classes = [IsUTPOrReadOnly]
    
    def get_queryset(self):
        queryset = Docente.objects.select_related('usuario').all()
        if self.request.user.role == 'DOCENTE':
            # Los docentes solo pueden ver su propio perfil
            queryset = queryset.filter(usuario=self.request.user)
        return queryset

class EquipoDirectivoViewSet(viewsets.ModelViewSet):
    queryset = EquipoDirectivo.objects.select_related('usuario').all()
    serializer_class = EquipoDirectivoSerializer
    permission_classes = [IsUTPOrReadOnly]

class NivelEducativoViewSet(viewsets.ModelViewSet):
    queryset = NivelEducativo.objects.all()
    serializer_class = NivelEducativoSerializer
    permission_classes = [IsUTPOrReadOnly]

class AsignaturaViewSet(viewsets.ModelViewSet):
    queryset = Asignatura.objects.all()
    serializer_class = AsignaturaSerializer
    permission_classes = [IsUTPOrReadOnly]
    
    @action(detail=False, methods=['get'], url_path='sugeridas-por-nivel/(?P<nivel_nombre>[^/.]+)')
    def sugeridas_por_nivel(self, request, nivel_nombre=None):
        """
        Retorna asignaturas COMUNES sugeridas según el nivel educativo del currículum chileno.
        """
        # Mapeo de niveles a categorías de asignaturas
        nivel_mapping = {
            'Educación Parvularia': ['Educación Parvularia'],
            'Educación Básica': ['Educación Básica'],
            '1° Básico': ['Educación Básica'],
            '2° Básico': ['Educación Básica'],
            '3° Básico': ['Educación Básica'],
            '4° Básico': ['Educación Básica'],
            '5° Básico': ['Educación Básica'],
            '6° Básico': ['Educación Básica'],
            '7° Básico': ['Educación Básica'],
            '8° Básico': ['Educación Básica'],
            'Educación Media': ['Educación Media'],
            '1° Medio': ['Educación Media'],
            '2° Medio': ['Educación Media'],
            '3° Medio': ['Educación Media'],
            '4° Medio': ['Educación Media'],
            'Educación de Adultos': ['Educación de Adultos'],
        }
        
        # Buscar qué categorías aplican
        categorias = []
        for key, values in nivel_mapping.items():
            if nivel_nombre and key.lower() in nivel_nombre.lower():
                categorias = values
                break
        
        if not categorias:
            # Por defecto, mostrar todas las asignaturas comunes
            asignaturas = Asignatura.objects.filter(tipo='COMUN')
        else:
            # Filtrar asignaturas COMUNES por descripción que contenga el nivel
            query = Asignatura.objects.none()
            for categoria in categorias:
                query = query | Asignatura.objects.filter(
                    descripcion__icontains=categoria,
                    tipo='COMUN'
                )
            asignaturas = query.distinct()
        
        serializer = self.get_serializer(asignaturas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='electivos-por-plan/(?P<plan>[^/.]+)')
    def electivos_por_plan(self, request, plan=None):
        """
        Retorna asignaturas ELECTIVAS según el plan diferenciado.
        Planes válidos: CH (Científico-Humanista), TP (Técnico Profesional), ARTISTICO
        """
        if not plan:
            return Response({'error': 'Debe especificar un plan'}, status=400)
        
        plan = plan.upper()
        if plan not in ['CH', 'TP', 'ARTISTICO']:
            return Response({'error': f'Plan no válido: {plan}'}, status=400)
        
        electivos = Asignatura.objects.filter(tipo='ELECTIVO', plan_asociado=plan)
        serializer = self.get_serializer(electivos, many=True)
        return Response(serializer.data)

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.select_related('nivel', 'docente_jefe', 'anio_academico').prefetch_related('asignaturas', 'asignaturas_asignadas__docente__usuario', 'asignaturas_asignadas__asignatura').all()
    serializer_class = CursoSerializer
    permission_classes = [IsUTPOrReadOnly]
    
    def perform_update(self, serializer):
        print(f"[CURSO perform_update] Datos recibidos: {self.request.data}")
        asignaturas_ids = self.request.data.get('asignaturas', [])
        print(f"[CURSO perform_update] Asignaturas IDs: {asignaturas_ids}")
        
        # Guardar el curso (sin las asignaturas)
        curso = serializer.save()
        
        # Actualizar las asignaturas manualmente
        if asignaturas_ids is not None:
            from .models import Asignatura
            print(f"[CURSO perform_update] Actualizando asignaturas del curso {curso.id}...")
            curso.asignaturas.set(asignaturas_ids)
            print(f"[CURSO perform_update] Asignaturas actualizadas: {list(curso.asignaturas.values_list('id', flat=True))}")
    
    def update(self, request, *args, **kwargs):
        print(f"[CURSO UPDATE] Datos recibidos en update: {request.data}")
        print(f"[CURSO UPDATE] Asignaturas en update: {request.data.get('asignaturas', [])}")
        return super().update(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = Curso.objects.select_related('nivel', 'docente_jefe', 'anio_academico').prefetch_related('asignaturas', 'asignaturas_asignadas__docente__usuario', 'asignaturas_asignadas__asignatura').all()
        
        # Filtrar por nivel educativo
        nivel_id = self.request.query_params.get('nivel', None)
        if nivel_id:
            queryset = queryset.filter(nivel_id=nivel_id)
        
        # Filtrar por año académico
        anio_id = self.request.query_params.get('anio_academico', None)
        if anio_id:
            queryset = queryset.filter(anio_academico_id=anio_id)
        
        # Filtrar por estado archivado (por defecto muestra todos)
        archivado = self.request.query_params.get('archivado', None)
        if archivado is not None:
            queryset = queryset.filter(archivado=(archivado.lower() == 'true'))
        
        return queryset
    
    @action(detail=True, methods=['post'], url_path='asignar-docente')
    def asignar_docente(self, request, pk=None):
        """
        Asigna un docente a una asignatura específica del curso.
        Espera: { "asignatura_id": int, "docente_id": int o null }
        """
        from .models import CursoAsignatura
        
        logger.error(f"[ASIGNAR_DOCENTE] Datos recibidos: {request.data}")
        logger.error(f"[ASIGNAR_DOCENTE] Curso ID: {pk}")
        
        curso = self.get_object()
        asignatura_id = request.data.get('asignatura_id')
        docente_id = request.data.get('docente_id')
        
        logger.error(f"[ASIGNAR_DOCENTE] asignatura_id: {asignatura_id}, docente_id: {docente_id}")
        
        if not asignatura_id:
            logger.error("[ASIGNAR_DOCENTE] Error: asignatura_id es requerido")
            return Response({"error": "asignatura_id es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            curso_asignatura = CursoAsignatura.objects.get(curso=curso, asignatura_id=asignatura_id)
            logger.error(f"[ASIGNAR_DOCENTE] CursoAsignatura encontrado: {curso_asignatura.id}")
            
            if docente_id:
                curso_asignatura.docente_id = docente_id
            else:
                curso_asignatura.docente = None
            curso_asignatura.save()
            
            logger.error(f"[ASIGNAR_DOCENTE] Docente asignado exitosamente")
            return Response(CursoAsignaturaSerializer(curso_asignatura).data)
        except CursoAsignatura.DoesNotExist:
            logger.error(f"[ASIGNAR_DOCENTE] Error: La asignatura {asignatura_id} no está asociada al curso {curso.id}")
            return Response({"error": "La asignatura no está asociada al curso"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"[ASIGNAR_DOCENTE] Error inesperado: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ObjetivoAprendizajeViewSet(viewsets.ModelViewSet):
    queryset = ObjetivoAprendizaje.objects.select_related('nivel_educativo', 'curso').all()
    serializer_class = ObjetivoAprendizajeSerializer
    permission_classes = [IsUTPOrReadOnly]
    
    def get_queryset(self):
        queryset = ObjetivoAprendizaje.objects.select_related('nivel_educativo', 'curso').all()
        curso_id = self.request.query_params.get('curso', None)
        nivel_id = self.request.query_params.get('nivel_educativo', None)
        if curso_id:
            queryset = queryset.filter(curso_id=curso_id)
        if nivel_id:
            queryset = queryset.filter(nivel_educativo_id=nivel_id)
        return queryset

class RecursoPedagogicoViewSet(viewsets.ModelViewSet):
    queryset = RecursoPedagogico.objects.all()
    serializer_class = RecursoPedagogicoSerializer
    permission_classes = [IsUTPOrReadOnly]
    
    def get_queryset(self):
        queryset = RecursoPedagogico.objects.all()
        tipo = self.request.query_params.get('tipo', None)
        if tipo:
            queryset = queryset.filter(tipo__icontains=tipo)
        return queryset

# ViewSets para tipos específicos de planificación
class PlanificacionAnualViewSet(viewsets.ModelViewSet):
    serializer_class = PlanificacionAnualSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = PlanificacionAnual.objects.select_related(
            'anio_academico', 'docente__usuario', 'curso', 'asignatura'
        ).all()
        if self.request.user.role in ['UTP', 'EQUIPO_DIRECTIVO']:
            return queryset
        return queryset.filter(autor=self.request.user)

class PlanificacionUnidadViewSet(viewsets.ModelViewSet):
    serializer_class = PlanificacionUnidadSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = PlanificacionUnidad.objects.select_related(
            'anio_academico', 'docente__usuario', 'curso', 'asignatura', 'planificacion_anual'
        ).all()
        if self.request.user.role in ['UTP', 'EQUIPO_DIRECTIVO']:
            return queryset
        return queryset.filter(autor=self.request.user)

class PlanificacionSemanalViewSet(viewsets.ModelViewSet):
    serializer_class = PlanificacionSemanalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = PlanificacionSemanal.objects.select_related(
            'anio_academico', 'docente__usuario', 'curso', 'asignatura', 'planificacion_unidad'
        ).all()
        if self.request.user.role in ['UTP', 'EQUIPO_DIRECTIVO']:
            return queryset
        return queryset.filter(autor=self.request.user)
