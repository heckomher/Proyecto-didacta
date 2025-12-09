from django.core.management.base import BaseCommand
from main.models import Curso, AnioAcademico

class Command(BaseCommand):
    help = 'Asigna cursos sin año académico al año activo o más reciente'

    def handle(self, *args, **options):
        # Buscar cursos sin año académico
        cursos_sin_anio = Curso.objects.filter(anio_academico__isnull=True)
        
        if not cursos_sin_anio.exists():
            self.stdout.write(self.style.SUCCESS('No hay cursos sin año académico'))
            return
        
        # Buscar año académico activo o el más reciente
        anio_activo = AnioAcademico.objects.filter(estado='ACTIVO').first()
        
        if not anio_activo:
            anio_activo = AnioAcademico.objects.filter(estado='BORRADOR').order_by('-fecha_inicio').first()
        
        if not anio_activo:
            self.stdout.write(self.style.ERROR('No hay años académicos disponibles. Cree uno primero.'))
            return
        
        # Asignar cursos al año encontrado
        count = cursos_sin_anio.update(anio_academico=anio_activo)
        
        self.stdout.write(self.style.SUCCESS(
            f'✓ Se asignaron {count} cursos al año académico "{anio_activo.nombre}"'
        ))
