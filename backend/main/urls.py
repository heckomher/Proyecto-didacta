from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (RegisterView, LoginView, logout_view, check_username, PlanificacionListCreateView, 
                   PlanificacionDetailView, enviar_a_validacion, validar_planificacion, 
                   EventoListCreateView, EventoDetailView, CalendarioListView, 
                   PlanificacionDetalleView, current_user, list_users, update_user, toggle_user_active, delete_user,
                   verificar_anio_academico,
                   verificar_configuracion_academica,
                   AnioAcademicoViewSet, PeriodoAcademicoViewSet, 
                   FeriadoViewSet, PeriodoVacacionesViewSet,
                   RolViewSet, DocenteViewSet, EquipoDirectivoViewSet,
                   NivelEducativoViewSet, AsignaturaViewSet, CursoViewSet,
                   ObjetivoAprendizajeViewSet, RecursoPedagogicoViewSet,
                   PlanificacionAnualViewSet, PlanificacionUnidadViewSet, PlanificacionSemanalViewSet)

# Curriculum views (MongoDB)
from .curriculum_views import (
    UnidadesCurricularesView, UnidadDetalleView, OAsPorNivelAsignaturaView,
    CodigosCurriculumView, OATsView, HabilidadesPorNivelAsignaturaView, 
    ActitudesPorAsignaturaView
)

# Router para los ViewSets
router = DefaultRouter()
# Configuración académica
router.register(r'anios-academicos', AnioAcademicoViewSet, basename='anio-academico')
router.register(r'periodos-academicos', PeriodoAcademicoViewSet, basename='periodo-academico')
router.register(r'feriados', FeriadoViewSet, basename='feriado')
router.register(r'vacaciones', PeriodoVacacionesViewSet, basename='vacaciones')
# Gestión de usuarios y roles
router.register(r'roles', RolViewSet, basename='rol')
router.register(r'docentes', DocenteViewSet, basename='docente')
router.register(r'equipo-directivo', EquipoDirectivoViewSet, basename='equipo-directivo')
# Estructura académica
router.register(r'niveles-educativos', NivelEducativoViewSet, basename='nivel-educativo')
router.register(r'asignaturas', AsignaturaViewSet, basename='asignatura')
router.register(r'cursos', CursoViewSet, basename='curso')
router.register(r'objetivos-aprendizaje', ObjetivoAprendizajeViewSet, basename='objetivo-aprendizaje')
router.register(r'recursos-pedagogicos', RecursoPedagogicoViewSet, basename='recurso-pedagogico')
# Planificaciones específicas
router.register(r'planificaciones-anuales', PlanificacionAnualViewSet, basename='planificacion-anual')
router.register(r'planificaciones-unidad', PlanificacionUnidadViewSet, basename='planificacion-unidad')
router.register(r'planificaciones-semanales', PlanificacionSemanalViewSet, basename='planificacion-semanal')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/check-username/', check_username, name='check-username'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/user/', current_user, name='current-user'),
    path('auth/users/', list_users, name='list-users'),
    path('auth/users/<int:pk>/', update_user, name='update-user'),
    path('auth/users/<int:pk>/toggle-active/', toggle_user_active, name='toggle-user-active'),
    path('auth/users/<int:pk>/delete/', delete_user, name='delete-user'),
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
    
    # Curriculum Nacional (MongoDB)
    path('curriculum/codigos/', CodigosCurriculumView.as_view(), name='curriculum-codigos'),
    path('curriculum/unidades/<str:nivel>/<str:asignatura>/', UnidadesCurricularesView.as_view(), name='curriculum-unidades'),
    path('curriculum/unidad/<str:codigo>/', UnidadDetalleView.as_view(), name='curriculum-unidad-detalle'),
    path('curriculum/oa/<str:nivel>/<str:asignatura>/', OAsPorNivelAsignaturaView.as_view(), name='curriculum-oa'),
    path('curriculum/oat/', OATsView.as_view(), name='curriculum-oat'),
    path('curriculum/habilidades/<str:nivel>/<str:asignatura>/', HabilidadesPorNivelAsignaturaView.as_view(), name='curriculum-habilidades'),
    path('curriculum/actitudes/<str:asignatura>/', ActitudesPorAsignaturaView.as_view(), name='curriculum-actitudes'),
    
    # Incluir rutas del router
    path('', include(router.urls)),
]