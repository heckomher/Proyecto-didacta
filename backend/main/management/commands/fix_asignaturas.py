"""
Comando para corregir asignaturas:
- Filosofía solo debe existir para III° y IV° Medio
- Para otros niveles debe llamarse "Formación Valórica"
"""
from django.core.management.base import BaseCommand
from main.models import Asignatura, NivelEducativo, CursoAsignatura, Curso


class Command(BaseCommand):
    help = 'Corrige asignaturas: Filosofía solo para III-IV Medio, resto es Formación Valórica'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simular cambios sin aplicarlos',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('=== MODO SIMULACIÓN (--dry-run) ==='))
        
        # Niveles donde Filosofía es válida
        niveles_filosofia = ['III° Medio', 'IV° Medio', '3° Medio', '4° Medio', 'III Medio', 'IV Medio']
        
        # Buscar o crear asignatura "Formación Valórica"
        formacion_valorica = None
        try:
            formacion_valorica = Asignatura.objects.get(nombre_asignatura='Formación Valórica')
            self.stdout.write(f'✓ Asignatura "Formación Valórica" ya existe (ID: {formacion_valorica.id})')
        except Asignatura.DoesNotExist:
            if not dry_run:
                formacion_valorica = Asignatura.objects.create(
                    nombre_asignatura='Formación Valórica',
                    descripcion='Formación en valores para niveles básica y media (excepto III° y IV° Medio)',
                    tipo='COMUN'
                )
                self.stdout.write(self.style.SUCCESS(
                    f'✓ Creada asignatura "Formación Valórica" (ID: {formacion_valorica.id})'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    '→ Se crearía asignatura "Formación Valórica"'
                ))
        
        # Buscar asignatura Filosofía
        try:
            filosofia = Asignatura.objects.get(nombre_asignatura='Filosofía')
            self.stdout.write(f'✓ Encontrada asignatura "Filosofía" (ID: {filosofia.id})')
        except Asignatura.DoesNotExist:
            self.stdout.write(self.style.WARNING('⚠ No existe asignatura "Filosofía" en la base de datos'))
            return
        
        # Buscar cursos con Filosofía asignada que NO son III° o IV° Medio
        cursos_a_cambiar = []
        
        for curso_asig in CursoAsignatura.objects.filter(asignatura=filosofia).select_related('curso', 'curso__nivel'):
            curso = curso_asig.curso
            nivel_nombre = curso.nivel.nombre if curso.nivel else ''
            
            # Verificar si este curso NO debería tener Filosofía
            es_nivel_filosofia = any(nf in nivel_nombre for nf in niveles_filosofia)
            
            if not es_nivel_filosofia:
                cursos_a_cambiar.append({
                    'curso_asig': curso_asig,
                    'curso': curso,
                    'nivel': nivel_nombre
                })
        
        if not cursos_a_cambiar:
            self.stdout.write(self.style.SUCCESS(
                '✓ No hay cursos con Filosofía que deban cambiarse a Formación Valórica'
            ))
            return
        
        self.stdout.write(f'\nEncontrados {len(cursos_a_cambiar)} curso(s) con Filosofía que deberían tener "Formación Valórica":')
        
        for item in cursos_a_cambiar:
            curso = item['curso']
            self.stdout.write(f'  - {curso.nombre_curso} ({item["nivel"]})')
            
            if not dry_run and formacion_valorica:
                # Cambiar la asignatura
                item['curso_asig'].asignatura = formacion_valorica
                item['curso_asig'].save()
                self.stdout.write(self.style.SUCCESS(f'    ✓ Cambiado a "Formación Valórica"'))
        
        if dry_run:
            self.stdout.write(self.style.WARNING(
                f'\n→ Se cambiarían {len(cursos_a_cambiar)} asignaciones de Filosofía a Formación Valórica'
            ))
            self.stdout.write(self.style.WARNING('Ejecuta sin --dry-run para aplicar los cambios'))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'\n✓ Completado: {len(cursos_a_cambiar)} asignaciones actualizadas'
            ))
