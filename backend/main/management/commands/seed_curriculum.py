"""
Comando para poblar el currículum nacional en MongoDB
Ejecutar con: python manage.py seed_curriculum
"""
from django.core.management.base import BaseCommand
from main.mongo_models import (
    UnidadCurricular, ObjetivoAprendizaje, IndicadorEvaluacion,
    ObjetivoTransversal, Habilidad, Actitud, ArticulacionCurricular
)

# Importar datos - Básica
from .curriculum_data_basica import (
    MATEMATICA_BASICA, EDUFISICA_BASICA
)
from .curriculum_data_lenguaje import LENGUAJE_BASICA
from .curriculum_data_ciencias import CIENCIAS_BASICA_COMPLETA
from .curriculum_data_historia import HISTORIA_BASICA_COMPLETA

# Importar datos - Media
from .curriculum_data_media import (
    LENGUA_MEDIA, MATEMATICA_MEDIA, BIOLOGIA_MEDIA, FISICA_MEDIA,
    QUIMICA_MEDIA, FILOSOFIA_MEDIA, CIUDADANA_MEDIA, HISTORIA_MEDIA
)


class Command(BaseCommand):
    help = 'Poblar datos del Currículum Nacional Chileno en MongoDB'
    
    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Limpiar datos existentes antes de poblar')
    
    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Limpiando datos existentes...')
            UnidadCurricular.objects.delete()
            ObjetivoAprendizaje.objects.delete()
            ObjetivoTransversal.objects.delete()
            Habilidad.objects.delete()
            Actitud.objects.delete()
        
        # Poblar OAT (transversales)
        self.poblar_oat()
        self.poblar_actitudes_transversales()
        
        # Poblar Lenguaje 1° Básico (método original)
        self.poblar_lenguaje_1b()
        
        # Poblar desde archivos de datos - EDUCACIÓN BÁSICA
        self.stdout.write('\n📚 EDUCACIÓN BÁSICA')
        self.poblar_asignatura('Lenguaje 2°-8° Básico', LENGUAJE_BASICA)
        self.poblar_asignatura('Matemática 1°-8° Básico', MATEMATICA_BASICA)
        self.poblar_asignatura('Ciencias Naturales 1°-8° Básico', CIENCIAS_BASICA_COMPLETA)
        self.poblar_asignatura('Historia 1°-8° Básico', HISTORIA_BASICA_COMPLETA)
        self.poblar_asignatura('Educación Física 8° Básico', EDUFISICA_BASICA)
        
        # Poblar desde archivos de datos - EDUCACIÓN MEDIA
        self.stdout.write('\n📖 EDUCACIÓN MEDIA')
        self.poblar_asignatura('Lengua y Literatura I°-II° Medio', LENGUA_MEDIA)
        self.poblar_asignatura('Matemática I°-II° Medio', MATEMATICA_MEDIA)
        self.poblar_asignatura('Biología III° Medio (Electivo CH)', BIOLOGIA_MEDIA)
        self.poblar_asignatura('Física III° Medio (Electivo CH)', FISICA_MEDIA)
        self.poblar_asignatura('Química III° Medio (Electivo CH)', QUIMICA_MEDIA)
        self.poblar_asignatura('Filosofía III° Medio (Electivo CH)', FILOSOFIA_MEDIA)
        self.poblar_asignatura('Educación Ciudadana III° Medio', CIUDADANA_MEDIA)
        self.poblar_asignatura('Historia I° Medio', HISTORIA_MEDIA)
        
        self.stdout.write(self.style.SUCCESS('\n✅ ¡Currículum Nacional poblado exitosamente!'))
    
    def poblar_asignatura(self, nombre, data):
        """Poblar una asignatura completa desde su diccionario de datos"""
        self.stdout.write(f'  Poblando {nombre}...')
        
        total_oas = 0
        total_unidades = 0
        
        # Poblar actitudes si existen
        if 'actitudes' in data:
            for act in data['actitudes']:
                Actitud.objects(codigo=act['codigo']).update_one(
                    upsert=True,
                    set__asignatura=act['asignatura'],
                    set__numero=act['numero'],
                    set__descripcion=act['descripcion']
                )
        
        # Poblar por nivel
        for nivel, nivel_data in data.get('niveles', {}).items():
            # Poblar OAs
            for oa_data in nivel_data.get('oas', []):
                indicadores = [IndicadorEvaluacion(**ind) for ind in oa_data.get('indicadores', [])]
                articulaciones = [ArticulacionCurricular(**art) for art in oa_data.get('articulaciones', [])]
                
                ObjetivoAprendizaje.objects(codigo=oa_data['codigo']).update_one(
                    upsert=True,
                    set__nivel=oa_data['nivel'],
                    set__asignatura=oa_data['asignatura'],
                    set__eje=oa_data.get('eje', ''),
                    set__numero=oa_data['numero'],
                    set__descripcion=oa_data['descripcion'],
                    set__priorizado_2025=oa_data.get('priorizado_2025', False),
                    set__nivel_priorizacion=oa_data.get('nivel_priorizacion'),
                    set__indicadores=indicadores,
                    set__articulaciones_con=articulaciones
                )
                total_oas += 1
            
            # Poblar Unidades
            for u_data in nivel_data.get('unidades', []):
                UnidadCurricular.objects(codigo=u_data['codigo']).update_one(
                    upsert=True,
                    set__nivel=u_data['nivel'],
                    set__asignatura=u_data['asignatura'],
                    set__numero=u_data['numero'],
                    set__nombre=u_data['nombre'],
                    set__descripcion=u_data.get('descripcion', ''),
                    set__oa_codigos=u_data.get('oa_codigos', []),
                    set__oat_codigos=u_data.get('oat_codigos', []),
                    set__habilidades_codigos=u_data.get('habilidades_codigos', []),
                    set__actitudes_codigos=u_data.get('actitudes_codigos', []),
                    set__horas_sugeridas=u_data.get('horas_sugeridas', 40),
                    set__semanas_sugeridas=u_data.get('semanas_sugeridas', 5),
                    set__priorizado_2025=u_data.get('priorizado_2025', False)
                )
                total_unidades += 1
        
        self.stdout.write(f'    → {total_oas} OAs, {total_unidades} unidades')
    
    def poblar_oat(self):
        """Poblar Objetivos de Aprendizaje Transversales"""
        self.stdout.write('Poblando OAT...')
        
        oats = [
            {'codigo': 'OAT-COG-01', 'dimension': 'COGNITIVA', 'numero': 1,
             'descripcion': 'Identificar, procesar y sintetizar información de diversas fuentes.'},
            {'codigo': 'OAT-COG-02', 'dimension': 'COGNITIVA', 'numero': 2,
             'descripcion': 'Organizar, clasificar, analizar, interpretar y sintetizar la información.'},
            {'codigo': 'OAT-COG-03', 'dimension': 'COGNITIVA', 'numero': 3,
             'descripcion': 'Exponer ideas, opiniones y experiencias de manera coherente y fundamentada.'},
            {'codigo': 'OAT-COG-04', 'dimension': 'COGNITIVA', 'numero': 4,
             'descripcion': 'Resolver problemas de manera reflexiva aplicando conceptos y criterios.'},
            {'codigo': 'OAT-AFE-01', 'dimension': 'AFECTIVA', 'numero': 1,
             'descripcion': 'Adquirir un sentido positivo ante la vida y sana autoestima.'},
            {'codigo': 'OAT-AFE-02', 'dimension': 'AFECTIVA', 'numero': 2,
             'descripcion': 'Comprender la importancia de las dimensiones afectiva, ética y social.'},
            {'codigo': 'OAT-SOC-01', 'dimension': 'SOCIOCULTURAL', 'numero': 1,
             'descripcion': 'Conocer y valorar la historia, tradiciones y patrimonio de la nación.'},
            {'codigo': 'OAT-SOC-02', 'dimension': 'SOCIOCULTURAL', 'numero': 2,
             'descripcion': 'Valorar la vida en sociedad y actuar según valores de convivencia cívica.'},
            {'codigo': 'OAT-MOR-01', 'dimension': 'MORAL', 'numero': 1,
             'descripcion': 'Conocer, respetar y defender la igualdad de derechos de todas las personas.'},
            {'codigo': 'OAT-FIS-01', 'dimension': 'FISICA', 'numero': 1,
             'descripcion': 'Practicar actividad física y apreciar sus beneficios para la salud.'},
        ]
        
        for oat_data in oats:
            ObjetivoTransversal.objects(codigo=oat_data['codigo']).update_one(
                upsert=True,
                set__dimension=oat_data['dimension'],
                set__numero=oat_data['numero'],
                set__descripcion=oat_data['descripcion']
            )
        self.stdout.write(f'  → {len(oats)} OAT')
    
    def poblar_actitudes_transversales(self):
        """Poblar actitudes transversales comunes"""
        actitudes = [
            {'codigo': 'TRANS-ACT01', 'asignatura': 'TRANS', 'numero': 1,
             'descripcion': 'Demostrar disposición e interés por compartir ideas y experiencias.'},
            {'codigo': 'TRANS-ACT02', 'asignatura': 'TRANS', 'numero': 2,
             'descripcion': 'Demostrar respeto por las diversas opiniones y puntos de vista.'},
            {'codigo': 'TRANS-ACT03', 'asignatura': 'TRANS', 'numero': 3,
             'descripcion': 'Demostrar empatía hacia los demás.'},
        ]
        
        for act in actitudes:
            Actitud.objects(codigo=act['codigo']).update_one(
                upsert=True,
                set__asignatura=act['asignatura'],
                set__numero=act['numero'],
                set__descripcion=act['descripcion']
            )
        self.stdout.write(f'  → {len(actitudes)} actitudes transversales')
    
    def poblar_lenguaje_1b(self):
        """Poblar Lenguaje y Comunicación 1° Básico (código original)"""
        self.stdout.write('Poblando Lenguaje 1° Básico...')
        
        # Actitudes de Lenguaje
        actitudes_lyc = [
            {'codigo': 'Lyc-ACT01', 'asignatura': 'Lyc', 'numero': 1,
             'descripcion': 'Demostrar interés y una actitud activa frente a la lectura.'},
            {'codigo': 'Lyc-ACT02', 'asignatura': 'Lyc', 'numero': 2,
             'descripcion': 'Demostrar disposición e interés por expresarse creativamente.'},
            {'codigo': 'Lyc-ACT03', 'asignatura': 'Lyc', 'numero': 3,
             'descripcion': 'Demostrar respeto por las diversas opiniones.'},
        ]
        
        for act in actitudes_lyc:
            Actitud.objects(codigo=act['codigo']).update_one(
                upsert=True,
                set__asignatura=act['asignatura'],
                set__numero=act['numero'],
                set__descripcion=act['descripcion']
            )
        
        # Habilidades
        habilidades = [
            {'codigo': '1b-Lyc-HAB01', 'nivel': '1b', 'asignatura': 'Lyc', 'numero': 1, 'tipo': 'BASICA',
             'descripcion': 'Reconocer que los textos escritos transmiten mensajes.'},
            {'codigo': '1b-Lyc-HAB02', 'nivel': '1b', 'asignatura': 'Lyc', 'numero': 2, 'tipo': 'BASICA',
             'descripcion': 'Reconocer que las palabras son unidades de significado separadas.'},
            {'codigo': '1b-Lyc-HAB03', 'nivel': '1b', 'asignatura': 'Lyc', 'numero': 3, 'tipo': 'BASICA',
             'descripcion': 'Identificar los sonidos que componen las palabras.'},
            {'codigo': '1b-Lyc-HAB04', 'nivel': '1b', 'asignatura': 'Lyc', 'numero': 4, 'tipo': 'INTERMEDIA',
             'descripcion': 'Leer palabras aplicando correspondencia letra-sonido.'},
        ]
        
        for hab in habilidades:
            Habilidad.objects(codigo=hab['codigo']).update_one(
                upsert=True,
                set__nivel=hab['nivel'],
                set__asignatura=hab['asignatura'],
                set__numero=hab['numero'],
                set__tipo=hab['tipo'],
                set__descripcion=hab['descripcion']
            )
        
        # OAs de Lenguaje 1° Básico
        oas = [
            {'codigo': '1b-Lyc-OA01', 'nivel': '1b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 1,
             'descripcion': 'Reconocer que los textos escritos transmiten mensajes.',
             'priorizado_2025': True, 'nivel_priorizacion': 'P1',
             'indicadores': [
                 {'codigo': '1b-Lyc-OA01-I1', 'descripcion': 'Identificar textos escritos en el entorno.', 'verbo_infinitivo': 'Identificar'},
                 {'codigo': '1b-Lyc-OA01-I2', 'descripcion': 'Reconocer propósitos comunicativos.', 'verbo_infinitivo': 'Reconocer'},
             ]},
            {'codigo': '1b-Lyc-OA02', 'nivel': '1b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 2,
             'descripcion': 'Reconocer que las palabras son unidades separadas por espacios.',
             'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
            {'codigo': '1b-Lyc-OA03', 'nivel': '1b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 3,
             'descripcion': 'Identificar los sonidos que componen las palabras (conciencia fonológica).',
             'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
            {'codigo': '1b-Lyc-OA04', 'nivel': '1b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 4,
             'descripcion': 'Leer palabras aisladas y en contexto aplicando correspondencia letra-sonido.',
             'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
            {'codigo': '1b-Lyc-OA05', 'nivel': '1b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 5,
             'descripcion': 'Leer textos breves en voz alta para adquirir fluidez.',
             'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
            {'codigo': '1b-Lyc-OA13', 'nivel': '1b', 'asignatura': 'Lyc', 'eje': 'Escritura', 'numero': 13,
             'descripcion': 'Experimentar con la escritura para comunicar hechos e ideas.',
             'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
            {'codigo': '1b-Lyc-OA14', 'nivel': '1b', 'asignatura': 'Lyc', 'eje': 'Escritura', 'numero': 14,
             'descripcion': 'Escribir oraciones completas para transmitir mensajes.',
             'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
            {'codigo': '1b-Lyc-OA18', 'nivel': '1b', 'asignatura': 'Lyc', 'eje': 'Comunicación Oral', 'numero': 18,
             'descripcion': 'Comprender textos orales para obtener información.',
             'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
            {'codigo': '1b-Lyc-OA21', 'nivel': '1b', 'asignatura': 'Lyc', 'eje': 'Comunicación Oral', 'numero': 21,
             'descripcion': 'Participar activamente en conversaciones grupales.',
             'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
        ]
        
        for oa_data in oas:
            indicadores = [IndicadorEvaluacion(**ind) for ind in oa_data.get('indicadores', [])]
            ObjetivoAprendizaje.objects(codigo=oa_data['codigo']).update_one(
                upsert=True,
                set__nivel=oa_data['nivel'],
                set__asignatura=oa_data['asignatura'],
                set__eje=oa_data['eje'],
                set__numero=oa_data['numero'],
                set__descripcion=oa_data['descripcion'],
                set__priorizado_2025=oa_data.get('priorizado_2025', False),
                set__nivel_priorizacion=oa_data.get('nivel_priorizacion'),
                set__indicadores=indicadores
            )
        
        # Unidades
        unidades = [
            {'codigo': '1b-Lyc-U1', 'nivel': '1b', 'asignatura': 'Lyc', 'numero': 1,
             'nombre': 'Descubriendo el lenguaje',
             'descripcion': 'Iniciación a la lectura y escritura.',
             'oa_codigos': ['1b-Lyc-OA01', '1b-Lyc-OA02', '1b-Lyc-OA03', '1b-Lyc-OA18'],
             'oat_codigos': ['OAT-COG-01', 'OAT-COG-03'],
             'habilidades_codigos': ['1b-Lyc-HAB01', '1b-Lyc-HAB02', '1b-Lyc-HAB03'],
             'actitudes_codigos': ['Lyc-ACT01', 'Lyc-ACT02'],
             'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True},
            {'codigo': '1b-Lyc-U2', 'nivel': '1b', 'asignatura': 'Lyc', 'numero': 2,
             'nombre': 'Leyendo mis primeras palabras',
             'descripcion': 'Desarrollo de la lectura de palabras y textos breves.',
             'oa_codigos': ['1b-Lyc-OA04', '1b-Lyc-OA05', '1b-Lyc-OA21'],
             'oat_codigos': ['OAT-COG-02', 'OAT-AFE-01'],
             'habilidades_codigos': ['1b-Lyc-HAB03', '1b-Lyc-HAB04'],
             'actitudes_codigos': ['Lyc-ACT01', 'Lyc-ACT03'],
             'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True},
            {'codigo': '1b-Lyc-U3', 'nivel': '1b', 'asignatura': 'Lyc', 'numero': 3,
             'nombre': 'Escribiendo para comunicar',
             'descripcion': 'Iniciación a la escritura de oraciones.',
             'oa_codigos': ['1b-Lyc-OA13', '1b-Lyc-OA14'],
             'oat_codigos': ['OAT-COG-03', 'OAT-SOC-02'],
             'habilidades_codigos': ['1b-Lyc-HAB01', '1b-Lyc-HAB04'],
             'actitudes_codigos': ['Lyc-ACT02', 'TRANS-ACT01'],
             'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
            {'codigo': '1b-Lyc-U4', 'nivel': '1b', 'asignatura': 'Lyc', 'numero': 4,
             'nombre': 'Comunicándonos con los demás',
             'descripcion': 'Desarrollo de comunicación oral.',
             'oa_codigos': ['1b-Lyc-OA18', '1b-Lyc-OA21'],
             'oat_codigos': ['OAT-SOC-01', 'OAT-SOC-02'],
             'habilidades_codigos': ['1b-Lyc-HAB01'],
             'actitudes_codigos': ['Lyc-ACT03', 'TRANS-ACT02', 'TRANS-ACT03'],
             'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
        ]
        
        for u_data in unidades:
            UnidadCurricular.objects(codigo=u_data['codigo']).update_one(
                upsert=True,
                set__nivel=u_data['nivel'],
                set__asignatura=u_data['asignatura'],
                set__numero=u_data['numero'],
                set__nombre=u_data['nombre'],
                set__descripcion=u_data['descripcion'],
                set__oa_codigos=u_data['oa_codigos'],
                set__oat_codigos=u_data['oat_codigos'],
                set__habilidades_codigos=u_data['habilidades_codigos'],
                set__actitudes_codigos=u_data['actitudes_codigos'],
                set__horas_sugeridas=u_data['horas_sugeridas'],
                set__semanas_sugeridas=u_data['semanas_sugeridas'],
                set__priorizado_2025=u_data['priorizado_2025']
            )
        
        self.stdout.write(f'  → {len(oas)} OAs, {len(unidades)} unidades')
