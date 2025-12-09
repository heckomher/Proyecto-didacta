"""
Comando para poblar la base de datos con asignaturas del currículum nacional chileno
según las Bases Curriculares del Ministerio de Educación de Chile.
"""
from django.core.management.base import BaseCommand
from main.models import Asignatura, NivelEducativo

class Command(BaseCommand):
    help = 'Pobla la base de datos con asignaturas del currículum educacional chileno'

    # Asignaturas según el currículum nacional chileno
    ASIGNATURAS_CHILE = {
        'Educación Parvularia': [
            'Ámbito: Desarrollo Personal y Social',
            'Ámbito: Comunicación Integral',
            'Ámbito: Interacción y Comprensión del Entorno',
        ],
        'Educación Básica': [
            # Obligatorias (1° a 8° básico)
            'Lengua y Literatura',
            'Matemática',
            'Historia, Geografía y Ciencias Sociales',
            'Ciencias Naturales',
            'Inglés',
            'Educación Física y Salud',
            'Artes Visuales',
            'Música',
            'Tecnología',
            'Orientación',
            # Religión (optativa)
            'Religión',
        ],
        'Educación Media': [
            # Plan Común (1° y 2° medio)
            'Lengua y Literatura',
            'Matemática',
            'Historia, Geografía y Ciencias Sociales',
            'Inglés',
            'Educación Física y Salud',
            'Ciencias Naturales: Biología',
            'Ciencias Naturales: Química',
            'Ciencias Naturales: Física',
            'Artes: Artes Visuales',
            'Artes: Música',
            'Tecnología',
            'Orientación',
            'Religión',
            
            # 3° y 4° medio - Plan Común Diferenciado
            'Educación Ciudadana',
            'Filosofía',
            'Ciencias para la Ciudadanía',
            
            # Electivos de profundización (3° y 4° medio)
            'Límites, Derivadas e Integrales',
            'Probabilidades y Estadística Descriptiva e Inferencial',
            'Geometría 3D',
            'Participación y Argumentación en Democracia',
            'Comprensión Histórica del Presente',
            'Economía y Sociedad',
            'Geografía, Territorio y Desafíos Socioambientales',
            'Biología Celular y Molecular',
            'Ciencias de la Salud',
            'Biología de los Ecosistemas',
            'Química',
            'Física',
            'Ciencias del Ejercicio Físico y Deportivo',
            'Interpretación y Creación en Danza',
            'Creación y Composición Musical',
            'Interpretación Musical',
            'Artes Visuales, Audiovisuales y Multimediales',
            'Diseño y Arquitectura',
            'Participación y Argumentación en Democracia (profundización)',
            'Lectura y Escritura Especializadas',
            'Literatura e Identidad',
            'Inglés',
            
            # Asignaturas técnico-profesionales
            'Módulo Técnico Profesional 1',
            'Módulo Técnico Profesional 2',
            'Módulo Técnico Profesional 3',
            'Módulo Técnico Profesional 4',
        ],
        'Educación de Adultos': [
            'Lengua Castellana y Comunicación',
            'Matemática',
            'Estudios Sociales',
            'Ciencias Naturales',
            'Inglés',
            'Consumo y Calidad de Vida',
            'Convivencia Social',
        ],
    }

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando población de asignaturas chilenas...'))
        
        creadas = 0
        existentes = 0
        errores = 0

        # Obtener o crear niveles educativos
        niveles = {}
        for nombre_nivel in self.ASIGNATURAS_CHILE.keys():
            nivel, created = NivelEducativo.objects.get_or_create(
                nombre=nombre_nivel,
                defaults={'descripcion': f'Nivel educativo: {nombre_nivel}'}
            )
            niveles[nombre_nivel] = nivel
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Nivel creado: {nombre_nivel}'))

        # Crear asignaturas
        for nivel_nombre, asignaturas in self.ASIGNATURAS_CHILE.items():
            self.stdout.write(self.style.WARNING(f'\n{nivel_nombre}:'))
            
            for asignatura_nombre in asignaturas:
                try:
                    asignatura, created = Asignatura.objects.get_or_create(
                        nombre_asignatura=asignatura_nombre,
                        defaults={
                            'descripcion': f'Asignatura del currículum nacional chileno - {nivel_nombre}'
                        }
                    )
                    
                    if created:
                        creadas += 1
                        self.stdout.write(self.style.SUCCESS(f'  ✓ {asignatura_nombre}'))
                    else:
                        existentes += 1
                        self.stdout.write(self.style.WARNING(f'  - {asignatura_nombre} (ya existe)'))
                        
                except Exception as e:
                    errores += 1
                    self.stdout.write(self.style.ERROR(f'  ✗ Error en {asignatura_nombre}: {str(e)}'))

        # Resumen
        self.stdout.write(self.style.SUCCESS(f'\n{"="*60}'))
        self.stdout.write(self.style.SUCCESS(f'Resumen:'))
        self.stdout.write(self.style.SUCCESS(f'  Asignaturas creadas: {creadas}'))
        self.stdout.write(self.style.WARNING(f'  Asignaturas existentes: {existentes}'))
        if errores > 0:
            self.stdout.write(self.style.ERROR(f'  Errores: {errores}'))
        self.stdout.write(self.style.SUCCESS(f'{"="*60}\n'))
        
        self.stdout.write(self.style.SUCCESS('✓ Proceso completado'))
