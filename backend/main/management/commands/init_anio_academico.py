from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from main.models import AnioAcademico, PeriodoAcademico, Feriado, PeriodoVacaciones

class Command(BaseCommand):
    help = 'Inicializa un año académico de ejemplo con semestres, feriados y vacaciones'

    def add_arguments(self, parser):
        parser.add_argument('--year', type=int, default=2025, help='Año académico a crear')
        parser.add_argument('--tipo', type=str, default='SEMESTRE', choices=['SEMESTRE', 'TRIMESTRE', 'ANUAL'], help='Tipo de periodo')

    def handle(self, *args, **options):
        year = options['year']
        tipo = options['tipo']
        
        # Crear año académico
        anio, created = AnioAcademico.objects.get_or_create(
            nombre=str(year),
            defaults={
                'fecha_inicio': datetime(year, 3, 1).date(),  # Marzo 1
                'fecha_fin': datetime(year, 12, 31).date(),   # Diciembre 31
                'tipo_periodo': tipo,
                'activo': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Año académico {year} creado'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ Año académico {year} ya existe'))
            return
        
        # Crear periodos según el tipo
        if tipo == 'SEMESTRE':
            periodos_data = [
                {'nombre': 'Primer Semestre', 'numero': 1, 'fecha_inicio': datetime(year, 3, 1).date(), 'fecha_fin': datetime(year, 7, 15).date()},
                {'nombre': 'Segundo Semestre', 'numero': 2, 'fecha_inicio': datetime(year, 8, 1).date(), 'fecha_fin': datetime(year, 12, 15).date()},
            ]
        elif tipo == 'TRIMESTRE':
            periodos_data = [
                {'nombre': 'Primer Trimestre', 'numero': 1, 'fecha_inicio': datetime(year, 3, 1).date(), 'fecha_fin': datetime(year, 5, 31).date()},
                {'nombre': 'Segundo Trimestre', 'numero': 2, 'fecha_inicio': datetime(year, 6, 1).date(), 'fecha_fin': datetime(year, 8, 31).date()},
                {'nombre': 'Tercer Trimestre', 'numero': 3, 'fecha_inicio': datetime(year, 9, 1).date(), 'fecha_fin': datetime(year, 12, 15).date()},
            ]
        else:  # ANUAL
            periodos_data = [
                {'nombre': 'Año Completo', 'numero': 1, 'fecha_inicio': datetime(year, 3, 1).date(), 'fecha_fin': datetime(year, 12, 15).date()},
            ]
        
        for periodo_data in periodos_data:
            PeriodoAcademico.objects.create(anio_academico=anio, **periodo_data)
            self.stdout.write(self.style.SUCCESS(f'  ✓ {periodo_data["nombre"]} creado'))
        
        # Feriados nacionales típicos de Chile
        feriados_data = [
            {'nombre': 'Año Nuevo', 'fecha': datetime(year, 1, 1).date(), 'tipo': 'FERIADO'},
            {'nombre': 'Día del Trabajo', 'fecha': datetime(year, 5, 1).date(), 'tipo': 'FERIADO'},
            {'nombre': 'Glorias Navales', 'fecha': datetime(year, 5, 21).date(), 'tipo': 'FERIADO'},
            {'nombre': 'Día de San Pedro y San Pablo', 'fecha': datetime(year, 6, 29).date(), 'tipo': 'FERIADO'},
            {'nombre': 'Día de la Virgen del Carmen', 'fecha': datetime(year, 7, 16).date(), 'tipo': 'FERIADO'},
            {'nombre': 'Asunción de la Virgen', 'fecha': datetime(year, 8, 15).date(), 'tipo': 'FERIADO'},
            {'nombre': 'Independencia Nacional', 'fecha': datetime(year, 9, 18).date(), 'tipo': 'FERIADO'},
            {'nombre': 'Glorias del Ejército', 'fecha': datetime(year, 9, 19).date(), 'tipo': 'FERIADO'},
            {'nombre': 'Encuentro de Dos Mundos', 'fecha': datetime(year, 10, 12).date(), 'tipo': 'FERIADO'},
            {'nombre': 'Día de las Iglesias Evangélicas', 'fecha': datetime(year, 10, 31).date(), 'tipo': 'FERIADO'},
            {'nombre': 'Día de Todos los Santos', 'fecha': datetime(year, 11, 1).date(), 'tipo': 'FERIADO'},
            {'nombre': 'Inmaculada Concepción', 'fecha': datetime(year, 12, 8).date(), 'tipo': 'FERIADO'},
            {'nombre': 'Navidad', 'fecha': datetime(year, 12, 25).date(), 'tipo': 'FERIADO'},
        ]
        
        for feriado_data in feriados_data:
            Feriado.objects.create(anio_academico=anio, **feriado_data)
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(feriados_data)} feriados creados'))
        
        # Periodos de vacaciones
        vacaciones_data = [
            {'nombre': 'Vacaciones de Invierno 2025', 'fecha_inicio': datetime(year, 7, 16).date(), 'fecha_fin': datetime(year, 7, 31).date(), 'tipo': 'INVIERNO'},
            {'nombre': 'Vacaciones de Verano 2025-2026', 'fecha_inicio': datetime(year, 12, 16).date(), 'fecha_fin': datetime(year + 1, 2, 28).date(), 'tipo': 'VERANO'},
        ]
        
        for vacacion_data in vacaciones_data:
            PeriodoVacaciones.objects.create(anio_academico=anio, **vacacion_data)
            self.stdout.write(self.style.SUCCESS(f'  ✓ {vacacion_data["nombre"]} creado'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Año académico {year} inicializado correctamente'))
        self.stdout.write(f'   - Tipo: {tipo}')
        self.stdout.write(f'   - Periodos: {len(periodos_data)}')
        self.stdout.write(f'   - Feriados: {len(feriados_data)}')
        self.stdout.write(f'   - Vacaciones: {len(vacaciones_data)}')
