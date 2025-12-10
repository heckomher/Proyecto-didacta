"""
Datos del Currículum Nacional Chileno - Ciencias Naturales 1°-8° Básico Completo
"""

# ==========================================
# CIENCIAS NATURALES - EDUCACIÓN BÁSICA COMPLETO
# ==========================================

CIENCIAS_ACTITUDES = [
    {'codigo': 'Cna-ACT01', 'asignatura': 'Cna', 'numero': 1,
     'descripcion': 'Demostrar curiosidad e interés por conocer fenómenos naturales.'},
    {'codigo': 'Cna-ACT02', 'asignatura': 'Cna', 'numero': 2,
     'descripcion': 'Manifestar un estilo de trabajo riguroso y perseverante.'},
    {'codigo': 'Cna-ACT03', 'asignatura': 'Cna', 'numero': 3,
     'descripcion': 'Reconocer la importancia del entorno natural y sus recursos.'},
    {'codigo': 'Cna-ACT04', 'asignatura': 'Cna', 'numero': 4,
     'descripcion': 'Asumir responsabilidades e interactuar en forma colaborativa.'},
]

# 1° Básico - Ciencias
CIENCIAS_1B_OAS = [
    {'codigo': '1b-Cna-OA01', 'nivel': '1b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 1,
     'descripcion': 'Reconocer y observar que los seres vivos crecen, responden a estímulos, se reproducen y necesitan agua, alimento y aire.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '1b-Cna-OA03', 'nivel': '1b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 3,
     'descripcion': 'Observar e identificar las estructuras principales de las plantas: hojas, flores, tallos y raíces.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '1b-Cna-OA05', 'nivel': '1b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 5,
     'descripcion': 'Reconocer y comparar diversas plantas y animales de nuestro país.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
    {'codigo': '1b-Cna-OA07', 'nivel': '1b', 'asignatura': 'Cna', 'eje': 'Ciencias Físicas y Químicas', 'numero': 7,
     'descripcion': 'Describir y agrupar los materiales según sus propiedades.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
    {'codigo': '1b-Cna-OA09', 'nivel': '1b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Tierra y el Universo', 'numero': 9,
     'descripcion': 'Describir y comunicar los cambios del ciclo diario y las estaciones del año.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

CIENCIAS_1B_UNIDADES = [
    {'codigo': '1b-Cna-U1', 'nivel': '1b', 'asignatura': 'Cna', 'numero': 1, 'nombre': 'Los seres vivos',
     'descripcion': 'Características de los seres vivos.',
     'oa_codigos': ['1b-Cna-OA01', '1b-Cna-OA03'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT01', 'Cna-ACT03'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '1b-Cna-U2', 'nivel': '1b', 'asignatura': 'Cna', 'numero': 2, 'nombre': 'Plantas y animales de Chile',
     'descripcion': 'Diversidad de flora y fauna chilena.',
     'oa_codigos': ['1b-Cna-OA05'], 'oat_codigos': ['OAT-SOC-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT03'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '1b-Cna-U3', 'nivel': '1b', 'asignatura': 'Cna', 'numero': 3, 'nombre': 'Los materiales',
     'descripcion': 'Propiedades de los materiales.',
     'oa_codigos': ['1b-Cna-OA07'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT01', 'Cna-ACT02'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '1b-Cna-U4', 'nivel': '1b', 'asignatura': 'Cna', 'numero': 4, 'nombre': 'El día y las estaciones',
     'descripcion': 'Ciclos diarios y anuales.',
     'oa_codigos': ['1b-Cna-OA09'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

# 2° Básico - Ciencias
CIENCIAS_2B_OAS = [
    {'codigo': '2b-Cna-OA01', 'nivel': '2b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 1,
     'descripcion': 'Observar y describir los cambios de los seres vivos durante su ciclo de vida.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '2b-Cna-OA03', 'nivel': '2b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 3,
     'descripcion': 'Observar y describir hábitats de Chile y del mundo.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '2b-Cna-OA07', 'nivel': '2b', 'asignatura': 'Cna', 'eje': 'Ciencias Físicas y Químicas', 'numero': 7,
     'descripcion': 'Describir que el agua puede encontrarse en la naturaleza en diferentes estados.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '2b-Cna-OA10', 'nivel': '2b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Tierra y el Universo', 'numero': 10,
     'descripcion': 'Describir el tiempo atmosférico y medir algunos de sus elementos.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
]

CIENCIAS_2B_UNIDADES = [
    {'codigo': '2b-Cna-U1', 'nivel': '2b', 'asignatura': 'Cna', 'numero': 1, 'nombre': 'Ciclos de vida',
     'descripcion': 'Cambios en los seres vivos durante su vida.',
     'oa_codigos': ['2b-Cna-OA01'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT01'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '2b-Cna-U2', 'nivel': '2b', 'asignatura': 'Cna', 'numero': 2, 'nombre': 'Hábitats',
     'descripcion': 'Hábitats de Chile y el mundo.',
     'oa_codigos': ['2b-Cna-OA03'], 'oat_codigos': ['OAT-COG-01', 'OAT-SOC-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT03'],
     'horas_sugeridas': 45, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '2b-Cna-U3', 'nivel': '2b', 'asignatura': 'Cna', 'numero': 3, 'nombre': 'Estados del agua',
     'descripcion': 'El agua en diferentes estados.',
     'oa_codigos': ['2b-Cna-OA07'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT02'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '2b-Cna-U4', 'nivel': '2b', 'asignatura': 'Cna', 'numero': 4, 'nombre': 'El tiempo atmosférico',
     'descripcion': 'Descripción y medición del clima.',
     'oa_codigos': ['2b-Cna-OA10'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT01', 'Cna-ACT02'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

# 3° Básico - Ciencias
CIENCIAS_3B_OAS = [
    {'codigo': '3b-Cna-OA01', 'nivel': '3b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 1,
     'descripcion': 'Observar y describir las características de las plantas y sus estructuras.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '3b-Cna-OA04', 'nivel': '3b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 4,
     'descripcion': 'Describir la importancia de las plantas para los seres vivos y el medio ambiente.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '3b-Cna-OA07', 'nivel': '3b', 'asignatura': 'Cna', 'eje': 'Ciencias Físicas y Químicas', 'numero': 7,
     'descripcion': 'Distinguir fuentes naturales y artificiales de luz.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
    {'codigo': '3b-Cna-OA10', 'nivel': '3b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Tierra y el Universo', 'numero': 10,
     'descripcion': 'Reconocer y describir los componentes del Sistema Solar.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

CIENCIAS_3B_UNIDADES = [
    {'codigo': '3b-Cna-U1', 'nivel': '3b', 'asignatura': 'Cna', 'numero': 1, 'nombre': 'Las plantas',
     'descripcion': 'Características y estructuras de las plantas.',
     'oa_codigos': ['3b-Cna-OA01', '3b-Cna-OA04'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT01', 'Cna-ACT03'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '3b-Cna-U2', 'nivel': '3b', 'asignatura': 'Cna', 'numero': 2, 'nombre': 'La luz',
     'descripcion': 'Fuentes de luz y sombras.',
     'oa_codigos': ['3b-Cna-OA07'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT02'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '3b-Cna-U3', 'nivel': '3b', 'asignatura': 'Cna', 'numero': 3, 'nombre': 'El Sistema Solar',
     'descripcion': 'Componentes del Sistema Solar.',
     'oa_codigos': ['3b-Cna-OA10'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT01'],
     'horas_sugeridas': 45, 'semanas_sugeridas': 6, 'priorizado_2025': True},
]

# 4° Básico - Ciencias
CIENCIAS_4B_OAS = [
    {'codigo': '4b-Cna-OA01', 'nivel': '4b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 1,
     'descripcion': 'Reconocer que los seres vivos interactúan con el ambiente y otros seres vivos en ecosistemas.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '4b-Cna-OA04', 'nivel': '4b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 4,
     'descripcion': 'Analizar los efectos de la actividad humana sobre los ecosistemas.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '4b-Cna-OA08', 'nivel': '4b', 'asignatura': 'Cna', 'eje': 'Ciencias Físicas y Químicas', 'numero': 8,
     'descripcion': 'Demostrar experimentalmente que la materia tiene masa y ocupa espacio.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '4b-Cna-OA11', 'nivel': '4b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Tierra y el Universo', 'numero': 11,
     'descripcion': 'Describir el movimiento de rotación y traslación de la Tierra.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

CIENCIAS_4B_UNIDADES = [
    {'codigo': '4b-Cna-U1', 'nivel': '4b', 'asignatura': 'Cna', 'numero': 1, 'nombre': 'Los ecosistemas',
     'descripcion': 'Interacciones en los ecosistemas.',
     'oa_codigos': ['4b-Cna-OA01', '4b-Cna-OA04'], 'oat_codigos': ['OAT-COG-01', 'OAT-SOC-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT03'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '4b-Cna-U2', 'nivel': '4b', 'asignatura': 'Cna', 'numero': 2, 'nombre': 'La materia',
     'descripcion': 'Propiedades de la materia.',
     'oa_codigos': ['4b-Cna-OA08'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT02'],
     'horas_sugeridas': 45, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '4b-Cna-U3', 'nivel': '4b', 'asignatura': 'Cna', 'numero': 3, 'nombre': 'La Tierra y sus movimientos',
     'descripcion': 'Movimientos de rotación y traslación.',
     'oa_codigos': ['4b-Cna-OA11'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT01'],
     'horas_sugeridas': 45, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

# 5° Básico - Ciencias
CIENCIAS_5B_OAS = [
    {'codigo': '5b-Cna-OA01', 'nivel': '5b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 1,
     'descripcion': 'Reconocer y explicar que los seres vivos están formados por una o más células.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '5b-Cna-OA04', 'nivel': '5b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 4,
     'descripcion': 'Analizar las relaciones alimentarias en un ecosistema.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '5b-Cna-OA09', 'nivel': '5b', 'asignatura': 'Cna', 'eje': 'Ciencias Físicas y Químicas', 'numero': 9,
     'descripcion': 'Medir y registrar el volumen de objetos, usando unidades de medida estandarizadas.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
    {'codigo': '5b-Cna-OA12', 'nivel': '5b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Tierra y el Universo', 'numero': 12,
     'descripcion': 'Describir el ciclo del agua en la naturaleza.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

CIENCIAS_5B_UNIDADES = [
    {'codigo': '5b-Cna-U1', 'nivel': '5b', 'asignatura': 'Cna', 'numero': 1, 'nombre': 'La célula',
     'descripcion': 'Estructura celular básica.',
     'oa_codigos': ['5b-Cna-OA01'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT01'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '5b-Cna-U2', 'nivel': '5b', 'asignatura': 'Cna', 'numero': 2, 'nombre': 'Cadenas alimentarias',
     'descripcion': 'Relaciones alimentarias en ecosistemas.',
     'oa_codigos': ['5b-Cna-OA04'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT03'],
     'horas_sugeridas': 45, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '5b-Cna-U3', 'nivel': '5b', 'asignatura': 'Cna', 'numero': 3, 'nombre': 'Medición y materiales',
     'descripcion': 'Volumen y propiedades de materiales.',
     'oa_codigos': ['5b-Cna-OA09'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT02'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '5b-Cna-U4', 'nivel': '5b', 'asignatura': 'Cna', 'numero': 4, 'nombre': 'El ciclo del agua',
     'descripcion': 'Ciclo hidrológico.',
     'oa_codigos': ['5b-Cna-OA12'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT03'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

# 6° Básico - Ciencias
CIENCIAS_6B_OAS = [
    {'codigo': '6b-Cna-OA01', 'nivel': '6b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 1,
     'descripcion': 'Explicar la fotosíntesis y la respiración en plantas, y sus efectos en el ambiente.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '6b-Cna-OA05', 'nivel': '6b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 5,
     'descripcion': 'Identificar y describir las funciones de las principales estructuras del cuerpo humano.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '6b-Cna-OA10', 'nivel': '6b', 'asignatura': 'Cna', 'eje': 'Ciencias Físicas y Químicas', 'numero': 10,
     'descripcion': 'Demostrar que la energía se puede transformar de una forma a otra.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '6b-Cna-OA14', 'nivel': '6b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Tierra y el Universo', 'numero': 14,
     'descripcion': 'Explicar las capas de la Tierra y los procesos geológicos.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

CIENCIAS_6B_UNIDADES = [
    {'codigo': '6b-Cna-U1', 'nivel': '6b', 'asignatura': 'Cna', 'numero': 1, 'nombre': 'Fotosíntesis y respiración',
     'descripcion': 'Procesos vitales en plantas.',
     'oa_codigos': ['6b-Cna-OA01'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT01', 'Cna-ACT03'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '6b-Cna-U2', 'nivel': '6b', 'asignatura': 'Cna', 'numero': 2, 'nombre': 'El cuerpo humano',
     'descripcion': 'Sistemas del cuerpo humano.',
     'oa_codigos': ['6b-Cna-OA05'], 'oat_codigos': ['OAT-AFE-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT01'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '6b-Cna-U3', 'nivel': '6b', 'asignatura': 'Cna', 'numero': 3, 'nombre': 'La energía',
     'descripcion': 'Transformaciones de energía.',
     'oa_codigos': ['6b-Cna-OA10'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT02'],
     'horas_sugeridas': 45, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '6b-Cna-U4', 'nivel': '6b', 'asignatura': 'Cna', 'numero': 4, 'nombre': 'Capas de la Tierra',
     'descripcion': 'Estructura y procesos geológicos.',
     'oa_codigos': ['6b-Cna-OA14'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT03'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

# 7° Básico - Ciencias
CIENCIAS_7B_OAS = [
    {'codigo': '7b-Cna-OA01', 'nivel': '7b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 1,
     'descripcion': 'Explicar la organización de los seres vivos: célula, tejido, órgano, sistema, organismo.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '7b-Cna-OA05', 'nivel': '7b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 5,
     'descripcion': 'Describir las características de las sustancias puras y mezclas.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '7b-Cna-OA11', 'nivel': '7b', 'asignatura': 'Cna', 'eje': 'Ciencias Físicas y Químicas', 'numero': 11,
     'descripcion': 'Describir la fuerza y sus efectos en los objetos en situaciones cotidianas.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '7b-Cna-OA15', 'nivel': '7b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Tierra y el Universo', 'numero': 15,
     'descripcion': 'Investigar y explicar los efectos de la actividad humana sobre el medio ambiente.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

CIENCIAS_7B_UNIDADES = [
    {'codigo': '7b-Cna-U1', 'nivel': '7b', 'asignatura': 'Cna', 'numero': 1, 'nombre': 'Organización de los seres vivos',
     'descripcion': 'Niveles de organización biológica.',
     'oa_codigos': ['7b-Cna-OA01'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT01'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '7b-Cna-U2', 'nivel': '7b', 'asignatura': 'Cna', 'numero': 2, 'nombre': 'Sustancias y mezclas',
     'descripcion': 'Clasificación de la materia.',
     'oa_codigos': ['7b-Cna-OA05'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT02'],
     'horas_sugeridas': 45, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '7b-Cna-U3', 'nivel': '7b', 'asignatura': 'Cna', 'numero': 3, 'nombre': 'Fuerza y movimiento',
     'descripcion': 'Efectos de las fuerzas.',
     'oa_codigos': ['7b-Cna-OA11'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT02'],
     'horas_sugeridas': 45, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '7b-Cna-U4', 'nivel': '7b', 'asignatura': 'Cna', 'numero': 4, 'nombre': 'Impacto ambiental',
     'descripcion': 'Efectos humanos en el medio ambiente.',
     'oa_codigos': ['7b-Cna-OA15'], 'oat_codigos': ['OAT-SOC-01', 'OAT-MOR-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT03', 'Cna-ACT04'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

# 8° Básico - Ciencias (con articulaciones)
CIENCIAS_8B_OAS = [
    {'codigo': '8b-Cna-OA01', 'nivel': '8b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 1,
     'descripcion': 'Explicar, basándose en evidencias, que la célula es la unidad estructural y funcional de los seres vivos.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '8b-Cna-OA04', 'nivel': '8b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 4,
     'descripcion': 'Crear modelos que expliquen la reproducción celular.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '8b-Cna-OA06', 'nivel': '8b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 6,
     'descripcion': 'Investigar las características de los nutrientes y sus efectos para la salud.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': [],
     'articulaciones': [{'asignatura_codigo': 'Efs', 'asignatura_nombre': 'Educación Física y Salud', 'descripcion': 'Nutrición y actividad física'}]},
    {'codigo': '8b-Cna-OA08', 'nivel': '8b', 'asignatura': 'Cna', 'eje': 'Ciencias Físicas y Químicas', 'numero': 8,
     'descripcion': 'Desarrollar modelos sobre la conservación de la masa en cambios químicos.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '8b-Cna-OA13', 'nivel': '8b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Tierra y el Universo', 'numero': 13,
     'descripcion': 'Describir los procesos de formación y extinción de especies.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
]

CIENCIAS_8B_UNIDADES = [
    {'codigo': '8b-Cna-U1', 'nivel': '8b', 'asignatura': 'Cna', 'numero': 1, 'nombre': 'La célula',
     'descripcion': 'Estructura y función celular.',
     'oa_codigos': ['8b-Cna-OA01', '8b-Cna-OA04'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT01'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '8b-Cna-U2', 'nivel': '8b', 'asignatura': 'Cna', 'numero': 2, 'nombre': 'Nutrición y salud',
     'descripcion': 'Nutrientes y alimentación saludable. ARTICULABLE CON ED. FÍSICA.',
     'oa_codigos': ['8b-Cna-OA06'], 'oat_codigos': ['OAT-AFE-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT03'],
     'horas_sugeridas': 45, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '8b-Cna-U3', 'nivel': '8b', 'asignatura': 'Cna', 'numero': 3, 'nombre': 'Cambios de la materia',
     'descripcion': 'Conservación de la masa.',
     'oa_codigos': ['8b-Cna-OA08'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT02'],
     'horas_sugeridas': 45, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '8b-Cna-U4', 'nivel': '8b', 'asignatura': 'Cna', 'numero': 4, 'nombre': 'Evolución y biodiversidad',
     'descripcion': 'Formación y extinción de especies.',
     'oa_codigos': ['8b-Cna-OA13'], 'oat_codigos': ['OAT-COG-01', 'OAT-SOC-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT01', 'Cna-ACT03'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

# Consolidar Ciencias
CIENCIAS_BASICA_COMPLETA = {
    'actitudes': CIENCIAS_ACTITUDES,
    'niveles': {
        '1b': {'oas': CIENCIAS_1B_OAS, 'unidades': CIENCIAS_1B_UNIDADES},
        '2b': {'oas': CIENCIAS_2B_OAS, 'unidades': CIENCIAS_2B_UNIDADES},
        '3b': {'oas': CIENCIAS_3B_OAS, 'unidades': CIENCIAS_3B_UNIDADES},
        '4b': {'oas': CIENCIAS_4B_OAS, 'unidades': CIENCIAS_4B_UNIDADES},
        '5b': {'oas': CIENCIAS_5B_OAS, 'unidades': CIENCIAS_5B_UNIDADES},
        '6b': {'oas': CIENCIAS_6B_OAS, 'unidades': CIENCIAS_6B_UNIDADES},
        '7b': {'oas': CIENCIAS_7B_OAS, 'unidades': CIENCIAS_7B_UNIDADES},
        '8b': {'oas': CIENCIAS_8B_OAS, 'unidades': CIENCIAS_8B_UNIDADES},
    }
}
