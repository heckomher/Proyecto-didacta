"""
Datos del Currículum Nacional Chileno - Historia, Geografía y Cs. Sociales 1°-8° Básico
"""

# ==========================================
# HISTORIA, GEOGRAFÍA Y CS. SOCIALES - BÁSICA COMPLETO
# ==========================================

HISTORIA_ACTITUDES = [
    {'codigo': 'His-ACT01', 'asignatura': 'His', 'numero': 1,
     'descripcion': 'Demostrar valoración por la vida en sociedad.'},
    {'codigo': 'His-ACT02', 'asignatura': 'His', 'numero': 2,
     'descripcion': 'Comportarse según principios y virtudes ciudadanas.'},
    {'codigo': 'His-ACT03', 'asignatura': 'His', 'numero': 3,
     'descripcion': 'Establecer lazos de pertenencia con su entorno.'},
    {'codigo': 'His-ACT04', 'asignatura': 'His', 'numero': 4,
     'descripcion': 'Respetar y defender la igualdad de derechos.'},
]

# 1° Básico - Historia
HISTORIA_1B_OAS = [
    {'codigo': '1b-His-OA01', 'nivel': '1b', 'asignatura': 'His', 'eje': 'Historia', 'numero': 1,
     'descripcion': 'Nombrar y secuenciar días de la semana y meses del año.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '1b-His-OA05', 'nivel': '1b', 'asignatura': 'His', 'eje': 'Geografía', 'numero': 5,
     'descripcion': 'Reconocer los símbolos representativos de Chile.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '1b-His-OA08', 'nivel': '1b', 'asignatura': 'His', 'eje': 'Formación Ciudadana', 'numero': 8,
     'descripcion': 'Reconocer que los niños tienen derechos.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '1b-His-OA10', 'nivel': '1b', 'asignatura': 'His', 'eje': 'Formación Ciudadana', 'numero': 10,
     'descripcion': 'Reconocer la importancia y el servicio que prestan instituciones públicas.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
]

HISTORIA_1B_UNIDADES = [
    {'codigo': '1b-His-U1', 'nivel': '1b', 'asignatura': 'His', 'numero': 1, 'nombre': 'El tiempo',
     'descripcion': 'Secuencias temporales y calendario.',
     'oa_codigos': ['1b-His-OA01'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT01'],
     'horas_sugeridas': 30, 'semanas_sugeridas': 4, 'priorizado_2025': True},
    {'codigo': '1b-His-U2', 'nivel': '1b', 'asignatura': 'His', 'numero': 2, 'nombre': 'Identidad nacional',
     'descripcion': 'Símbolos patrios y pertenencia.',
     'oa_codigos': ['1b-His-OA05'], 'oat_codigos': ['OAT-SOC-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT03'],
     'horas_sugeridas': 30, 'semanas_sugeridas': 4, 'priorizado_2025': True},
    {'codigo': '1b-His-U3', 'nivel': '1b', 'asignatura': 'His', 'numero': 3, 'nombre': 'Derechos del niño',
     'descripcion': 'Derechos y deberes básicos.',
     'oa_codigos': ['1b-His-OA08', '1b-His-OA10'], 'oat_codigos': ['OAT-MOR-01', 'OAT-SOC-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT02', 'His-ACT04'],
     'horas_sugeridas': 35, 'semanas_sugeridas': 4, 'priorizado_2025': True},
]

# 2° Básico - Historia
HISTORIA_2B_OAS = [
    {'codigo': '2b-His-OA01', 'nivel': '2b', 'asignatura': 'His', 'eje': 'Historia', 'numero': 1,
     'descripcion': 'Describir los modos de vida de algunos pueblos originarios de Chile.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '2b-His-OA04', 'nivel': '2b', 'asignatura': 'His', 'eje': 'Geografía', 'numero': 4,
     'descripcion': 'Leer y comunicar información geográfica a través de representaciones.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '2b-His-OA08', 'nivel': '2b', 'asignatura': 'His', 'eje': 'Formación Ciudadana', 'numero': 8,
     'descripcion': 'Mostrar actitudes y realizar acciones de respeto hacia los demás.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

HISTORIA_2B_UNIDADES = [
    {'codigo': '2b-His-U1', 'nivel': '2b', 'asignatura': 'His', 'numero': 1, 'nombre': 'Pueblos originarios',
     'descripcion': 'Pueblos originarios de Chile.',
     'oa_codigos': ['2b-His-OA01'], 'oat_codigos': ['OAT-SOC-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT03'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '2b-His-U2', 'nivel': '2b', 'asignatura': 'His', 'numero': 2, 'nombre': 'Representaciones geográficas',
     'descripcion': 'Mapas y puntos cardinales.',
     'oa_codigos': ['2b-His-OA04'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT01'],
     'horas_sugeridas': 35, 'semanas_sugeridas': 4, 'priorizado_2025': True},
    {'codigo': '2b-His-U3', 'nivel': '2b', 'asignatura': 'His', 'numero': 3, 'nombre': 'Convivencia',
     'descripcion': 'Respeto y buena convivencia.',
     'oa_codigos': ['2b-His-OA08'], 'oat_codigos': ['OAT-MOR-01', 'OAT-SOC-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT02', 'His-ACT04'],
     'horas_sugeridas': 30, 'semanas_sugeridas': 4, 'priorizado_2025': True},
]

# 3° Básico - Historia
HISTORIA_3B_OAS = [
    {'codigo': '3b-His-OA01', 'nivel': '3b', 'asignatura': 'His', 'eje': 'Historia', 'numero': 1,
     'descripcion': 'Reconocer aspectos de la vida cotidiana de la civilización griega.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '3b-His-OA03', 'nivel': '3b', 'asignatura': 'His', 'eje': 'Historia', 'numero': 3,
     'descripcion': 'Explicar la importancia de los aportes de griegos y romanos a nuestra cultura.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '3b-His-OA08', 'nivel': '3b', 'asignatura': 'His', 'eje': 'Geografía', 'numero': 8,
     'descripcion': 'Caracterizar el entorno geográfico de las civilizaciones estudiadas.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
]

HISTORIA_3B_UNIDADES = [
    {'codigo': '3b-His-U1', 'nivel': '3b', 'asignatura': 'His', 'numero': 1, 'nombre': 'Grecia antigua',
     'descripcion': 'Civilización griega.',
     'oa_codigos': ['3b-His-OA01', '3b-His-OA03'], 'oat_codigos': ['OAT-SOC-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT01', 'His-ACT03'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '3b-His-U2', 'nivel': '3b', 'asignatura': 'His', 'numero': 2, 'nombre': 'Geografía de la antigüedad',
     'descripcion': 'Entorno geográfico de las civilizaciones.',
     'oa_codigos': ['3b-His-OA08'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

# 4° Básico - Historia
HISTORIA_4B_OAS = [
    {'codigo': '4b-His-OA01', 'nivel': '4b', 'asignatura': 'His', 'eje': 'Historia', 'numero': 1,
     'descripcion': 'Describir la civilización maya, inca y azteca.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '4b-His-OA05', 'nivel': '4b', 'asignatura': 'His', 'eje': 'Geografía', 'numero': 5,
     'descripcion': 'Describir características físicas del paisaje de Chile.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '4b-His-OA10', 'nivel': '4b', 'asignatura': 'His', 'eje': 'Formación Ciudadana', 'numero': 10,
     'descripcion': 'Explicar por qué los seres humanos tenemos derechos.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

HISTORIA_4B_UNIDADES = [
    {'codigo': '4b-His-U1', 'nivel': '4b', 'asignatura': 'His', 'numero': 1, 'nombre': 'Civilizaciones americanas',
     'descripcion': 'Mayas, incas y aztecas.',
     'oa_codigos': ['4b-His-OA01'], 'oat_codigos': ['OAT-SOC-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT03'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '4b-His-U2', 'nivel': '4b', 'asignatura': 'His', 'numero': 2, 'nombre': 'Geografía de Chile',
     'descripcion': 'Paisajes y zonas de Chile.',
     'oa_codigos': ['4b-His-OA05'], 'oat_codigos': ['OAT-COG-01', 'OAT-SOC-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT03'],
     'horas_sugeridas': 45, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '4b-His-U3', 'nivel': '4b', 'asignatura': 'His', 'numero': 3, 'nombre': 'Derechos humanos',
     'descripcion': 'Fundamentos de los derechos.',
     'oa_codigos': ['4b-His-OA10'], 'oat_codigos': ['OAT-MOR-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT04'],
     'horas_sugeridas': 35, 'semanas_sugeridas': 4, 'priorizado_2025': True},
]

# 5° Básico - Historia
HISTORIA_5B_OAS = [
    {'codigo': '5b-His-OA01', 'nivel': '5b', 'asignatura': 'His', 'eje': 'Historia', 'numero': 1,
     'descripcion': 'Explicar los viajes de descubrimiento de Cristóbal Colón.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '5b-His-OA04', 'nivel': '5b', 'asignatura': 'His', 'eje': 'Historia', 'numero': 4,
     'descripcion': 'Investigar sobre los efectos de la conquista para los pueblos originarios.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '5b-His-OA09', 'nivel': '5b', 'asignatura': 'His', 'eje': 'Geografía', 'numero': 9,
     'descripcion': 'Caracterizar los principales recursos naturales de Chile.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '5b-His-OA14', 'nivel': '5b', 'asignatura': 'His', 'eje': 'Formación Ciudadana', 'numero': 14,
     'descripcion': 'Reconocer que todos los niños tienen derechos garantizados por la ley.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
]

HISTORIA_5B_UNIDADES = [
    {'codigo': '5b-His-U1', 'nivel': '5b', 'asignatura': 'His', 'numero': 1, 'nombre': 'Descubrimiento y conquista',
     'descripcion': 'Viajes de descubrimiento y conquista de América.',
     'oa_codigos': ['5b-His-OA01', '5b-His-OA04'], 'oat_codigos': ['OAT-SOC-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT01', 'His-ACT03'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '5b-His-U2', 'nivel': '5b', 'asignatura': 'His', 'numero': 2, 'nombre': 'Recursos naturales',
     'descripcion': 'Recursos de Chile.',
     'oa_codigos': ['5b-His-OA09'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT03'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '5b-His-U3', 'nivel': '5b', 'asignatura': 'His', 'numero': 3, 'nombre': 'Derechos del niño',
     'descripcion': 'Derechos garantizados.',
     'oa_codigos': ['5b-His-OA14'], 'oat_codigos': ['OAT-MOR-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT04'],
     'horas_sugeridas': 35, 'semanas_sugeridas': 4, 'priorizado_2025': True},
]

# 6° Básico - Historia
HISTORIA_6B_OAS = [
    {'codigo': '6b-His-OA01', 'nivel': '6b', 'asignatura': 'His', 'eje': 'Historia', 'numero': 1,
     'descripcion': 'Explicar los factores que propiciaron la independencia de Chile.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '6b-His-OA05', 'nivel': '6b', 'asignatura': 'His', 'eje': 'Historia', 'numero': 5,
     'descripcion': 'Describir cómo se organizó la república de Chile en el siglo XIX.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '6b-His-OA12', 'nivel': '6b', 'asignatura': 'His', 'eje': 'Geografía', 'numero': 12,
     'descripcion': 'Comparar diversos ambientes naturales de Chile.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
    {'codigo': '6b-His-OA16', 'nivel': '6b', 'asignatura': 'His', 'eje': 'Formación Ciudadana', 'numero': 16,
     'descripcion': 'Explicar que los derechos generan deberes responsabilidades.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

HISTORIA_6B_UNIDADES = [
    {'codigo': '6b-His-U1', 'nivel': '6b', 'asignatura': 'His', 'numero': 1, 'nombre': 'Independencia de Chile',
     'descripcion': 'Proceso de independencia.',
     'oa_codigos': ['6b-His-OA01', '6b-His-OA05'], 'oat_codigos': ['OAT-SOC-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT01', 'His-ACT03'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '6b-His-U2', 'nivel': '6b', 'asignatura': 'His', 'numero': 2, 'nombre': 'Ambientes de Chile',
     'descripcion': 'Diversidad de ambientes naturales.',
     'oa_codigos': ['6b-His-OA12'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT03'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '6b-His-U3', 'nivel': '6b', 'asignatura': 'His', 'numero': 3, 'nombre': 'Derechos y deberes',
     'descripcion': 'Relación derechos-deberes.',
     'oa_codigos': ['6b-His-OA16'], 'oat_codigos': ['OAT-MOR-01', 'OAT-SOC-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT02', 'His-ACT04'],
     'horas_sugeridas': 35, 'semanas_sugeridas': 4, 'priorizado_2025': True},
]

# 7° Básico - Historia
HISTORIA_7B_OAS = [
    {'codigo': '7b-His-OA01', 'nivel': '7b', 'asignatura': 'His', 'eje': 'Historia', 'numero': 1,
     'descripcion': 'Explicar el proceso de hominización y migración del ser humano.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '7b-His-OA05', 'nivel': '7b', 'asignatura': 'His', 'eje': 'Historia', 'numero': 5,
     'descripcion': 'Caracterizar las primeras civilizaciones fluviales.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '7b-His-OA09', 'nivel': '7b', 'asignatura': 'His', 'eje': 'Geografía', 'numero': 9,
     'descripcion': 'Explicar las dinámicas demográficas a nivel mundial.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
    {'codigo': '7b-His-OA14', 'nivel': '7b', 'asignatura': 'His', 'eje': 'Formación Ciudadana', 'numero': 14,
     'descripcion': 'Explicar la importancia de la participación ciudadana en una democracia.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

HISTORIA_7B_UNIDADES = [
    {'codigo': '7b-His-U1', 'nivel': '7b', 'asignatura': 'His', 'numero': 1, 'nombre': 'Orígenes de la humanidad',
     'descripcion': 'Hominización y migraciones.',
     'oa_codigos': ['7b-His-OA01'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT01'],
     'horas_sugeridas': 45, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '7b-His-U2', 'nivel': '7b', 'asignatura': 'His', 'numero': 2, 'nombre': 'Primeras civilizaciones',
     'descripcion': 'Civilizaciones fluviales.',
     'oa_codigos': ['7b-His-OA05'], 'oat_codigos': ['OAT-SOC-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT03'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '7b-His-U3', 'nivel': '7b', 'asignatura': 'His', 'numero': 3, 'nombre': 'Demografía mundial',
     'descripcion': 'Dinámicas de población.',
     'oa_codigos': ['7b-His-OA09'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '7b-His-U4', 'nivel': '7b', 'asignatura': 'His', 'numero': 4, 'nombre': 'Democracia y participación',
     'descripcion': 'Participación ciudadana.',
     'oa_codigos': ['7b-His-OA14'], 'oat_codigos': ['OAT-SOC-02', 'OAT-MOR-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT02', 'His-ACT04'],
     'horas_sugeridas': 35, 'semanas_sugeridas': 4, 'priorizado_2025': True},
]

# 8° Básico - Historia
HISTORIA_8B_OAS = [
    {'codigo': '8b-His-OA01', 'nivel': '8b', 'asignatura': 'His', 'eje': 'Historia', 'numero': 1,
     'descripcion': 'Analizar las transformaciones culturales del siglo XVIII.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '8b-His-OA05', 'nivel': '8b', 'asignatura': 'His', 'eje': 'Historia', 'numero': 5,
     'descripcion': 'Analizar las consecuencias sociales y económicas de las revoluciones.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '8b-His-OA09', 'nivel': '8b', 'asignatura': 'His', 'eje': 'Historia', 'numero': 9,
     'descripcion': 'Explicar las características del régimen liberal republicano.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '8b-His-OA14', 'nivel': '8b', 'asignatura': 'His', 'eje': 'Geografía', 'numero': 14,
     'descripcion': 'Analizar las características de urbanización en las sociedades contemporáneas.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
    {'codigo': '8b-His-OA18', 'nivel': '8b', 'asignatura': 'His', 'eje': 'Formación Ciudadana', 'numero': 18,
     'descripcion': 'Analizar el concepto de Estado y nación desde diversas perspectivas.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

HISTORIA_8B_UNIDADES = [
    {'codigo': '8b-His-U1', 'nivel': '8b', 'asignatura': 'His', 'numero': 1, 'nombre': 'Transformaciones del siglo XVIII',
     'descripcion': 'Cambios culturales e ilustración.',
     'oa_codigos': ['8b-His-OA01'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT01'],
     'horas_sugeridas': 45, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '8b-His-U2', 'nivel': '8b', 'asignatura': 'His', 'numero': 2, 'nombre': 'Las revoluciones',
     'descripcion': 'Revoluciones y sus consecuencias.',
     'oa_codigos': ['8b-His-OA05', '8b-His-OA09'], 'oat_codigos': ['OAT-SOC-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT01', 'His-ACT03'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '8b-His-U3', 'nivel': '8b', 'asignatura': 'His', 'numero': 3, 'nombre': 'Urbanización',
     'descripcion': 'Ciudades y sociedad contemporánea.',
     'oa_codigos': ['8b-His-OA14'], 'oat_codigos': ['OAT-COG-01', 'OAT-SOC-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT03'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '8b-His-U4', 'nivel': '8b', 'asignatura': 'His', 'numero': 4, 'nombre': 'Estado y nación',
     'descripcion': 'Conceptos de estado y ciudadanía.',
     'oa_codigos': ['8b-His-OA18'], 'oat_codigos': ['OAT-SOC-02', 'OAT-MOR-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT02', 'His-ACT04'],
     'horas_sugeridas': 35, 'semanas_sugeridas': 4, 'priorizado_2025': True},
]

# Consolidar Historia
HISTORIA_BASICA_COMPLETA = {
    'actitudes': HISTORIA_ACTITUDES,
    'niveles': {
        '1b': {'oas': HISTORIA_1B_OAS, 'unidades': HISTORIA_1B_UNIDADES},
        '2b': {'oas': HISTORIA_2B_OAS, 'unidades': HISTORIA_2B_UNIDADES},
        '3b': {'oas': HISTORIA_3B_OAS, 'unidades': HISTORIA_3B_UNIDADES},
        '4b': {'oas': HISTORIA_4B_OAS, 'unidades': HISTORIA_4B_UNIDADES},
        '5b': {'oas': HISTORIA_5B_OAS, 'unidades': HISTORIA_5B_UNIDADES},
        '6b': {'oas': HISTORIA_6B_OAS, 'unidades': HISTORIA_6B_UNIDADES},
        '7b': {'oas': HISTORIA_7B_OAS, 'unidades': HISTORIA_7B_UNIDADES},
        '8b': {'oas': HISTORIA_8B_OAS, 'unidades': HISTORIA_8B_UNIDADES},
    }
}
