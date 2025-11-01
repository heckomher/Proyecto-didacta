from django.urls import path
from .views import RegisterView, LoginView, logout_view, PlanificacionListCreateView, PlanificacionDetailView, enviar_a_validacion, validar_planificacion, EventoListCreateView, EventoDetailView, CalendarioListView, PlanificacionDetalleView, current_user

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/user/', current_user, name='current-user'),
    path('planificaciones/', PlanificacionListCreateView.as_view(), name='planificaciones'),
    path('planificaciones/<int:pk>/', PlanificacionDetailView.as_view(), name='planificacion-detail'),
    path('planificaciones/<int:pk>/enviar/', enviar_a_validacion, name='enviar-validacion'),
    path('planificaciones/<int:pk>/validar/', validar_planificacion, name='validar-planificacion'),
    path('planificaciones/<int:pk>/detalle/', PlanificacionDetalleView.as_view(), name='planificacion-detalle'),
    path('eventos/', EventoListCreateView.as_view(), name='eventos'),
    path('eventos/<int:pk>/', EventoDetailView.as_view(), name='evento-detail'),
    path('calendario/', CalendarioListView.as_view(), name='calendario'),
]