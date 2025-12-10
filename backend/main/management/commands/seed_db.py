from django.core.management.base import BaseCommand
from main.models import NivelEducativo, Asignatura


class Command(BaseCommand):
    help = 'Inicializa los datos base del sistema (niveles educativos, asignaturas, etc.)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Forzar re-creación de datos aunque ya existan',
        )

    def handle(self, *args, **options):
        force = options.get('force', False)
        
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('SIEMBRA DE BASE DE DATOS - DIDACTA'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        
        self._seed_niveles_educativos()
        self._seed_asignaturas()
        
        self.stdout.write(self.style.SUCCESS('\n✓ Siembra completada exitosamente'))

    def _seed_niveles_educativos(self):
        """Siembra los niveles educativos del sistema chileno"""
        self.stdout.write('\n[1/2] Sembrando Niveles Educativos...')
        
        niveles = [
            {'nombre': 'Educación Parvularia', 'descripcion': 'Pre-kínder y Kínder'},
            {'nombre': 'Educación Básica', 'descripcion': '1° a 8° Básico'},
            {'nombre': 'Educación Media', 'descripcion': '1° a 4° Medio'},
        ]
        
        creados = 0
        existentes = 0
        
        for nivel_data in niveles:
            nivel, created = NivelEducativo.objects.get_or_create(
                nombre=nivel_data['nombre'],
                defaults={'descripcion': nivel_data['descripcion']}
            )
            
            if created:
                creados += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Creado: {nivel.nombre}'))
            else:
                existentes += 1
                self.stdout.write(f'  - Ya existe: {nivel.nombre}')
        
        self.stdout.write(f'  Resultado: {creados} creados, {existentes} existían')

    def _seed_asignaturas(self):
        """Siembra las asignaturas del currículum chileno"""
        self.stdout.write('\n[2/2] Sembrando Asignaturas...')
        
        asignaturas = [
            # Asignaturas comunes
            {'nombre_asignatura': 'Lenguaje y Comunicación', 'descripcion': 'Desarrollo de habilidades comunicativas'},
            {'nombre_asignatura': 'Matemática', 'descripcion': 'Desarrollo del pensamiento lógico-matemático'},
            {'nombre_asignatura': 'Historia, Geografía y Ciencias Sociales', 'descripcion': 'Conocimiento del entorno social'},
            {'nombre_asignatura': 'Ciencias Naturales', 'descripcion': 'Exploración del mundo natural'},
            {'nombre_asignatura': 'Inglés', 'descripcion': 'Idioma extranjero'},
            {'nombre_asignatura': 'Educación Física y Salud', 'descripcion': 'Desarrollo motriz y vida saludable'},
            {'nombre_asignatura': 'Artes Visuales', 'descripcion': 'Expresión artística visual'},
            {'nombre_asignatura': 'Música', 'descripcion': 'Expresión musical'},
            {'nombre_asignatura': 'Tecnología', 'descripcion': 'Desarrollo tecnológico'},
            {'nombre_asignatura': 'Orientación', 'descripcion': 'Desarrollo personal y social'},
            # Educación Media
            {'nombre_asignatura': 'Física', 'descripcion': 'Ciencias físicas - Educación Media'},
            {'nombre_asignatura': 'Química', 'descripcion': 'Ciencias químicas - Educación Media'},
            {'nombre_asignatura': 'Biología', 'descripcion': 'Ciencias biológicas - Educación Media'},
            {'nombre_asignatura': 'Filosofía', 'descripcion': 'Pensamiento filosófico - Educación Media'},
            # Parvularia
            {'nombre_asignatura': 'Ámbito Personal y Social', 'descripcion': 'Desarrollo socioemocional - Parvularia'},
            {'nombre_asignatura': 'Comunicación Integral', 'descripcion': 'Lenguaje verbal y artístico - Parvularia'},
            {'nombre_asignatura': 'Interacción y Comprensión del Entorno', 'descripcion': 'Exploración del entorno - Parvularia'},
        ]
        
        creados = 0
        existentes = 0
        
        for asig_data in asignaturas:
            asig, created = Asignatura.objects.get_or_create(
                nombre_asignatura=asig_data['nombre_asignatura'],
                defaults={'descripcion': asig_data['descripcion']}
            )
            
            if created:
                creados += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Creada: {asig.nombre_asignatura}'))
            else:
                existentes += 1
        
        if existentes > 0:
            self.stdout.write(f'  - {existentes} asignaturas ya existían')
        self.stdout.write(f'  Resultado: {creados} creadas, {existentes} existían')
