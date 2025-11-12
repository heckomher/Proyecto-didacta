from django.core.management.base import BaseCommand
from main.models import Planificacion, AnioAcademico
from django.utils import timezone
from datetime import datetime

class Command(BaseCommand):
    help = 'Migra todas las planificaciones existentes para tener un año académico asociado'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Ejecutar en modo de prueba sin realizar cambios',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Contar planificaciones sin año académico
        planificaciones_sin_anio = Planificacion.objects.filter(anio_academico__isnull=True)
        total = planificaciones_sin_anio.count()
        
        if total == 0:
            self.stdout.write(
                self.style.SUCCESS('✓ Todas las planificaciones ya tienen año académico asignado')
            )
            return
        
        self.stdout.write(f'📊 Planificaciones sin año académico: {total}')
        
        # Buscar año académico activo o crear uno por defecto
        anio_activo = AnioAcademico.objects.filter(estado='ACTIVO').first()
        
        if not anio_activo:
            # Crear un año académico por defecto
            current_year = datetime.now().year
            anio_name = f"Año Académico {current_year}"
            
            if not dry_run:
                anio_activo = AnioAcademico.objects.create(
                    nombre=anio_name,
                    fecha_inicio=datetime(current_year, 3, 1),  # Marzo
                    fecha_fin=datetime(current_year + 1, 2, 28),  # Febrero del año siguiente
                    estado='ACTIVO',
                    tipo_periodo='Semestre'
                )
                self.stdout.write(
                    self.style.WARNING(f'📅 Creado año académico por defecto: {anio_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'[DRY-RUN] Se crearía año académico: {anio_name}')
                )
                # Para dry-run, crear un objeto temporal
                anio_activo = AnioAcademico(
                    nombre=anio_name,
                    fecha_inicio=datetime(current_year, 3, 1),
                    fecha_fin=datetime(current_year + 1, 2, 28),
                    estado='ACTIVO',
                    tipo_periodo='Semestre'
                )
                anio_activo.id = 'temp'
        
        # Asignar el año académico a todas las planificaciones sin año
        if not dry_run:
            updated = planificaciones_sin_anio.update(anio_academico=anio_activo)
            self.stdout.write(
                self.style.SUCCESS(f'✅ {updated} planificaciones actualizadas con año académico: {anio_activo.nombre}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'[DRY-RUN] Se asignarían {total} planificaciones al año académico: {anio_activo.nombre}')
            )
        
        self.stdout.write(
            self.style.SUCCESS('🎯 Migración completada. Ahora todas las planificaciones tienen año académico.')
        )