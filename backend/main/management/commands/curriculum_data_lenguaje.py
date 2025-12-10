"""
Datos del Currículum Nacional Chileno - Lenguaje y Comunicación 1°-8° Básico
"""

# ==========================================
# LENGUAJE Y COMUNICACIÓN - EDUCACIÓN BÁSICA
# ==========================================

LENGUAJE_ACTITUDES = [
    {'codigo': 'Lyc-ACT01', 'asignatura': 'Lyc', 'numero': 1,
     'descripcion': 'Demostrar interés y una actitud activa frente a la lectura.'},
    {'codigo': 'Lyc-ACT02', 'asignatura': 'Lyc', 'numero': 2,
     'descripcion': 'Demostrar disposición e interés por expresarse creativamente.'},
    {'codigo': 'Lyc-ACT03', 'asignatura': 'Lyc', 'numero': 3,
     'descripcion': 'Demostrar respeto por las diversas opiniones.'},
    {'codigo': 'Lyc-ACT04', 'asignatura': 'Lyc', 'numero': 4,
     'descripcion': 'Realizar tareas y trabajos de forma rigurosa y perseverante.'},
]

# 2° Básico - Lenguaje
LENGUAJE_2B_OAS = [
    {'codigo': '2b-Lyc-OA01', 'nivel': '2b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 1,
     'descripcion': 'Leer textos significativos que incluyan palabras con hiatos y diptongos.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': [
         {'codigo': '2b-Lyc-OA01-I1', 'descripcion': 'Leer palabras con diptongos.', 'verbo_infinitivo': 'Leer'},
         {'codigo': '2b-Lyc-OA01-I2', 'descripcion': 'Leer palabras con hiatos.', 'verbo_infinitivo': 'Leer'},
     ]},
    {'codigo': '2b-Lyc-OA03', 'nivel': '2b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 3,
     'descripcion': 'Comprender textos aplicando estrategias de comprensión lectora.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '2b-Lyc-OA05', 'nivel': '2b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 5,
     'descripcion': 'Demostrar comprensión de las narraciones leídas.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '2b-Lyc-OA12', 'nivel': '2b', 'asignatura': 'Lyc', 'eje': 'Escritura', 'numero': 12,
     'descripcion': 'Escribir frecuentemente para desarrollar la creatividad y expresar sus ideas.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '2b-Lyc-OA18', 'nivel': '2b', 'asignatura': 'Lyc', 'eje': 'Comunicación Oral', 'numero': 18,
     'descripcion': 'Comprender textos orales para obtener información.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

LENGUAJE_2B_UNIDADES = [
    {'codigo': '2b-Lyc-U1', 'nivel': '2b', 'asignatura': 'Lyc', 'numero': 1, 'nombre': 'Lectura fluida',
     'descripcion': 'Desarrollo de la fluidez lectora con diptongos e hiatos.',
     'oa_codigos': ['2b-Lyc-OA01', '2b-Lyc-OA03'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT01'],
     'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True},
    {'codigo': '2b-Lyc-U2', 'nivel': '2b', 'asignatura': 'Lyc', 'numero': 2, 'nombre': 'Comprensión de narraciones',
     'descripcion': 'Comprensión de cuentos y narraciones.',
     'oa_codigos': ['2b-Lyc-OA05'], 'oat_codigos': ['OAT-COG-02', 'OAT-AFE-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT01', 'Lyc-ACT03'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '2b-Lyc-U3', 'nivel': '2b', 'asignatura': 'Lyc', 'numero': 3, 'nombre': 'Escritura creativa',
     'descripcion': 'Desarrollo de la escritura creativa.',
     'oa_codigos': ['2b-Lyc-OA12'], 'oat_codigos': ['OAT-COG-03'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT02'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '2b-Lyc-U4', 'nivel': '2b', 'asignatura': 'Lyc', 'numero': 4, 'nombre': 'Comunicación oral',
     'descripcion': 'Comprensión y expresión oral.',
     'oa_codigos': ['2b-Lyc-OA18'], 'oat_codigos': ['OAT-SOC-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT03'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

# 3° Básico - Lenguaje
LENGUAJE_3B_OAS = [
    {'codigo': '3b-Lyc-OA01', 'nivel': '3b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 1,
     'descripcion': 'Leer de manera fluida textos variados apropiados a su edad.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '3b-Lyc-OA04', 'nivel': '3b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 4,
     'descripcion': 'Profundizar su comprensión de las narraciones leídas.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '3b-Lyc-OA08', 'nivel': '3b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 8,
     'descripcion': 'Comprender textos no literarios para ampliar su conocimiento del mundo.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '3b-Lyc-OA12', 'nivel': '3b', 'asignatura': 'Lyc', 'eje': 'Escritura', 'numero': 12,
     'descripcion': 'Escribir creativamente narraciones que incluyan una secuencia lógica de eventos.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '3b-Lyc-OA22', 'nivel': '3b', 'asignatura': 'Lyc', 'eje': 'Comunicación Oral', 'numero': 22,
     'descripcion': 'Comprender y disfrutar versiones completas de obras de la literatura.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
]

LENGUAJE_3B_UNIDADES = [
    {'codigo': '3b-Lyc-U1', 'nivel': '3b', 'asignatura': 'Lyc', 'numero': 1, 'nombre': 'Lectura variada',
     'descripcion': 'Lectura fluida de textos diversos.',
     'oa_codigos': ['3b-Lyc-OA01', '3b-Lyc-OA04'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT01'],
     'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True},
    {'codigo': '3b-Lyc-U2', 'nivel': '3b', 'asignatura': 'Lyc', 'numero': 2, 'nombre': 'Textos informativos',
     'descripcion': 'Comprensión de textos no literarios.',
     'oa_codigos': ['3b-Lyc-OA08'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT04'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '3b-Lyc-U3', 'nivel': '3b', 'asignatura': 'Lyc', 'numero': 3, 'nombre': 'Narraciones propias',
     'descripcion': 'Escritura de narraciones con estructura.',
     'oa_codigos': ['3b-Lyc-OA12'], 'oat_codigos': ['OAT-COG-03'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT02'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '3b-Lyc-U4', 'nivel': '3b', 'asignatura': 'Lyc', 'numero': 4, 'nombre': 'Literatura oral',
     'descripcion': 'Comprensión y disfrute de literatura.',
     'oa_codigos': ['3b-Lyc-OA22'], 'oat_codigos': ['OAT-AFE-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT01', 'Lyc-ACT03'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

# 4° Básico - Lenguaje
LENGUAJE_4B_OAS = [
    {'codigo': '4b-Lyc-OA01', 'nivel': '4b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 1,
     'descripcion': 'Leer y familiarizarse con un amplio repertorio de literatura.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '4b-Lyc-OA04', 'nivel': '4b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 4,
     'descripcion': 'Profundizar su comprensión de las narraciones leídas extrayendo información explícita e implícita.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '4b-Lyc-OA12', 'nivel': '4b', 'asignatura': 'Lyc', 'eje': 'Escritura', 'numero': 12,
     'descripcion': 'Escribir creativamente narraciones que incluyan descripciones de ambiente y personajes.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '4b-Lyc-OA14', 'nivel': '4b', 'asignatura': 'Lyc', 'eje': 'Escritura', 'numero': 14,
     'descripcion': 'Escribir cartas, instrucciones, afiches, reportes de una experiencia, noticias.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
]

LENGUAJE_4B_UNIDADES = [
    {'codigo': '4b-Lyc-U1', 'nivel': '4b', 'asignatura': 'Lyc', 'numero': 1, 'nombre': 'Repertorio literario',
     'descripcion': 'Ampliación del repertorio de lecturas.',
     'oa_codigos': ['4b-Lyc-OA01', '4b-Lyc-OA04'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT01'],
     'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True},
    {'codigo': '4b-Lyc-U2', 'nivel': '4b', 'asignatura': 'Lyc', 'numero': 2, 'nombre': 'Narraciones descriptivas',
     'descripcion': 'Escritura de narraciones con descripciones.',
     'oa_codigos': ['4b-Lyc-OA12'], 'oat_codigos': ['OAT-COG-03'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT02'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '4b-Lyc-U3', 'nivel': '4b', 'asignatura': 'Lyc', 'numero': 3, 'nombre': 'Textos funcionales',
     'descripcion': 'Escritura de diversos tipos de textos funcionales.',
     'oa_codigos': ['4b-Lyc-OA14'], 'oat_codigos': ['OAT-COG-03', 'OAT-SOC-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT04'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
]

# 5° Básico - Lenguaje
LENGUAJE_5B_OAS = [
    {'codigo': '5b-Lyc-OA03', 'nivel': '5b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 3,
     'descripcion': 'Analizar aspectos relevantes de narraciones leídas para profundizar su comprensión.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '5b-Lyc-OA06', 'nivel': '5b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 6,
     'descripcion': 'Leer independientemente y comprender textos no literarios.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '5b-Lyc-OA11', 'nivel': '5b', 'asignatura': 'Lyc', 'eje': 'Escritura', 'numero': 11,
     'descripcion': 'Escribir artículos informativos para comunicar información sobre un tema.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '5b-Lyc-OA22', 'nivel': '5b', 'asignatura': 'Lyc', 'eje': 'Comunicación Oral', 'numero': 22,
     'descripcion': 'Dialogar para compartir y desarrollar ideas y buscar acuerdos.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
]

LENGUAJE_5B_UNIDADES = [
    {'codigo': '5b-Lyc-U1', 'nivel': '5b', 'asignatura': 'Lyc', 'numero': 1, 'nombre': 'Análisis narrativo',
     'descripcion': 'Análisis de narraciones literarias.',
     'oa_codigos': ['5b-Lyc-OA03'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT01'],
     'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True},
    {'codigo': '5b-Lyc-U2', 'nivel': '5b', 'asignatura': 'Lyc', 'numero': 2, 'nombre': 'Textos no literarios',
     'descripcion': 'Lectura y comprensión de textos informativos.',
     'oa_codigos': ['5b-Lyc-OA06'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT04'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '5b-Lyc-U3', 'nivel': '5b', 'asignatura': 'Lyc', 'numero': 3, 'nombre': 'Escritura informativa',
     'descripcion': 'Producción de textos informativos.',
     'oa_codigos': ['5b-Lyc-OA11'], 'oat_codigos': ['OAT-COG-03'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT02', 'Lyc-ACT04'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '5b-Lyc-U4', 'nivel': '5b', 'asignatura': 'Lyc', 'numero': 4, 'nombre': 'Diálogo y acuerdos',
     'descripcion': 'Habilidades de diálogo y construcción de acuerdos.',
     'oa_codigos': ['5b-Lyc-OA22'], 'oat_codigos': ['OAT-SOC-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT03'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

# 6° Básico - Lenguaje
LENGUAJE_6B_OAS = [
    {'codigo': '6b-Lyc-OA03', 'nivel': '6b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 3,
     'descripcion': 'Analizar aspectos relevantes de narraciones leídas para profundizar su comprensión.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '6b-Lyc-OA04', 'nivel': '6b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 4,
     'descripcion': 'Analizar aspectos relevantes de poemas para profundizar su comprensión.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '6b-Lyc-OA12', 'nivel': '6b', 'asignatura': 'Lyc', 'eje': 'Escritura', 'numero': 12,
     'descripcion': 'Escribir creativamente narraciones que desarrollen un conflicto central.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '6b-Lyc-OA18', 'nivel': '6b', 'asignatura': 'Lyc', 'eje': 'Comunicación Oral', 'numero': 18,
     'descripcion': 'Expresarse de manera clara y efectiva en exposiciones orales.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

LENGUAJE_6B_UNIDADES = [
    {'codigo': '6b-Lyc-U1', 'nivel': '6b', 'asignatura': 'Lyc', 'numero': 1, 'nombre': 'Análisis literario',
     'descripcion': 'Análisis de narraciones y poemas.',
     'oa_codigos': ['6b-Lyc-OA03', '6b-Lyc-OA04'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT01'],
     'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True},
    {'codigo': '6b-Lyc-U2', 'nivel': '6b', 'asignatura': 'Lyc', 'numero': 2, 'nombre': 'Narraciones con conflicto',
     'descripcion': 'Escritura de narraciones con conflicto central.',
     'oa_codigos': ['6b-Lyc-OA12'], 'oat_codigos': ['OAT-COG-03'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT02'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '6b-Lyc-U3', 'nivel': '6b', 'asignatura': 'Lyc', 'numero': 3, 'nombre': 'Exposiciones orales',
     'descripcion': 'Desarrollo de habilidades de exposición.',
     'oa_codigos': ['6b-Lyc-OA18'], 'oat_codigos': ['OAT-COG-03', 'OAT-SOC-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT03', 'Lyc-ACT04'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
]

# 7° Básico - Lenguaje
LENGUAJE_7B_OAS = [
    {'codigo': '7b-Lyc-OA02', 'nivel': '7b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 2,
     'descripcion': 'Reflexionar sobre las narraciones leídas considerando el conflicto central y el protagonista.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '7b-Lyc-OA06', 'nivel': '7b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 6,
     'descripcion': 'Leer y comprender textos no literarios para distinguir hechos de opiniones.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '7b-Lyc-OA11', 'nivel': '7b', 'asignatura': 'Lyc', 'eje': 'Escritura', 'numero': 11,
     'descripcion': 'Escribir, con el propósito de persuadir, textos breves de diversos géneros.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '7b-Lyc-OA18', 'nivel': '7b', 'asignatura': 'Lyc', 'eje': 'Comunicación Oral', 'numero': 18,
     'descripcion': 'Expresar opiniones fundamentadas sobre un tema.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
]

LENGUAJE_7B_UNIDADES = [
    {'codigo': '7b-Lyc-U1', 'nivel': '7b', 'asignatura': 'Lyc', 'numero': 1, 'nombre': 'Reflexión narrativa',
     'descripcion': 'Análisis reflexivo de narraciones.',
     'oa_codigos': ['7b-Lyc-OA02'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT01'],
     'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True},
    {'codigo': '7b-Lyc-U2', 'nivel': '7b', 'asignatura': 'Lyc', 'numero': 2, 'nombre': 'Hechos y opiniones',
     'descripcion': 'Distinción entre hechos y opiniones en textos.',
     'oa_codigos': ['7b-Lyc-OA06'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT04'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '7b-Lyc-U3', 'nivel': '7b', 'asignatura': 'Lyc', 'numero': 3, 'nombre': 'Escritura persuasiva',
     'descripcion': 'Producción de textos persuasivos.',
     'oa_codigos': ['7b-Lyc-OA11'], 'oat_codigos': ['OAT-COG-03'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT02'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '7b-Lyc-U4', 'nivel': '7b', 'asignatura': 'Lyc', 'numero': 4, 'nombre': 'Opinión fundamentada',
     'descripcion': 'Expresión oral de opiniones fundamentadas.',
     'oa_codigos': ['7b-Lyc-OA18'], 'oat_codigos': ['OAT-SOC-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT03'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

# 8° Básico - Lenguaje
LENGUAJE_8B_OAS = [
    {'codigo': '8b-Lyc-OA02', 'nivel': '8b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 2,
     'descripcion': 'Reflexionar sobre las narraciones leídas considerando el contexto sociocultural de producción.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '8b-Lyc-OA03', 'nivel': '8b', 'asignatura': 'Lyc', 'eje': 'Lectura', 'numero': 3,
     'descripcion': 'Analizar las narraciones leídas considerando los recursos utilizados para crear efectos.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '8b-Lyc-OA09', 'nivel': '8b', 'asignatura': 'Lyc', 'eje': 'Escritura', 'numero': 9,
     'descripcion': 'Analizar y evaluar textos de los medios de comunicación.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '8b-Lyc-OA12', 'nivel': '8b', 'asignatura': 'Lyc', 'eje': 'Escritura', 'numero': 12,
     'descripcion': 'Escribir, con el propósito de explicar un tema, textos coherentes y cohesionados.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '8b-Lyc-OA19', 'nivel': '8b', 'asignatura': 'Lyc', 'eje': 'Comunicación Oral', 'numero': 19,
     'descripcion': 'Dialogar para compartir y desarrollar ideas, proponiendo soluciones a los problemas.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
]

LENGUAJE_8B_UNIDADES = [
    {'codigo': '8b-Lyc-U1', 'nivel': '8b', 'asignatura': 'Lyc', 'numero': 1, 'nombre': 'Contexto sociocultural',
     'descripcion': 'Análisis de narraciones en su contexto.',
     'oa_codigos': ['8b-Lyc-OA02', '8b-Lyc-OA03'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-02', 'OAT-SOC-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT01'],
     'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True},
    {'codigo': '8b-Lyc-U2', 'nivel': '8b', 'asignatura': 'Lyc', 'numero': 2, 'nombre': 'Medios de comunicación',
     'descripcion': 'Análisis de textos mediáticos.',
     'oa_codigos': ['8b-Lyc-OA09'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT04'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '8b-Lyc-U3', 'nivel': '8b', 'asignatura': 'Lyc', 'numero': 3, 'nombre': 'Escritura explicativa',
     'descripcion': 'Producción de textos explicativos coherentes.',
     'oa_codigos': ['8b-Lyc-OA12'], 'oat_codigos': ['OAT-COG-03'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT02', 'Lyc-ACT04'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '8b-Lyc-U4', 'nivel': '8b', 'asignatura': 'Lyc', 'numero': 4, 'nombre': 'Diálogo y soluciones',
     'descripcion': 'Diálogo orientado a la resolución de problemas.',
     'oa_codigos': ['8b-Lyc-OA19'], 'oat_codigos': ['OAT-SOC-02', 'OAT-MOR-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyc-ACT03'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

# Consolidar Lenguaje
LENGUAJE_BASICA = {
    'actitudes': LENGUAJE_ACTITUDES,
    'niveles': {
        '2b': {'oas': LENGUAJE_2B_OAS, 'unidades': LENGUAJE_2B_UNIDADES},
        '3b': {'oas': LENGUAJE_3B_OAS, 'unidades': LENGUAJE_3B_UNIDADES},
        '4b': {'oas': LENGUAJE_4B_OAS, 'unidades': LENGUAJE_4B_UNIDADES},
        '5b': {'oas': LENGUAJE_5B_OAS, 'unidades': LENGUAJE_5B_UNIDADES},
        '6b': {'oas': LENGUAJE_6B_OAS, 'unidades': LENGUAJE_6B_UNIDADES},
        '7b': {'oas': LENGUAJE_7B_OAS, 'unidades': LENGUAJE_7B_UNIDADES},
        '8b': {'oas': LENGUAJE_8B_OAS, 'unidades': LENGUAJE_8B_UNIDADES},
    }
}
