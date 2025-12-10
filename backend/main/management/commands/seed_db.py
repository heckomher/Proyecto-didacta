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
        self._seed_electivos()
        
        self.stdout.write(self.style.SUCCESS('\n✓ Siembra completada exitosamente'))

    def _seed_niveles_educativos(self):
        """Siembra los niveles educativos del sistema chileno"""
        self.stdout.write('\n[1/3] Sembrando Niveles Educativos...')
        
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
        """Siembra las asignaturas comunes del currículum chileno"""
        self.stdout.write('\n[2/3] Sembrando Asignaturas Comunes...')
        
        # Asignaturas COMUNES organizadas por nivel educativo
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
                {'nombre': 'Ciencias para la Ciudadanía', 'desc': 'Formación científica ciudadana'},
                {'nombre': 'Educación Ciudadana', 'desc': 'Formación cívica y ciudadana'},
                {'nombre': 'Filosofía', 'desc': 'Pensamiento filosófico y ético'},
            ],
        }
        
        creados = 0
        actualizados = 0
        existentes = 0
        
        for nivel_nombre, asignaturas in asignaturas_por_nivel.items():
            for asig_data in asignaturas:
                descripcion_completa = f"{asig_data['desc']} - {nivel_nombre}"
                
                asig, created = Asignatura.objects.get_or_create(
                    nombre_asignatura=asig_data['nombre'],
                    defaults={
                        'descripcion': descripcion_completa,
                        'tipo': 'COMUN',
                        'plan_asociado': ''
                    }
                )
                
                if created:
                    creados += 1
                    self.stdout.write(self.style.SUCCESS(f'  ✓ {asig.nombre_asignatura}'))
                else:
                    # Actualizar descripción y tipo si es necesario
                    needs_update = False
                    if nivel_nombre not in asig.descripcion:
                        asig.descripcion = descripcion_completa
                        needs_update = True
                    if asig.tipo != 'COMUN':
                        asig.tipo = 'COMUN'
                        needs_update = True
                    
                    if needs_update:
                        asig.save()
                        actualizados += 1
                    else:
                        existentes += 1
        
        self.stdout.write(f'  Resultado: {creados} creadas, {actualizados} actualizadas, {existentes} sin cambios')

    def _seed_electivos(self):
        """Siembra los electivos del Plan de Formación Diferenciada (3°-4° Medio)"""
        self.stdout.write('\n[3/3] Sembrando Electivos por Plan Diferenciado...')
        
        # Electivos organizados por plan diferenciado (3°-4° Medio)
        electivos_por_plan = {
            'CH': [  # Científico-Humanista
                {'nombre': 'Biología Celular y Molecular', 'desc': 'Estudio avanzado de biología'},
                {'nombre': 'Física', 'desc': 'Ciencias físicas avanzadas'},
                {'nombre': 'Química', 'desc': 'Ciencias químicas avanzadas'},
                {'nombre': 'Probabilidades y Estadística', 'desc': 'Matemática aplicada'},
                {'nombre': 'Límites, Derivadas e Integrales', 'desc': 'Cálculo diferencial e integral'},
                {'nombre': 'Literatura e Identidad', 'desc': 'Análisis literario avanzado'},
                {'nombre': 'Participación y Argumentación en Democracia', 'desc': 'Formación ciudadana avanzada'},
                {'nombre': 'Geografía, Territorio y Desafíos Socioambientales', 'desc': 'Geografía humana y ambiental'},
                {'nombre': 'Economía y Sociedad', 'desc': 'Fundamentos de economía'},
                {'nombre': 'Estética', 'desc': 'Filosofía del arte'},
                {'nombre': 'Filosofía Política', 'desc': 'Pensamiento político'},
            ],
            'TP': [  # Técnico Profesional
                {'nombre': 'Administración', 'desc': 'Fundamentos de administración'},
                {'nombre': 'Contabilidad', 'desc': 'Principios contables'},
                {'nombre': 'Electricidad', 'desc': 'Fundamentos de electricidad'},
                {'nombre': 'Electrónica', 'desc': 'Circuitos y sistemas electrónicos'},
                {'nombre': 'Mecánica Industrial', 'desc': 'Procesos mecánicos industriales'},
                {'nombre': 'Mecánica Automotriz', 'desc': 'Sistemas automotrices'},
                {'nombre': 'Construcción', 'desc': 'Técnicas de construcción'},
                {'nombre': 'Enfermería', 'desc': 'Cuidados de salud'},
                {'nombre': 'Gastronomía', 'desc': 'Artes culinarias'},
                {'nombre': 'Programación', 'desc': 'Desarrollo de software'},
                {'nombre': 'Conectividad y Redes', 'desc': 'Infraestructura de redes'},
            ],
            'ARTISTICO': [  # Artístico
                {'nombre': 'Artes Visuales Avanzado', 'desc': 'Expresión visual especializada'},
                {'nombre': 'Artes Musicales', 'desc': 'Formación musical avanzada'},
                {'nombre': 'Artes Escénicas', 'desc': 'Teatro y performance'},
                {'nombre': 'Danza', 'desc': 'Expresión corporal y danza'},
                {'nombre': 'Audiovisual', 'desc': 'Producción audiovisual'},
                {'nombre': 'Diseño', 'desc': 'Diseño gráfico y de productos'},
            ],
        }
        
        creados = 0
        actualizados = 0
        existentes = 0
        
        for plan, electivos in electivos_por_plan.items():
            plan_display = {'CH': 'Científico-Humanista', 'TP': 'Técnico Profesional', 'ARTISTICO': 'Artístico'}[plan]
            self.stdout.write(f'  Plan {plan_display}:')
            
            for elec_data in electivos:
                descripcion_completa = f"{elec_data['desc']} - Educación Media ({plan_display})"
                
                asig, created = Asignatura.objects.get_or_create(
                    nombre_asignatura=elec_data['nombre'],
                    defaults={
                        'descripcion': descripcion_completa,
                        'tipo': 'ELECTIVO',
                        'plan_asociado': plan
                    }
                )
                
                if created:
                    creados += 1
                    self.stdout.write(self.style.SUCCESS(f'    ✓ {asig.nombre_asignatura}'))
                else:
                    # Actualizar si es necesario
                    needs_update = False
                    if asig.tipo != 'ELECTIVO':
                        asig.tipo = 'ELECTIVO'
                        needs_update = True
                    if asig.plan_asociado != plan:
                        asig.plan_asociado = plan
                        needs_update = True
                    
                    if needs_update:
                        asig.save()
                        actualizados += 1
                        self.stdout.write(f'    ↻ Actualizado: {asig.nombre_asignatura}')
                    else:
                        existentes += 1
        
        self.stdout.write(f'  Resultado: {creados} creados, {actualizados} actualizados, {existentes} sin cambios')
