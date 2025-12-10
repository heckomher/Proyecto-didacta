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
        # Basado en el currículum nacional chileno (MINEDUC)
        electivos_por_plan = {
            'CH': [  # Científico-Humanista - Formación Diferenciada
                # Área Ciencias
                {'nombre': 'Biología Celular y Molecular', 'desc': 'Procesos celulares y moleculares'},
                {'nombre': 'Biología de los Ecosistemas', 'desc': 'Ecología y ecosistemas'},
                {'nombre': 'Ciencias de la Salud', 'desc': 'Salud humana y prevención'},
                {'nombre': 'Física', 'desc': 'Fenómenos físicos avanzados'},
                {'nombre': 'Química', 'desc': 'Reacciones y procesos químicos'},
                {'nombre': 'Probabilidades y Estadística Descriptiva e Inferencial', 'desc': 'Estadística aplicada'},
                {'nombre': 'Límites, Derivadas e Integrales', 'desc': 'Cálculo diferencial e integral'},
                {'nombre': 'Geometría 3D', 'desc': 'Geometría espacial'},
                # Área Humanidades
                {'nombre': 'Literatura e Identidad', 'desc': 'Literatura y cultura'},
                {'nombre': 'Taller de Literatura', 'desc': 'Creación literaria'},
                {'nombre': 'Lectura y Escritura Especializadas', 'desc': 'Comunicación avanzada'},
                {'nombre': 'Participación y Argumentación en Democracia', 'desc': 'Ciudadanía activa'},
                {'nombre': 'Geografía, Territorio y Desafíos Socioambientales', 'desc': 'Geografía y ambiente'},
                {'nombre': 'Economía y Sociedad', 'desc': 'Economía y desarrollo'},
                {'nombre': 'Chile y la Región Latinoamericana', 'desc': 'Historia regional'},
                {'nombre': 'Mundo Global', 'desc': 'Relaciones internacionales'},
                {'nombre': 'Comprensión Histórica del Presente', 'desc': 'Historia contemporánea'},
                # Área Filosofía
                {'nombre': 'Estética', 'desc': 'Filosofía del arte'},
                {'nombre': 'Filosofía Política', 'desc': 'Pensamiento político'},
                {'nombre': 'Argumentación Filosófica', 'desc': 'Lógica y argumentación'},
                # Área Artes
                {'nombre': 'Artes Visuales, Audiovisuales y Multimediales', 'desc': 'Expresión artística multimedia'},
                {'nombre': 'Interpretación y Creación en Danza', 'desc': 'Danza contemporánea'},
                {'nombre': 'Interpretación y Creación en Teatro', 'desc': 'Artes escénicas'},
                {'nombre': 'Interpretación y Creación Musical', 'desc': 'Música y composición'},
                {'nombre': 'Diseño y Arquitectura', 'desc': 'Diseño y espacio'},
                # Área Educación Física
                {'nombre': 'Ciencias del Ejercicio Físico y Deportivo', 'desc': 'Fisiología del deporte'},
                {'nombre': 'Promoción de Estilos de Vida Activos y Saludables', 'desc': 'Vida saludable'},
            ],
            'TP': [  # Técnico Profesional - Especialidades
                # Sector Administración
                {'nombre': 'Administración', 'desc': 'Gestión empresarial'},
                {'nombre': 'Contabilidad', 'desc': 'Registros contables'},
                {'nombre': 'Recursos Humanos', 'desc': 'Gestión de personas'},
                {'nombre': 'Logística', 'desc': 'Cadena de suministro'},
                {'nombre': 'Servicios de Turismo', 'desc': 'Industria turística'},
                # Sector Metalmecánica
                {'nombre': 'Mecánica Industrial', 'desc': 'Manufactura mecánica'},
                {'nombre': 'Mecánica Automotriz', 'desc': 'Sistemas automotrices'},
                {'nombre': 'Construcciones Metálicas', 'desc': 'Soldadura y estructuras'},
                {'nombre': 'Mecánica de Mantenimiento de Aeronaves', 'desc': 'Aviación'},
                # Sector Electricidad
                {'nombre': 'Electricidad', 'desc': 'Instalaciones eléctricas'},
                {'nombre': 'Electrónica', 'desc': 'Sistemas electrónicos'},
                {'nombre': 'Telecomunicaciones', 'desc': 'Comunicaciones'},
                # Sector Construcción
                {'nombre': 'Edificación', 'desc': 'Construcción de edificios'},
                {'nombre': 'Terminaciones de Construcción', 'desc': 'Acabados'},
                {'nombre': 'Instalaciones Sanitarias', 'desc': 'Gasfitería'},
                {'nombre': 'Refrigeración y Climatización', 'desc': 'HVAC'},
                # Sector Salud y Educación
                {'nombre': 'Enfermería', 'desc': 'Cuidados de salud'},
                {'nombre': 'Atención de Párvulos', 'desc': 'Educación inicial'},
                {'nombre': 'Atención de Adultos Mayores', 'desc': 'Gerontología'},
                # Sector Alimentación
                {'nombre': 'Gastronomía', 'desc': 'Cocina y pastelería'},
                {'nombre': 'Elaboración Industrial de Alimentos', 'desc': 'Industria alimentaria'},
                # Sector Tecnologías
                {'nombre': 'Programación', 'desc': 'Desarrollo de software'},
                {'nombre': 'Conectividad y Redes', 'desc': 'Infraestructura TI'},
            ],
            'ARTISTICO': [  # Artístico - Formación Diferenciada
                {'nombre': 'Artes Visuales', 'desc': 'Expresión visual especializada'},
                {'nombre': 'Artes Musicales', 'desc': 'Formación musical avanzada'},
                {'nombre': 'Artes Escénicas', 'desc': 'Teatro y performance'},
                {'nombre': 'Danza', 'desc': 'Expresión corporal y danza'},
                {'nombre': 'Audiovisual', 'desc': 'Producción audiovisual'},
                {'nombre': 'Diseño', 'desc': 'Diseño gráfico y de productos'},
                {'nombre': 'Fotografía', 'desc': 'Arte fotográfico'},
                {'nombre': 'Escultura', 'desc': 'Arte tridimensional'},
                {'nombre': 'Grabado y Estampa', 'desc': 'Técnicas de impresión artística'},
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
