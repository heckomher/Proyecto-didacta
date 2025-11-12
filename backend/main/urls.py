from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (RegisterView, LoginView, logout_view, PlanificacionListCreateView, 
                   PlanificacionDetailView, enviar_a_validacion, validar_planificacion, 
                   EventoListCreateView, EventoDetailView, CalendarioListView, 
                   PlanificacionDetalleView, current_user, verificar_anio_academico,
                   verificar_configuracion_academica,
                   AnioAcademicoViewSet, PeriodoAcademicoViewSet, 
                   FeriadoViewSet, PeriodoVacacionesViewSet)

# Router para los ViewSets de configuración académica
router = DefaultRouter()
router.register(r'anios-academicos', AnioAcademicoViewSet, basename='anio-academico')
router.register(r'periodos-academicos', PeriodoAcademicoViewSet, basename='periodo-academico')
router.register(r'feriados', FeriadoViewSet, basename='feriado')
router.register(r'vacaciones', PeriodoVacacionesViewSet, basename='vacaciones')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/user/', current_user, name='current-user'),
    path('verificar-anio-academico/', verificar_anio_academico, name='verificar-anio-academico'),
    path('verificar-configuracion-academica/', verificar_configuracion_academica, name='verificar-configuracion-academica'),
    path('planificaciones/', PlanificacionListCreateView.as_view(), name='planificaciones'),
    path('planificaciones/<int:pk>/', PlanificacionDetailView.as_view(), name='planificacion-detail'),
    path('planificaciones/<int:pk>/enviar/', enviar_a_validacion, name='enviar-validacion'),
    path('planificaciones/<int:pk>/validar/', validar_planificacion, name='validar-planificacion'),
    path('planificaciones/<int:pk>/detalle/', PlanificacionDetalleView.as_view(), name='planificacion-detalle'),
    path('eventos/', EventoListCreateView.as_view(), name='eventos'),
    path('eventos/<int:pk>/', EventoDetailView.as_view(), name='evento-detail'),
    path('calendario/', CalendarioListView.as_view(), name='calendario'),
    # Incluir rutas del router
    path('', include(router.urls)),
]