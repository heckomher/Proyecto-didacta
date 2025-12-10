"""
Datos del Currículum Nacional Chileno - Educación Media
Incluye asignaturas comunes y electivos del área Científico-Humanista
"""

# ==========================================
# LENGUA Y LITERATURA - EDUCACIÓN MEDIA
# ==========================================

LENGUA_LITERATURA_ACTITUDES = [
    {'codigo': 'Lyl-ACT01', 'asignatura': 'Lyl', 'numero': 1,
     'descripcion': 'Interesarse por comprender las experiencias e ideas de los demás.'},
    {'codigo': 'Lyl-ACT02', 'asignatura': 'Lyl', 'numero': 2,
     'descripcion': 'Valorar la diversidad de perspectivas, creencias y culturas.'},
    {'codigo': 'Lyl-ACT03', 'asignatura': 'Lyl', 'numero': 3,
     'descripcion': 'Valorar la evidencia y la búsqueda de conocimiento en la literatura.'},
]

LENGUA_1M_OAS = [
    {'codigo': '1m-Lyl-OA01', 'nivel': '1m', 'asignatura': 'Lyl', 'eje': 'Lectura', 'numero': 1,
     'descripcion': 'Leer habitualmente para aprender y recrearse, y seleccionar textos de acuerdo con sus preferencias y propósitos.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '1m-Lyl-OA03', 'nivel': '1m', 'asignatura': 'Lyl', 'eje': 'Lectura', 'numero': 3,
     'descripcion': 'Analizar las narraciones leídas para enriquecer su comprensión.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '1m-Lyl-OA12', 'nivel': '1m', 'asignatura': 'Lyl', 'eje': 'Escritura', 'numero': 12,
     'descripcion': 'Escribir, con el propósito de explicar un tema, textos de diversos géneros.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '1m-Lyl-OA18', 'nivel': '1m', 'asignatura': 'Lyl', 'eje': 'Comunicación Oral', 'numero': 18,
     'descripcion': 'Dialogar constructivamente para debatir o explorar ideas.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
]

LENGUA_1M_UNIDADES = [
    {'codigo': '1m-Lyl-U1', 'nivel': '1m', 'asignatura': 'Lyl', 'numero': 1, 'nombre': 'Narrativa y análisis literario',
     'descripcion': 'Lectura y análisis de textos narrativos.',
     'oa_codigos': ['1m-Lyl-OA01', '1m-Lyl-OA03'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-03'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyl-ACT01', 'Lyl-ACT02'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '1m-Lyl-U2', 'nivel': '1m', 'asignatura': 'Lyl', 'numero': 2, 'nombre': 'Escritura expositiva',
     'descripcion': 'Producción de textos explicativos.',
     'oa_codigos': ['1m-Lyl-OA12'], 'oat_codigos': ['OAT-COG-03'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyl-ACT03'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '1m-Lyl-U3', 'nivel': '1m', 'asignatura': 'Lyl', 'numero': 3, 'nombre': 'Comunicación y debate',
     'descripcion': 'Habilidades de diálogo y argumentación.',
     'oa_codigos': ['1m-Lyl-OA18'], 'oat_codigos': ['OAT-SOC-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyl-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

LENGUA_2M_OAS = [
    {'codigo': '2m-Lyl-OA02', 'nivel': '2m', 'asignatura': 'Lyl', 'eje': 'Lectura', 'numero': 2,
     'descripcion': 'Reflexionar sobre las diferentes dimensiones de la experiencia humana en textos literarios.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '2m-Lyl-OA05', 'nivel': '2m', 'asignatura': 'Lyl', 'eje': 'Lectura', 'numero': 5,
     'descripcion': 'Analizar los poemas leídos para enriquecer su comprensión.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

LENGUA_2M_UNIDADES = [
    {'codigo': '2m-Lyl-U1', 'nivel': '2m', 'asignatura': 'Lyl', 'numero': 1, 'nombre': 'Poesía y análisis',
     'descripcion': 'Lectura y análisis de textos poéticos.',
     'oa_codigos': ['2m-Lyl-OA02', '2m-Lyl-OA05'], 'oat_codigos': ['OAT-AFE-01', 'OAT-COG-03'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyl-ACT01', 'Lyl-ACT02'],
     'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True},
]

# III° Medio - Lengua y Literatura
LENGUA_3M_OAS = [
    {'codigo': '3m-Lyl-OA01', 'nivel': '3m', 'asignatura': 'Lyl', 'eje': 'Lectura', 'numero': 1,
     'descripcion': 'Formular interpretaciones de textos literarios considerando aspectos contextuales e intertextuales.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '3m-Lyl-OA03', 'nivel': '3m', 'asignatura': 'Lyl', 'eje': 'Lectura', 'numero': 3,
     'descripcion': 'Analizar textos no literarios considerando su propósito comunicativo.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '3m-Lyl-OA05', 'nivel': '3m', 'asignatura': 'Lyl', 'eje': 'Escritura', 'numero': 5,
     'descripcion': 'Producir textos con propósitos argumentativos variados.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '3m-Lyl-OA08', 'nivel': '3m', 'asignatura': 'Lyl', 'eje': 'Comunicación Oral', 'numero': 8,
     'descripcion': 'Dialogar para construir acuerdos considerando diversas perspectivas.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
]

LENGUA_3M_UNIDADES = [
    {'codigo': '3m-Lyl-U1', 'nivel': '3m', 'asignatura': 'Lyl', 'numero': 1, 'nombre': 'Interpretación literaria',
     'descripcion': 'Análisis de obras literarias con enfoque contextual.',
     'oa_codigos': ['3m-Lyl-OA01'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-03'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyl-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '3m-Lyl-U2', 'nivel': '3m', 'asignatura': 'Lyl', 'numero': 2, 'nombre': 'Textos no literarios',
     'descripcion': 'Análisis de medios y textos informativos.',
     'oa_codigos': ['3m-Lyl-OA03'], 'oat_codigos': ['OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyl-ACT02'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '3m-Lyl-U3', 'nivel': '3m', 'asignatura': 'Lyl', 'numero': 3, 'nombre': 'Argumentación',
     'descripcion': 'Escritura de textos argumentativos.',
     'oa_codigos': ['3m-Lyl-OA05', '3m-Lyl-OA08'], 'oat_codigos': ['OAT-SOC-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyl-ACT03'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
]

# IV° Medio - Lengua y Literatura
LENGUA_4M_OAS = [
    {'codigo': '4m-Lyl-OA01', 'nivel': '4m', 'asignatura': 'Lyl', 'eje': 'Lectura', 'numero': 1,
     'descripcion': 'Evaluar críticamente textos literarios y no literarios considerando múltiples perspectivas.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '4m-Lyl-OA04', 'nivel': '4m', 'asignatura': 'Lyl', 'eje': 'Escritura', 'numero': 4,
     'descripcion': 'Escribir ensayos que desarrollen un tema o punto de vista con fundamentos.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '4m-Lyl-OA07', 'nivel': '4m', 'asignatura': 'Lyl', 'eje': 'Comunicación Oral', 'numero': 7,
     'descripcion': 'Exponer oralmente sobre temas de interés fundamentando sus planteamientos.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
]

LENGUA_4M_UNIDADES = [
    {'codigo': '4m-Lyl-U1', 'nivel': '4m', 'asignatura': 'Lyl', 'numero': 1, 'nombre': 'Pensamiento crítico',
     'descripcion': 'Evaluación crítica de textos diversos.',
     'oa_codigos': ['4m-Lyl-OA01'], 'oat_codigos': ['OAT-COG-03'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyl-ACT02'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '4m-Lyl-U2', 'nivel': '4m', 'asignatura': 'Lyl', 'numero': 2, 'nombre': 'El ensayo',
     'descripcion': 'Producción de ensayos académicos.',
     'oa_codigos': ['4m-Lyl-OA04'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyl-ACT03'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '4m-Lyl-U3', 'nivel': '4m', 'asignatura': 'Lyl', 'numero': 3, 'nombre': 'Oratoria',
     'descripcion': 'Exposiciones orales formales.',
     'oa_codigos': ['4m-Lyl-OA07'], 'oat_codigos': ['OAT-SOC-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Lyl-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

LENGUA_MEDIA = {
    'actitudes': LENGUA_LITERATURA_ACTITUDES,
    'niveles': {
        '1m': {'oas': LENGUA_1M_OAS, 'unidades': LENGUA_1M_UNIDADES},
        '2m': {'oas': LENGUA_2M_OAS, 'unidades': LENGUA_2M_UNIDADES},
        '3m': {'oas': LENGUA_3M_OAS, 'unidades': LENGUA_3M_UNIDADES},
        '4m': {'oas': LENGUA_4M_OAS, 'unidades': LENGUA_4M_UNIDADES},
    }
}


# ==========================================
# MATEMÁTICA - EDUCACIÓN MEDIA
# ==========================================

MATEMATICA_1M_OAS = [
    {'codigo': '1m-Mat-OA01', 'nivel': '1m', 'asignatura': 'Mat', 'eje': 'Números', 'numero': 1,
     'descripcion': 'Mostrar que comprenden la multiplicación y la división de números enteros.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '1m-Mat-OA04', 'nivel': '1m', 'asignatura': 'Mat', 'eje': 'Álgebra', 'numero': 4,
     'descripcion': 'Mostrar que comprenden las expresiones algebraicas reduciendo y desarrollando.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '1m-Mat-OA08', 'nivel': '1m', 'asignatura': 'Mat', 'eje': 'Álgebra', 'numero': 8,
     'descripcion': 'Resolver sistemas de ecuaciones lineales.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '1m-Mat-OA12', 'nivel': '1m', 'asignatura': 'Mat', 'eje': 'Geometría', 'numero': 12,
     'descripcion': 'Mostrar que comprenden las transformaciones isométricas.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
]

MATEMATICA_1M_UNIDADES = [
    {'codigo': '1m-Mat-U1', 'nivel': '1m', 'asignatura': 'Mat', 'numero': 1, 'nombre': 'Números enteros',
     'descripcion': 'Operaciones con números enteros.',
     'oa_codigos': ['1m-Mat-OA01'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '1m-Mat-U2', 'nivel': '1m', 'asignatura': 'Mat', 'numero': 2, 'nombre': 'Álgebra',
     'descripcion': 'Expresiones algebraicas y ecuaciones.',
     'oa_codigos': ['1m-Mat-OA04', '1m-Mat-OA08'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT02'],
     'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True},
    {'codigo': '1m-Mat-U3', 'nivel': '1m', 'asignatura': 'Mat', 'numero': 3, 'nombre': 'Geometría',
     'descripcion': 'Transformaciones isométricas.',
     'oa_codigos': ['1m-Mat-OA12'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

MATEMATICA_2M_OAS = [
    {'codigo': '2m-Mat-OA01', 'nivel': '2m', 'asignatura': 'Mat', 'eje': 'Números', 'numero': 1,
     'descripcion': 'Mostrar que comprenden las potencias de exponente entero.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '2m-Mat-OA04', 'nivel': '2m', 'asignatura': 'Mat', 'eje': 'Álgebra', 'numero': 4,
     'descripcion': 'Mostrar que comprenden la función cuadrática.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

MATEMATICA_2M_UNIDADES = [
    {'codigo': '2m-Mat-U1', 'nivel': '2m', 'asignatura': 'Mat', 'numero': 1, 'nombre': 'Potencias y raíces',
     'descripcion': 'Potencias de exponente entero.',
     'oa_codigos': ['2m-Mat-OA01'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '2m-Mat-U2', 'nivel': '2m', 'asignatura': 'Mat', 'numero': 2, 'nombre': 'Función cuadrática',
     'descripcion': 'Análisis de la función cuadrática.',
     'oa_codigos': ['2m-Mat-OA04'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT02'],
     'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True},
]

# III° Medio - Matemática (electivo)
MATEMATICA_3M_OAS = [
    {'codigo': '3m-Mat-OA01', 'nivel': '3m', 'asignatura': 'Mat', 'eje': 'Números', 'numero': 1,
     'descripcion': 'Aplicar procedimientos de cálculo con números complejos.',
     'priorizado_2025': False, 'nivel_priorizacion': 'COMPLEMENTARIO', 'indicadores': []},
    {'codigo': '3m-Mat-OA04', 'nivel': '3m', 'asignatura': 'Mat', 'eje': 'Álgebra', 'numero': 4,
     'descripcion': 'Resolver sistemas de ecuaciones no lineales.',
     'priorizado_2025': False, 'nivel_priorizacion': 'COMPLEMENTARIO', 'indicadores': []},
    {'codigo': '3m-Mat-OA07', 'nivel': '3m', 'asignatura': 'Mat', 'eje': 'Probabilidad', 'numero': 7,
     'descripcion': 'Resolver problemas que involucren probabilidades.',
     'priorizado_2025': False, 'nivel_priorizacion': 'COMPLEMENTARIO', 'indicadores': []},
]

MATEMATICA_3M_UNIDADES = [
    {'codigo': '3m-Mat-U1', 'nivel': '3m', 'asignatura': 'Mat', 'numero': 1, 'nombre': 'Números complejos',
     'descripcion': 'Operaciones con números complejos.',
     'oa_codigos': ['3m-Mat-OA01'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': False},
    {'codigo': '3m-Mat-U2', 'nivel': '3m', 'asignatura': 'Mat', 'numero': 2, 'nombre': 'Ecuaciones no lineales',
     'descripcion': 'Sistemas de ecuaciones.',
     'oa_codigos': ['3m-Mat-OA04'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT02'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': False},
    {'codigo': '3m-Mat-U3', 'nivel': '3m', 'asignatura': 'Mat', 'numero': 3, 'nombre': 'Probabilidad',
     'descripcion': 'Cálculo de probabilidades.',
     'oa_codigos': ['3m-Mat-OA07'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': False},
]

# IV° Medio - Matemática (electivo)
MATEMATICA_4M_OAS = [
    {'codigo': '4m-Mat-OA01', 'nivel': '4m', 'asignatura': 'Mat', 'eje': 'Cálculo', 'numero': 1,
     'descripcion': 'Comprender el concepto de límite y continuidad.',
     'priorizado_2025': False, 'nivel_priorizacion': 'COMPLEMENTARIO', 'indicadores': []},
    {'codigo': '4m-Mat-OA03', 'nivel': '4m', 'asignatura': 'Mat', 'eje': 'Cálculo', 'numero': 3,
     'descripcion': 'Aplicar derivadas para analizar funciones.',
     'priorizado_2025': False, 'nivel_priorizacion': 'COMPLEMENTARIO', 'indicadores': []},
    {'codigo': '4m-Mat-OA06', 'nivel': '4m', 'asignatura': 'Mat', 'eje': 'Estadística', 'numero': 6,
     'descripcion': 'Aplicar distribuciones de probabilidad para resolver problemas.',
     'priorizado_2025': False, 'nivel_priorizacion': 'COMPLEMENTARIO', 'indicadores': []},
]

MATEMATICA_4M_UNIDADES = [
    {'codigo': '4m-Mat-U1', 'nivel': '4m', 'asignatura': 'Mat', 'numero': 1, 'nombre': 'Límites y continuidad',
     'descripcion': 'Concepto de límite de funciones.',
     'oa_codigos': ['4m-Mat-OA01'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': False},
    {'codigo': '4m-Mat-U2', 'nivel': '4m', 'asignatura': 'Mat', 'numero': 2, 'nombre': 'Derivadas',
     'descripcion': 'Cálculo diferencial básico.',
     'oa_codigos': ['4m-Mat-OA03'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT02'],
     'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': False},
    {'codigo': '4m-Mat-U3', 'nivel': '4m', 'asignatura': 'Mat', 'numero': 3, 'nombre': 'Distribuciones',
     'descripcion': 'Distribuciones de probabilidad.',
     'oa_codigos': ['4m-Mat-OA06'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': False},
]

MATEMATICA_MEDIA = {
    'niveles': {
        '1m': {'oas': MATEMATICA_1M_OAS, 'unidades': MATEMATICA_1M_UNIDADES},
        '2m': {'oas': MATEMATICA_2M_OAS, 'unidades': MATEMATICA_2M_UNIDADES},
        '3m': {'oas': MATEMATICA_3M_OAS, 'unidades': MATEMATICA_3M_UNIDADES},
        '4m': {'oas': MATEMATICA_4M_OAS, 'unidades': MATEMATICA_4M_UNIDADES},
    }
}


# ==========================================
# BIOLOGÍA - EDUCACIÓN MEDIA (Ciencias para la Ciudadanía y electivo)
# ==========================================

BIOLOGIA_ACTITUDES = [
    {'codigo': 'Bio-ACT01', 'asignatura': 'Bio', 'numero': 1,
     'descripcion': 'Mostrar curiosidad, creatividad e interés por conocer y comprender los fenómenos del entorno natural.'},
    {'codigo': 'Bio-ACT02', 'asignatura': 'Bio', 'numero': 2,
     'descripcion': 'Manifestar una visión de futuro sustentable del medio ambiente.'},
]

BIOLOGIA_3M_OAS = [
    {'codigo': '3m-Bio-OA01', 'nivel': '3m', 'asignatura': 'Bio', 'eje': 'Biología Celular y Molecular', 'numero': 1,
     'descripcion': 'Explicar la estructura y función de la membrana celular y los procesos de transporte.',
     'priorizado_2025': False, 'nivel_priorizacion': 'COMPLEMENTARIO', 'indicadores': []},
    {'codigo': '3m-Bio-OA03', 'nivel': '3m', 'asignatura': 'Bio', 'eje': 'Herencia y Evolución', 'numero': 3,
     'descripcion': 'Explicar los mecanismos de herencia y variabilidad genética.',
     'priorizado_2025': False, 'nivel_priorizacion': 'COMPLEMENTARIO', 'indicadores': []},
    {'codigo': '3m-Bio-OA05', 'nivel': '3m', 'asignatura': 'Bio', 'eje': 'Ecología', 'numero': 5,
     'descripcion': 'Analizar y evaluar los impactos de las actividades humanas en el medio ambiente.',
     'priorizado_2025': False, 'nivel_priorizacion': 'COMPLEMENTARIO', 'indicadores': [],
     'articulaciones': [{'asignatura_codigo': 'His', 'asignatura_nombre': 'Historia y Geografía', 'descripcion': 'Desarrollo sustentable'}]},
]

BIOLOGIA_3M_UNIDADES = [
    {'codigo': '3m-Bio-U1', 'nivel': '3m', 'asignatura': 'Bio', 'numero': 1, 'nombre': 'Biología celular',
     'descripcion': 'Estructura y función celular.',
     'oa_codigos': ['3m-Bio-OA01'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Bio-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': False},
    {'codigo': '3m-Bio-U2', 'nivel': '3m', 'asignatura': 'Bio', 'numero': 2, 'nombre': 'Herencia y genética',
     'descripcion': 'Genética mendeliana y molecular.',
     'oa_codigos': ['3m-Bio-OA03'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Bio-ACT01'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': False},
    {'codigo': '3m-Bio-U3', 'nivel': '3m', 'asignatura': 'Bio', 'numero': 3, 'nombre': 'Ecología y medio ambiente',
     'descripcion': 'Impacto humano en ecosistemas. ARTICULABLE CON HISTORIA.',
     'oa_codigos': ['3m-Bio-OA05'], 'oat_codigos': ['OAT-SOC-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Bio-ACT02'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': False},
]

BIOLOGIA_MEDIA = {
    'actitudes': BIOLOGIA_ACTITUDES,
    'niveles': {
        '3m': {'oas': BIOLOGIA_3M_OAS, 'unidades': BIOLOGIA_3M_UNIDADES},
    }
}


# ==========================================
# FÍSICA - EDUCACIÓN MEDIA (Electivo CH)
# ==========================================

FISICA_ACTITUDES = [
    {'codigo': 'Fis-ACT01', 'asignatura': 'Fis', 'numero': 1,
     'descripcion': 'Mostrar curiosidad e interés por conocer y comprender fenómenos físicos.'},
    {'codigo': 'Fis-ACT02', 'asignatura': 'Fis', 'numero': 2,
     'descripcion': 'Trabajar responsablemente en forma proactiva y colaborativa.'},
]

FISICA_3M_OAS = [
    {'codigo': '3m-Fis-OA01', 'nivel': '3m', 'asignatura': 'Fis', 'eje': 'Mecánica', 'numero': 1,
     'descripcion': 'Describir el movimiento de objetos utilizando las leyes de Newton.',
     'priorizado_2025': False, 'nivel_priorizacion': 'COMPLEMENTARIO', 'indicadores': [],
     'articulaciones': [{'asignatura_codigo': 'Mat', 'asignatura_nombre': 'Matemática', 'descripcion': 'Funciones y vectores'}]},
    {'codigo': '3m-Fis-OA04', 'nivel': '3m', 'asignatura': 'Fis', 'eje': 'Ondas', 'numero': 4,
     'descripcion': 'Analizar fenómenos ondulatorios de la vida cotidiana.',
     'priorizado_2025': False, 'nivel_priorizacion': 'COMPLEMENTARIO', 'indicadores': []},
    {'codigo': '3m-Fis-OA07', 'nivel': '3m', 'asignatura': 'Fis', 'eje': 'Electricidad', 'numero': 7,
     'descripcion': 'Explicar circuitos eléctricos simples y su aplicación.',
     'priorizado_2025': False, 'nivel_priorizacion': 'COMPLEMENTARIO', 'indicadores': []},
]

FISICA_3M_UNIDADES = [
    {'codigo': '3m-Fis-U1', 'nivel': '3m', 'asignatura': 'Fis', 'numero': 1, 'nombre': 'Mecánica newtoniana',
     'descripcion': 'Leyes de Newton y movimiento. ARTICULABLE CON MATEMÁTICA.',
     'oa_codigos': ['3m-Fis-OA01'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Fis-ACT01'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': False},
    {'codigo': '3m-Fis-U2', 'nivel': '3m', 'asignatura': 'Fis', 'numero': 2, 'nombre': 'Ondas',
     'descripcion': 'Fenómenos ondulatorios.',
     'oa_codigos': ['3m-Fis-OA04'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Fis-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': False},
    {'codigo': '3m-Fis-U3', 'nivel': '3m', 'asignatura': 'Fis', 'numero': 3, 'nombre': 'Electricidad',
     'descripcion': 'Circuitos eléctricos.',
     'oa_codigos': ['3m-Fis-OA07'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Fis-ACT02'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': False},
]

FISICA_MEDIA = {
    'actitudes': FISICA_ACTITUDES,
    'niveles': {
        '3m': {'oas': FISICA_3M_OAS, 'unidades': FISICA_3M_UNIDADES},
    }
}


# ==========================================
# QUÍMICA - EDUCACIÓN MEDIA (Electivo CH)
# ==========================================

QUIMICA_ACTITUDES = [
    {'codigo': 'Qui-ACT01', 'asignatura': 'Qui', 'numero': 1,
     'descripcion': 'Mostrar curiosidad e interés por conocer las propiedades de la materia.'},
    {'codigo': 'Qui-ACT02', 'asignatura': 'Qui', 'numero': 2,
     'descripcion': 'Manifestar una visión de futuro sustentable en el uso de recursos químicos.'},
]

QUIMICA_3M_OAS = [
    {'codigo': '3m-Qui-OA01', 'nivel': '3m', 'asignatura': 'Qui', 'eje': 'Estructura Atómica', 'numero': 1,
     'descripcion': 'Explicar la estructura atómica y organización de la tabla periódica.',
     'priorizado_2025': False, 'nivel_priorizacion': 'COMPLEMENTARIO', 'indicadores': []},
    {'codigo': '3m-Qui-OA04', 'nivel': '3m', 'asignatura': 'Qui', 'eje': 'Reacciones Químicas', 'numero': 4,
     'descripcion': 'Predecir el comportamiento de reacciones químicas.',
     'priorizado_2025': False, 'nivel_priorizacion': 'COMPLEMENTARIO', 'indicadores': [],
     'articulaciones': [{'asignatura_codigo': 'Bio', 'asignatura_nombre': 'Biología', 'descripcion': 'Reacciones bioquímicas'}]},
    {'codigo': '3m-Qui-OA06', 'nivel': '3m', 'asignatura': 'Qui', 'eje': 'Química Orgánica', 'numero': 6,
     'descripcion': 'Analizar las propiedades de compuestos orgánicos.',
     'priorizado_2025': False, 'nivel_priorizacion': 'COMPLEMENTARIO', 'indicadores': []},
]

QUIMICA_3M_UNIDADES = [
    {'codigo': '3m-Qui-U1', 'nivel': '3m', 'asignatura': 'Qui', 'numero': 1, 'nombre': 'Estructura atómica',
     'descripcion': 'Átomo y tabla periódica.',
     'oa_codigos': ['3m-Qui-OA01'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Qui-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': False},
    {'codigo': '3m-Qui-U2', 'nivel': '3m', 'asignatura': 'Qui', 'numero': 2, 'nombre': 'Reacciones químicas',
     'descripcion': 'Estequiometría y equilibrio. ARTICULABLE CON BIOLOGÍA.',
     'oa_codigos': ['3m-Qui-OA04'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Qui-ACT01'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': False},
    {'codigo': '3m-Qui-U3', 'nivel': '3m', 'asignatura': 'Qui', 'numero': 3, 'nombre': 'Química orgánica',
     'descripcion': 'Compuestos del carbono.',
     'oa_codigos': ['3m-Qui-OA06'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Qui-ACT02'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': False},
]

QUIMICA_MEDIA = {
    'actitudes': QUIMICA_ACTITUDES,
    'niveles': {
        '3m': {'oas': QUIMICA_3M_OAS, 'unidades': QUIMICA_3M_UNIDADES},
    }
}


# ==========================================
# FILOSOFÍA - EDUCACIÓN MEDIA
# ==========================================

FILOSOFIA_ACTITUDES = [
    {'codigo': 'Fil-ACT01', 'asignatura': 'Fil', 'numero': 1,
     'descripcion': 'Pensar con apertura a distintas perspectivas y contextos.'},
    {'codigo': 'Fil-ACT02', 'asignatura': 'Fil', 'numero': 2,
     'descripcion': 'Valorar el diálogo como fuente de conocimiento y crecimiento.'},
]

FILOSOFIA_3M_OAS = [
    {'codigo': '3m-Fil-OA01', 'nivel': '3m', 'asignatura': 'Fil', 'eje': 'Filosofía', 'numero': 1,
     'descripcion': 'Formular preguntas filosóficas sobre la realidad y el conocimiento.',
     'priorizado_2025': False, 'nivel_priorizacion': 'COMPLEMENTARIO', 'indicadores': []},
    {'codigo': '3m-Fil-OA03', 'nivel': '3m', 'asignatura': 'Fil', 'eje': 'Ética', 'numero': 3,
     'descripcion': 'Analizar problemas éticos contemporáneos en base a conceptos filosóficos.',
     'priorizado_2025': False, 'nivel_priorizacion': 'COMPLEMENTARIO', 'indicadores': [],
     'articulaciones': [{'asignatura_codigo': 'Edc', 'asignatura_nombre': 'Educación Ciudadana', 'descripcion': 'Ética y ciudadanía'}]},
]

FILOSOFIA_3M_UNIDADES = [
    {'codigo': '3m-Fil-U1', 'nivel': '3m', 'asignatura': 'Fil', 'numero': 1, 'nombre': 'Introducción a la filosofía',
     'descripcion': 'Preguntas fundamentales de la filosofía.',
     'oa_codigos': ['3m-Fil-OA01'], 'oat_codigos': ['OAT-COG-03'], 'habilidades_codigos': [], 'actitudes_codigos': ['Fil-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': False},
    {'codigo': '3m-Fil-U2', 'nivel': '3m', 'asignatura': 'Fil', 'numero': 2, 'nombre': 'Ética y moral',
     'descripcion': 'Problemas éticos contemporáneos. ARTICULABLE CON ED. CIUDADANA.',
     'oa_codigos': ['3m-Fil-OA03'], 'oat_codigos': ['OAT-MOR-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Fil-ACT02'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': False},
]

FILOSOFIA_MEDIA = {
    'actitudes': FILOSOFIA_ACTITUDES,
    'niveles': {
        '3m': {'oas': FILOSOFIA_3M_OAS, 'unidades': FILOSOFIA_3M_UNIDADES},
    }
}


# ==========================================
# EDUCACIÓN CIUDADANA - EDUCACIÓN MEDIA
# ==========================================

CIUDADANA_ACTITUDES = [
    {'codigo': 'Edc-ACT01', 'asignatura': 'Edc', 'numero': 1,
     'descripcion': 'Valorar la democracia y el respeto de los derechos humanos.'},
    {'codigo': 'Edc-ACT02', 'asignatura': 'Edc', 'numero': 2,
     'descripcion': 'Participar de manera activa y responsable en la comunidad.'},
]

CIUDADANA_3M_OAS = [
    {'codigo': '3m-Edc-OA01', 'nivel': '3m', 'asignatura': 'Edc', 'eje': 'Ciudadanía', 'numero': 1,
     'descripcion': 'Identificar los fundamentos, atributos y dimensiones de la democracia.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '3m-Edc-OA05', 'nivel': '3m', 'asignatura': 'Edc', 'eje': 'Derechos Humanos', 'numero': 5,
     'descripcion': 'Evaluar la importancia de los derechos humanos.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': [],
     'articulaciones': [{'asignatura_codigo': 'His', 'asignatura_nombre': 'Historia', 'descripcion': 'Violaciones DDHH en Chile'}]},
]

CIUDADANA_3M_UNIDADES = [
    {'codigo': '3m-Edc-U1', 'nivel': '3m', 'asignatura': 'Edc', 'numero': 1, 'nombre': 'Democracia y participación',
     'descripcion': 'Fundamentos de la democracia.',
     'oa_codigos': ['3m-Edc-OA01'], 'oat_codigos': ['OAT-SOC-02', 'OAT-MOR-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Edc-ACT01', 'Edc-ACT02'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '3m-Edc-U2', 'nivel': '3m', 'asignatura': 'Edc', 'numero': 2, 'nombre': 'Derechos humanos',
     'descripcion': 'DDHH y su importancia. ARTICULABLE CON HISTORIA.',
     'oa_codigos': ['3m-Edc-OA05'], 'oat_codigos': ['OAT-MOR-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Edc-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

CIUDADANA_MEDIA = {
    'actitudes': CIUDADANA_ACTITUDES,
    'niveles': {
        '3m': {'oas': CIUDADANA_3M_OAS, 'unidades': CIUDADANA_3M_UNIDADES},
    }
}


# ==========================================
# HISTORIA - EDUCACIÓN MEDIA
# ==========================================

HISTORIA_MEDIA_1M_OAS = [
    {'codigo': '1m-His-OA01', 'nivel': '1m', 'asignatura': 'His', 'eje': 'Historia', 'numero': 1,
     'descripcion': 'Analizar los principales antecedentes de la Primera Guerra Mundial.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '1m-His-OA08', 'nivel': '1m', 'asignatura': 'His', 'eje': 'Formación Ciudadana', 'numero': 8,
     'descripcion': 'Analizar los conceptos de soberanía y representación política.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

HISTORIA_MEDIA_1M_UNIDADES = [
    {'codigo': '1m-His-U1', 'nivel': '1m', 'asignatura': 'His', 'numero': 1, 'nombre': 'El siglo XX',
     'descripcion': 'Guerras mundiales y sus consecuencias.',
     'oa_codigos': ['1m-His-OA01'], 'oat_codigos': ['OAT-SOC-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT01', 'His-ACT03'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '1m-His-U2', 'nivel': '1m', 'asignatura': 'His', 'numero': 2, 'nombre': 'Democracia',
     'descripcion': 'Soberanía y representación.',
     'oa_codigos': ['1m-His-OA08'], 'oat_codigos': ['OAT-SOC-02', 'OAT-MOR-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT02'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

# II° Medio - Historia
HISTORIA_MEDIA_2M_OAS = [
    {'codigo': '2m-His-OA01', 'nivel': '2m', 'asignatura': 'His', 'eje': 'Historia', 'numero': 1,
     'descripcion': 'Analizar la Guerra Fría como un período histórico caracterizado por la tensión entre dos bloques.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '2m-His-OA05', 'nivel': '2m', 'asignatura': 'His', 'eje': 'Historia', 'numero': 5,
     'descripcion': 'Evaluar el proceso de independencia de los países de América Latina y África.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '2m-His-OA09', 'nivel': '2m', 'asignatura': 'His', 'eje': 'Formación Ciudadana', 'numero': 9,
     'descripcion': 'Analizar la experiencia histórica de Chile en el siglo XX.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

HISTORIA_MEDIA_2M_UNIDADES = [
    {'codigo': '2m-His-U1', 'nivel': '2m', 'asignatura': 'His', 'numero': 1, 'nombre': 'La Guerra Fría',
     'descripcion': 'Tensión entre bloques y sus efectos globales.',
     'oa_codigos': ['2m-His-OA01'], 'oat_codigos': ['OAT-SOC-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT01'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '2m-His-U2', 'nivel': '2m', 'asignatura': 'His', 'numero': 2, 'nombre': 'Descolonización',
     'descripcion': 'Independencia en América Latina y África.',
     'oa_codigos': ['2m-His-OA05'], 'oat_codigos': ['OAT-SOC-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT02'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '2m-His-U3', 'nivel': '2m', 'asignatura': 'His', 'numero': 3, 'nombre': 'Chile siglo XX',
     'descripcion': 'Historia de Chile contemporáneo.',
     'oa_codigos': ['2m-His-OA09'], 'oat_codigos': ['OAT-MOR-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT03'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
]

HISTORIA_MEDIA = {
    'niveles': {
        '1m': {'oas': HISTORIA_MEDIA_1M_OAS, 'unidades': HISTORIA_MEDIA_1M_UNIDADES},
        '2m': {'oas': HISTORIA_MEDIA_2M_OAS, 'unidades': HISTORIA_MEDIA_2M_UNIDADES},
    }
}

# ==========================================
# CIENCIAS PARA LA CIUDADANÍA - I° y II° MEDIO
# ==========================================

CIENCIAS_CIUDADANIA_ACTITUDES = [
    {'codigo': 'CpC-ACT01', 'asignatura': 'CpC', 'numero': 1,
     'descripcion': 'Mostrar curiosidad e interés por conocer y comprender fenómenos del entorno natural y tecnológico.'},
    {'codigo': 'CpC-ACT02', 'asignatura': 'CpC', 'numero': 2,
     'descripcion': 'Manifestar una visión de sustentabilidad del medio ambiente.'},
]

CIENCIAS_CPC_1M_OAS = [
    {'codigo': '1m-CpC-OA01', 'nivel': '1m', 'asignatura': 'CpC', 'eje': 'Bienestar y Salud', 'numero': 1,
     'descripcion': 'Explicar los factores biológicos, ambientales y sociales que afectan la salud humana.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '1m-CpC-OA03', 'nivel': '1m', 'asignatura': 'CpC', 'eje': 'Bienestar y Salud', 'numero': 3,
     'descripcion': 'Analizar los componentes de una alimentación equilibrada.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
]

CIENCIAS_CPC_1M_UNIDADES = [
    {'codigo': '1m-CpC-U1', 'nivel': '1m', 'asignatura': 'CpC', 'numero': 1, 'nombre': 'Salud y bienestar',
     'descripcion': 'Factores de la salud humana.',
     'oa_codigos': ['1m-CpC-OA01', '1m-CpC-OA03'], 'oat_codigos': ['OAT-AFE-02', 'OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['CpC-ACT01'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
]

CIENCIAS_CPC_2M_OAS = [
    {'codigo': '2m-CpC-OA01', 'nivel': '2m', 'asignatura': 'CpC', 'eje': 'Ambiente y Sostenibilidad', 'numero': 1,
     'descripcion': 'Evaluar el impacto ambiental de las actividades humanas y proponer acciones de mitigación.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '2m-CpC-OA04', 'nivel': '2m', 'asignatura': 'CpC', 'eje': 'Tecnología', 'numero': 4,
     'descripcion': 'Analizar cómo la tecnología ha modificado las formas de vida de las personas.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
]

CIENCIAS_CPC_2M_UNIDADES = [
    {'codigo': '2m-CpC-U1', 'nivel': '2m', 'asignatura': 'CpC', 'numero': 1, 'nombre': 'Sostenibilidad ambiental',
     'descripcion': 'Impacto ambiental y acciones.',
     'oa_codigos': ['2m-CpC-OA01'], 'oat_codigos': ['OAT-SOC-01', 'OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['CpC-ACT02'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '2m-CpC-U2', 'nivel': '2m', 'asignatura': 'CpC', 'numero': 2, 'nombre': 'Tecnología y sociedad',
     'descripcion': 'Impacto de la tecnología.',
     'oa_codigos': ['2m-CpC-OA04'], 'oat_codigos': ['OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['CpC-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

CIENCIAS_CIUDADANIA_MEDIA = {
    'actitudes': CIENCIAS_CIUDADANIA_ACTITUDES,
    'niveles': {
        '1m': {'oas': CIENCIAS_CPC_1M_OAS, 'unidades': CIENCIAS_CPC_1M_UNIDADES},
        '2m': {'oas': CIENCIAS_CPC_2M_OAS, 'unidades': CIENCIAS_CPC_2M_UNIDADES},
    }
}
