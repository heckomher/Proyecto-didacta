from django.contrib import admin
from .models import User, Planificacion, AnioAcademico, PeriodoAcademico, Feriado, PeriodoVacaciones

class PeriodoAcademicoInline(admin.TabularInline):
    model = PeriodoAcademico
    extra = 1

class FeriadoInline(admin.TabularInline):
    model = Feriado
    extra = 1

class PeriodoVacacionesInline(admin.TabularInline):
    model = PeriodoVacaciones
    extra = 1

@admin.register(AnioAcademico)
class AnioAcademicoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha_inicio', 'fecha_fin', 'tipo_periodo', 'activo', 'cerrado']
    list_filter = ['activo', 'cerrado', 'tipo_periodo']
    search_fields = ['nombre']
    inlines = [PeriodoAcademicoInline, FeriadoInline, PeriodoVacacionesInline]
    
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'activo', 'cerrado', 'tipo_periodo')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Hacer todos los campos de solo lectura si el año está cerrado"""
        if obj and obj.cerrado:
            return [field.name for field in self.model._meta.fields]
        return []
    
    def has_delete_permission(self, request, obj=None):
        """No permitir eliminar años cerrados"""
        if obj and obj.cerrado:
            return False
        return super().has_delete_permission(request, obj)

@admin.register(PeriodoAcademico)
class PeriodoAcademicoAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'numero', 'fecha_inicio', 'fecha_fin']
    list_filter = ['anio_academico']
    search_fields = ['nombre', 'anio_academico__nombre']

@admin.register(Feriado)
class FeriadoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha', 'tipo', 'anio_academico']
    list_filter = ['tipo', 'anio_academico']
    search_fields = ['nombre']
    date_hierarchy = 'fecha'

@admin.register(PeriodoVacaciones)
class PeriodoVacacionesAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'fecha_inicio', 'fecha_fin', 'anio_academico']
    list_filter = ['tipo', 'anio_academico']
    search_fields = ['nombre']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_staff', 'is_superuser']
    list_filter = ['role', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name']

@admin.register(Planificacion)
class PlanificacionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'anio_academico', 'tipo', 'estado', 'fecha_inicio', 'fecha_fin']
    list_filter = ['estado', 'tipo', 'anio_academico']
    search_fields = ['titulo', 'autor__username']
    date_hierarchy = 'fecha_creacion'

# Register your models here.
