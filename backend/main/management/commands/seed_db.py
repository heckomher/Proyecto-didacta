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
        """Siembra las asignaturas del currículum chileno con niveles educativos"""
        self.stdout.write('\n[2/2] Sembrando Asignaturas del Currículum Chileno...')
        
        # Asignaturas organizadas por nivel educativo chileno
        asignaturas_por_nivel = {
            'Educación Parvularia': [
                {'nombre': 'Ámbito Personal y Social', 'desc': 'Desarrollo socioemocional'},
                {'nombre': 'Comunicación Integral', 'desc': 'Lenguaje verbal y artístico'},
                {'nombre': 'Interacción y Comprensión del Entorno', 'desc': 'Exploración del entorno'},
            ],
            'Educación Básica': [
                {'nombre': 'Lenguaje y Comunicación', 'desc': 'Desarrollo de habilidades comunicativas'},
                {'nombre': 'Matemática', 'desc': 'Desarrollo del pensamiento lógico-matemático'},
                {'nombre': 'Historia, Geografía y Ciencias Sociales', 'desc': 'Conocimiento del entorno social'},
                {'nombre': 'Ciencias Naturales', 'desc': 'Exploración del mundo natural'},
                {'nombre': 'Inglés', 'desc': 'Idioma extranjero'},
                {'nombre': 'Educación Física y Salud', 'desc': 'Desarrollo motriz y vida saludable'},
                {'nombre': 'Artes Visuales', 'desc': 'Expresión artística visual'},
                {'nombre': 'Música', 'desc': 'Expresión musical'},
                {'nombre': 'Tecnología', 'desc': 'Desarrollo tecnológico'},
                {'nombre': 'Orientación', 'desc': 'Desarrollo personal y social'},
            ],
            'Educación Media': [
                {'nombre': 'Lengua y Literatura', 'desc': 'Comprensión y producción de textos'},
                {'nombre': 'Matemática', 'desc': 'Desarrollo del pensamiento lógico-matemático'},
                {'nombre': 'Historia, Geografía y Ciencias Sociales', 'desc': 'Formación ciudadana'},
                {'nombre': 'Inglés', 'desc': 'Idioma extranjero'},
                {'nombre': 'Educación Física y Salud', 'desc': 'Desarrollo motriz y vida saludable'},
                {'nombre': 'Física', 'desc': 'Ciencias físicas'},
                {'nombre': 'Química', 'desc': 'Ciencias químicas'},
                {'nombre': 'Biología', 'desc': 'Ciencias biológicas'},
                {'nombre': 'Filosofía', 'desc': 'Pensamiento filosófico y ético'},
                {'nombre': 'Artes Visuales', 'desc': 'Expresión artística visual'},
                {'nombre': 'Música', 'desc': 'Expresión musical'},
                {'nombre': 'Tecnología', 'desc': 'Desarrollo tecnológico'},
            ],
        }
        
        creados = 0
        actualizados = 0
        existentes = 0
        
        for nivel_nombre, asignaturas in asignaturas_por_nivel.items():
            for asig_data in asignaturas:
                # La descripción incluye el nivel para el filtro sugeridas-por-nivel
                descripcion_completa = f"{asig_data['desc']} - {nivel_nombre}"
                
                asig, created = Asignatura.objects.get_or_create(
                    nombre_asignatura=asig_data['nombre'],
                    defaults={'descripcion': descripcion_completa}
                )
                
                if created:
                    creados += 1
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Creada: {asig.nombre_asignatura} ({nivel_nombre})'))
                else:
                    # Actualizar descripción si no tiene el nivel
                    if nivel_nombre not in asig.descripcion:
                        asig.descripcion = descripcion_completa
                        asig.save()
                        actualizados += 1
                        self.stdout.write(f'  ↻ Actualizada: {asig.nombre_asignatura} → {nivel_nombre}')
                    else:
                        existentes += 1
        
        self.stdout.write(f'  Resultado: {creados} creadas, {actualizados} actualizadas, {existentes} sin cambios')

