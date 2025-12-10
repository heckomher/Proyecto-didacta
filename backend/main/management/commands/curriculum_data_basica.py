"""
Datos del Currículum Nacional Chileno - Educación Básica
Archivo de datos separado para mantener modularidad
"""

# ==========================================
# MATEMÁTICA - EDUCACIÓN BÁSICA (1° a 8°)
# ==========================================

MATEMATICA_ACTITUDES = [
    {'codigo': 'Mat-ACT01', 'asignatura': 'Mat', 'numero': 1,
     'descripcion': 'Manifestar curiosidad e interés por el aprendizaje de las matemáticas.'},
    {'codigo': 'Mat-ACT02', 'asignatura': 'Mat', 'numero': 2,
     'descripcion': 'Abordar de manera flexible y creativa la búsqueda de soluciones a problemas.'},
    {'codigo': 'Mat-ACT03', 'asignatura': 'Mat', 'numero': 3,
     'descripcion': 'Manifestar una actitud positiva frente a sí mismo y sus capacidades.'},
    {'codigo': 'Mat-ACT04', 'asignatura': 'Mat', 'numero': 4,
     'descripcion': 'Expresar y escuchar ideas de forma respetuosa.'},
]

# 1° Básico - Matemática
MATEMATICA_1B_OAS = [
    {
        'codigo': '1b-Mat-OA01', 'nivel': '1b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 1,
        'descripcion': 'Contar números del 0 al 100, de 1 en 1, de 2 en 2, de 5 en 5 y de 10 en 10, hacia adelante y hacia atrás.',
        'priorizado_2025': True, 'nivel_priorizacion': 'P1',
        'indicadores': [
            {'codigo': '1b-Mat-OA01-I1', 'descripcion': 'Contar de 1 en 1 hasta 100.', 'verbo_infinitivo': 'Contar'},
            {'codigo': '1b-Mat-OA01-I2', 'descripcion': 'Contar de 2 en 2 hasta 20.', 'verbo_infinitivo': 'Contar'},
        ]
    },
    {
        'codigo': '1b-Mat-OA02', 'nivel': '1b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 2,
        'descripcion': 'Leer números del 0 al 20 y representarlos en forma concreta, pictórica y simbólica.',
        'priorizado_2025': True, 'nivel_priorizacion': 'P1',
        'indicadores': [
            {'codigo': '1b-Mat-OA02-I1', 'descripcion': 'Leer números del 0 al 20.', 'verbo_infinitivo': 'Leer'},
            {'codigo': '1b-Mat-OA02-I2', 'descripcion': 'Representar números con material concreto.', 'verbo_infinitivo': 'Representar'},
        ]
    },
    {
        'codigo': '1b-Mat-OA03', 'nivel': '1b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 3,
        'descripcion': 'Comparar y ordenar números del 0 al 20 de menor a mayor y viceversa.',
        'priorizado_2025': True, 'nivel_priorizacion': 'P1',
        'indicadores': [
            {'codigo': '1b-Mat-OA03-I1', 'descripcion': 'Comparar números usando mayor que, menor que.', 'verbo_infinitivo': 'Comparar'},
            {'codigo': '1b-Mat-OA03-I2', 'descripcion': 'Ordenar secuencias numéricas.', 'verbo_infinitivo': 'Ordenar'},
        ]
    },
    {
        'codigo': '1b-Mat-OA09', 'nivel': '1b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 9,
        'descripcion': 'Demostrar que comprenden la adición y la sustracción de números del 0 al 20.',
        'priorizado_2025': True, 'nivel_priorizacion': 'P1',
        'indicadores': [
            {'codigo': '1b-Mat-OA09-I1', 'descripcion': 'Resolver adiciones con números hasta 20.', 'verbo_infinitivo': 'Resolver'},
            {'codigo': '1b-Mat-OA09-I2', 'descripcion': 'Resolver sustracciones con números hasta 20.', 'verbo_infinitivo': 'Resolver'},
        ]
    },
    {
        'codigo': '1b-Mat-OA14', 'nivel': '1b', 'asignatura': 'Mat', 'eje': 'Geometría', 'numero': 14,
        'descripcion': 'Identificar en el entorno figuras 3D como cubos, paralelepípedos, esferas, conos, cilindros y las figuras 2D asociadas.',
        'priorizado_2025': True, 'nivel_priorizacion': 'P2',
        'indicadores': [
            {'codigo': '1b-Mat-OA14-I1', 'descripcion': 'Identificar figuras 3D en el entorno.', 'verbo_infinitivo': 'Identificar'},
            {'codigo': '1b-Mat-OA14-I2', 'descripcion': 'Nombrar figuras geométricas básicas.', 'verbo_infinitivo': 'Nombrar'},
        ]
    },
    {
        'codigo': '1b-Mat-OA17', 'nivel': '1b', 'asignatura': 'Mat', 'eje': 'Patrones y Álgebra', 'numero': 17,
        'descripcion': 'Describir y aplicar estrategias de cálculo mental para las adiciones y sustracciones hasta 20.',
        'priorizado_2025': True, 'nivel_priorizacion': 'P1',
        'indicadores': [
            {'codigo': '1b-Mat-OA17-I1', 'descripcion': 'Aplicar estrategias de cálculo mental.', 'verbo_infinitivo': 'Aplicar'},
        ]
    },
]

MATEMATICA_1B_UNIDADES = [
    {
        'codigo': '1b-Mat-U1', 'nivel': '1b', 'asignatura': 'Mat', 'numero': 1,
        'nombre': 'Números hasta el 20',
        'descripcion': 'Conteo, lectura, escritura y comparación de números del 0 al 20.',
        'oa_codigos': ['1b-Mat-OA01', '1b-Mat-OA02', '1b-Mat-OA03'],
        'oat_codigos': ['OAT-COG-01', 'OAT-COG-04'],
        'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01', 'Mat-ACT03'],
        'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True
    },
    {
        'codigo': '1b-Mat-U2', 'nivel': '1b', 'asignatura': 'Mat', 'numero': 2,
        'nombre': 'Adición y sustracción',
        'descripcion': 'Operaciones básicas con números hasta 20.',
        'oa_codigos': ['1b-Mat-OA09', '1b-Mat-OA17'],
        'oat_codigos': ['OAT-COG-04'],
        'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01', 'Mat-ACT02'],
        'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True
    },
    {
        'codigo': '1b-Mat-U3', 'nivel': '1b', 'asignatura': 'Mat', 'numero': 3,
        'nombre': 'Geometría básica',
        'descripcion': 'Figuras 2D y 3D en el entorno.',
        'oa_codigos': ['1b-Mat-OA14'],
        'oat_codigos': ['OAT-COG-01'],
        'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01'],
        'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True
    },
]

# 2° Básico - Matemática
MATEMATICA_2B_OAS = [
    {
        'codigo': '2b-Mat-OA01', 'nivel': '2b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 1,
        'descripcion': 'Contar números del 0 al 1000, de 1 en 1, de 2 en 2, de 5 en 5 y de 10 en 10.',
        'priorizado_2025': True, 'nivel_priorizacion': 'P1',
        'indicadores': [
            {'codigo': '2b-Mat-OA01-I1', 'descripcion': 'Contar de 10 en 10 hasta 1000.', 'verbo_infinitivo': 'Contar'},
        ]
    },
    {
        'codigo': '2b-Mat-OA02', 'nivel': '2b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 2,
        'descripcion': 'Leer números del 0 al 100 y representarlos en forma concreta, pictórica y simbólica.',
        'priorizado_2025': True, 'nivel_priorizacion': 'P1',
        'indicadores': [
            {'codigo': '2b-Mat-OA02-I1', 'descripcion': 'Leer números del 0 al 100.', 'verbo_infinitivo': 'Leer'},
        ]
    },
    {
        'codigo': '2b-Mat-OA06', 'nivel': '2b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 6,
        'descripcion': 'Demostrar que comprenden la adición y la sustracción en el ámbito del 0 al 100.',
        'priorizado_2025': True, 'nivel_priorizacion': 'P1',
        'indicadores': [
            {'codigo': '2b-Mat-OA06-I1', 'descripcion': 'Resolver problemas de adición hasta 100.', 'verbo_infinitivo': 'Resolver'},
        ]
    },
    {
        'codigo': '2b-Mat-OA11', 'nivel': '2b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 11,
        'descripcion': 'Demostrar que comprenden la multiplicación como arreglos, grupos iguales y sumar repetidamente.',
        'priorizado_2025': True, 'nivel_priorizacion': 'P1',
        'indicadores': [
            {'codigo': '2b-Mat-OA11-I1', 'descripcion': 'Representar multiplicaciones con arreglos.', 'verbo_infinitivo': 'Representar'},
        ]
    },
]

MATEMATICA_2B_UNIDADES = [
    {
        'codigo': '2b-Mat-U1', 'nivel': '2b', 'asignatura': 'Mat', 'numero': 1,
        'nombre': 'Números hasta el 100',
        'descripcion': 'Conteo, lectura y operaciones con números hasta 100.',
        'oa_codigos': ['2b-Mat-OA01', '2b-Mat-OA02', '2b-Mat-OA06'],
        'oat_codigos': ['OAT-COG-01', 'OAT-COG-04'],
        'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01', 'Mat-ACT03'],
        'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True
    },
    {
        'codigo': '2b-Mat-U2', 'nivel': '2b', 'asignatura': 'Mat', 'numero': 2,
        'nombre': 'Introducción a la multiplicación',
        'descripcion': 'Concepto de multiplicación como suma repetida.',
        'oa_codigos': ['2b-Mat-OA11'],
        'oat_codigos': ['OAT-COG-04'],
        'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT02'],
        'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True
    },
]

# 3° - 8° Básico Matemática (estructura simplificada)
MATEMATICA_3B_OAS = [
    {'codigo': '3b-Mat-OA01', 'nivel': '3b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 1,
     'descripcion': 'Contar números del 0 al 10 000, de 10 en 10, de 100 en 100.', 'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '3b-Mat-OA08', 'nivel': '3b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 8,
     'descripcion': 'Demostrar que comprenden las tablas de multiplicar hasta 10 de manera progresiva.', 'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '3b-Mat-OA13', 'nivel': '3b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 13,
     'descripcion': 'Demostrar que comprenden las fracciones de uso común.', 'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

MATEMATICA_3B_UNIDADES = [
    {'codigo': '3b-Mat-U1', 'nivel': '3b', 'asignatura': 'Mat', 'numero': 1, 'nombre': 'Números hasta 10.000',
     'descripcion': 'Lectura, escritura y operaciones con números hasta 10.000.',
     'oa_codigos': ['3b-Mat-OA01'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '3b-Mat-U2', 'nivel': '3b', 'asignatura': 'Mat', 'numero': 2, 'nombre': 'Multiplicación y división',
     'descripcion': 'Tablas de multiplicar y división exacta.',
     'oa_codigos': ['3b-Mat-OA08'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT02'],
     'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True},
    {'codigo': '3b-Mat-U3', 'nivel': '3b', 'asignatura': 'Mat', 'numero': 3, 'nombre': 'Fracciones',
     'descripcion': 'Introducción a las fracciones.',
     'oa_codigos': ['3b-Mat-OA13'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

MATEMATICA_4B_OAS = [
    {'codigo': '4b-Mat-OA01', 'nivel': '4b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 1,
     'descripcion': 'Representar y describir números del 0 al 10 000.', 'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '4b-Mat-OA06', 'nivel': '4b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 6,
     'descripcion': 'Demostrar que comprenden la multiplicación de números de tres dígitos por números de un dígito.', 'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '4b-Mat-OA10', 'nivel': '4b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 10,
     'descripcion': 'Demostrar que comprenden las fracciones con denominadores 100, 12, 10, 8, 6, 5, 4, 3, 2.', 'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

MATEMATICA_4B_UNIDADES = [
    {'codigo': '4b-Mat-U1', 'nivel': '4b', 'asignatura': 'Mat', 'numero': 1, 'nombre': 'Números grandes',
     'descripcion': 'Números hasta 10.000 y sus operaciones.',
     'oa_codigos': ['4b-Mat-OA01', '4b-Mat-OA06'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01'],
     'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True},
    {'codigo': '4b-Mat-U2', 'nivel': '4b', 'asignatura': 'Mat', 'numero': 2, 'nombre': 'Fracciones y decimales',
     'descripcion': 'Fracciones y su relación con decimales.',
     'oa_codigos': ['4b-Mat-OA10'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT02'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
]

MATEMATICA_5B_OAS = [
    {'codigo': '5b-Mat-OA01', 'nivel': '5b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 1,
     'descripcion': 'Representar y describir números naturales de hasta más de 6 dígitos.', 'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '5b-Mat-OA06', 'nivel': '5b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 6,
     'descripcion': 'Demostrar que comprenden la división con dividendos de tres dígitos y divisores de un dígito.', 'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '5b-Mat-OA08', 'nivel': '5b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 8,
     'descripcion': 'Demostrar que comprenden las fracciones propias e impropias y números mixtos.', 'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

MATEMATICA_5B_UNIDADES = [
    {'codigo': '5b-Mat-U1', 'nivel': '5b', 'asignatura': 'Mat', 'numero': 1, 'nombre': 'Números naturales grandes',
     'descripcion': 'Operaciones con números de más de 6 dígitos.',
     'oa_codigos': ['5b-Mat-OA01', '5b-Mat-OA06'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '5b-Mat-U2', 'nivel': '5b', 'asignatura': 'Mat', 'numero': 2, 'nombre': 'Fracciones avanzadas',
     'descripcion': 'Fracciones propias, impropias y números mixtos.',
     'oa_codigos': ['5b-Mat-OA08'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT02'],
     'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True},
]

MATEMATICA_6B_OAS = [
    {'codigo': '6b-Mat-OA01', 'nivel': '6b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 1,
     'descripcion': 'Demostrar que comprenden los factores y múltiplos.', 'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '6b-Mat-OA04', 'nivel': '6b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 4,
     'descripcion': 'Demostrar que comprenden el concepto de razón y su aplicación.', 'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '6b-Mat-OA07', 'nivel': '6b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 7,
     'descripcion': 'Demostrar que comprenden el concepto de porcentaje.', 'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

MATEMATICA_6B_UNIDADES = [
    {'codigo': '6b-Mat-U1', 'nivel': '6b', 'asignatura': 'Mat', 'numero': 1, 'nombre': 'Factores y múltiplos',
     'descripcion': 'Divisibilidad, factores y múltiplos.',
     'oa_codigos': ['6b-Mat-OA01'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '6b-Mat-U2', 'nivel': '6b', 'asignatura': 'Mat', 'numero': 2, 'nombre': 'Razones y porcentajes',
     'descripcion': 'Concepto de razón, proporción y porcentaje.',
     'oa_codigos': ['6b-Mat-OA04', '6b-Mat-OA07'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT02'],
     'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True},
]

MATEMATICA_7B_OAS = [
    {'codigo': '7b-Mat-OA01', 'nivel': '7b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 1,
     'descripcion': 'Mostrar que comprenden los números enteros.', 'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '7b-Mat-OA04', 'nivel': '7b', 'asignatura': 'Mat', 'eje': 'Álgebra', 'numero': 4,
     'descripcion': 'Mostrar que comprenden el concepto de expresión algebraica.', 'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '7b-Mat-OA09', 'nivel': '7b', 'asignatura': 'Mat', 'eje': 'Geometría', 'numero': 9,
     'descripcion': 'Mostrar que comprenden las relaciones entre ángulos.', 'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
]

MATEMATICA_7B_UNIDADES = [
    {'codigo': '7b-Mat-U1', 'nivel': '7b', 'asignatura': 'Mat', 'numero': 1, 'nombre': 'Números enteros',
     'descripcion': 'Concepto y operaciones con números enteros.',
     'oa_codigos': ['7b-Mat-OA01'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '7b-Mat-U2', 'nivel': '7b', 'asignatura': 'Mat', 'numero': 2, 'nombre': 'Introducción al álgebra',
     'descripcion': 'Expresiones algebraicas básicas.',
     'oa_codigos': ['7b-Mat-OA04'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT02'],
     'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True},
    {'codigo': '7b-Mat-U3', 'nivel': '7b', 'asignatura': 'Mat', 'numero': 3, 'nombre': 'Geometría y ángulos',
     'descripcion': 'Relaciones entre ángulos.',
     'oa_codigos': ['7b-Mat-OA09'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

MATEMATICA_8B_OAS = [
    {'codigo': '8b-Mat-OA01', 'nivel': '8b', 'asignatura': 'Mat', 'eje': 'Números y Operaciones', 'numero': 1,
     'descripcion': 'Mostrar que comprenden los números racionales positivos y negativos.', 'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '8b-Mat-OA04', 'nivel': '8b', 'asignatura': 'Mat', 'eje': 'Álgebra', 'numero': 4,
     'descripcion': 'Mostrar que comprenden la función lineal.', 'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '8b-Mat-OA08', 'nivel': '8b', 'asignatura': 'Mat', 'eje': 'Geometría', 'numero': 8,
     'descripcion': 'Mostrar que comprenden el teorema de Pitágoras.', 'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

MATEMATICA_8B_UNIDADES = [
    {'codigo': '8b-Mat-U1', 'nivel': '8b', 'asignatura': 'Mat', 'numero': 1, 'nombre': 'Números racionales',
     'descripcion': 'Operaciones con números racionales.',
     'oa_codigos': ['8b-Mat-OA01'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '8b-Mat-U2', 'nivel': '8b', 'asignatura': 'Mat', 'numero': 2, 'nombre': 'Función lineal',
     'descripcion': 'Concepto y gráfico de función lineal.',
     'oa_codigos': ['8b-Mat-OA04'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT02'],
     'horas_sugeridas': 60, 'semanas_sugeridas': 8, 'priorizado_2025': True},
    {'codigo': '8b-Mat-U3', 'nivel': '8b', 'asignatura': 'Mat', 'numero': 3, 'nombre': 'Teorema de Pitágoras',
     'descripcion': 'Aplicación del teorema de Pitágoras.',
     'oa_codigos': ['8b-Mat-OA08'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Mat-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

# Consolidar todos los datos de Matemática
MATEMATICA_BASICA = {
    'actitudes': MATEMATICA_ACTITUDES,
    'niveles': {
        '1b': {'oas': MATEMATICA_1B_OAS, 'unidades': MATEMATICA_1B_UNIDADES},
        '2b': {'oas': MATEMATICA_2B_OAS, 'unidades': MATEMATICA_2B_UNIDADES},
        '3b': {'oas': MATEMATICA_3B_OAS, 'unidades': MATEMATICA_3B_UNIDADES},
        '4b': {'oas': MATEMATICA_4B_OAS, 'unidades': MATEMATICA_4B_UNIDADES},
        '5b': {'oas': MATEMATICA_5B_OAS, 'unidades': MATEMATICA_5B_UNIDADES},
        '6b': {'oas': MATEMATICA_6B_OAS, 'unidades': MATEMATICA_6B_UNIDADES},
        '7b': {'oas': MATEMATICA_7B_OAS, 'unidades': MATEMATICA_7B_UNIDADES},
        '8b': {'oas': MATEMATICA_8B_OAS, 'unidades': MATEMATICA_8B_UNIDADES},
    }
}


# ==========================================
# CIENCIAS NATURALES - EDUCACIÓN BÁSICA
# ==========================================

CIENCIAS_ACTITUDES = [
    {'codigo': 'Cna-ACT01', 'asignatura': 'Cna', 'numero': 1,
     'descripcion': 'Demostrar curiosidad e interés por conocer fenómenos naturales.'},
    {'codigo': 'Cna-ACT02', 'asignatura': 'Cna', 'numero': 2,
     'descripcion': 'Manifestar un estilo de trabajo riguroso y perseverante para lograr los aprendizajes.'},
    {'codigo': 'Cna-ACT03', 'asignatura': 'Cna', 'numero': 3,
     'descripcion': 'Reconocer la importancia del entorno natural y sus recursos.'},
]

CIENCIAS_1B_OAS = [
    {'codigo': '1b-Cna-OA01', 'nivel': '1b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 1,
     'descripcion': 'Reconocer y observar, por medio de la exploración, que los seres vivos crecen, responden a estímulos del medio, se reproducen y necesitan agua, alimento y aire para vivir.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '1b-Cna-OA03', 'nivel': '1b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 3,
     'descripcion': 'Observar e identificar, por medio de la exploración, las estructuras principales de las plantas: hojas, flores, tallos y raíces.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '1b-Cna-OA07', 'nivel': '1b', 'asignatura': 'Cna', 'eje': 'Ciencias Físicas y Químicas', 'numero': 7,
     'descripcion': 'Describir y agrupar los materiales según sus propiedades.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P2', 'indicadores': []},
]

CIENCIAS_1B_UNIDADES = [
    {'codigo': '1b-Cna-U1', 'nivel': '1b', 'asignatura': 'Cna', 'numero': 1, 'nombre': 'Los seres vivos',
     'descripcion': 'Características de los seres vivos y sus necesidades.',
     'oa_codigos': ['1b-Cna-OA01', '1b-Cna-OA03'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT01', 'Cna-ACT03'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '1b-Cna-U2', 'nivel': '1b', 'asignatura': 'Cna', 'numero': 2, 'nombre': 'Los materiales',
     'descripcion': 'Propiedades de los materiales.',
     'oa_codigos': ['1b-Cna-OA07'], 'oat_codigos': ['OAT-COG-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT01', 'Cna-ACT02'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

# 8° Básico Ciencias con articulación
CIENCIAS_8B_OAS = [
    {'codigo': '8b-Cna-OA01', 'nivel': '8b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 1,
     'descripcion': 'Explicar, basándose en evidencias, que la célula es la unidad estructural y funcional de los seres vivos.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '8b-Cna-OA06', 'nivel': '8b', 'asignatura': 'Cna', 'eje': 'Ciencias de la Vida', 'numero': 6,
     'descripcion': 'Investigar y explicar las características de los nutrientes (carbohidratos, proteínas, lípidos y vitaminas) y sus efectos para la salud.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': [],
     'articulaciones': [{'asignatura_codigo': 'Efs', 'asignatura_nombre': 'Educación Física y Salud', 'descripcion': 'Nutrición y actividad física'}]},
    {'codigo': '8b-Cna-OA08', 'nivel': '8b', 'asignatura': 'Cna', 'eje': 'Ciencias Físicas y Químicas', 'numero': 8,
     'descripcion': 'Desarrollar modelos que expliquen la relación entre los cambios de materia y la conservación de la masa.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
]

CIENCIAS_8B_UNIDADES = [
    {'codigo': '8b-Cna-U1', 'nivel': '8b', 'asignatura': 'Cna', 'numero': 1, 'nombre': 'La célula',
     'descripcion': 'Estructura y función celular.',
     'oa_codigos': ['8b-Cna-OA01'], 'oat_codigos': ['OAT-COG-01', 'OAT-COG-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT01'],
     'horas_sugeridas': 50, 'semanas_sugeridas': 6, 'priorizado_2025': True},
    {'codigo': '8b-Cna-U2', 'nivel': '8b', 'asignatura': 'Cna', 'numero': 2, 'nombre': 'Nutrición y salud',
     'descripcion': 'Nutrientes y alimentación saludable. ARTICULABLE CON ED. FÍSICA.',
     'oa_codigos': ['8b-Cna-OA06'], 'oat_codigos': ['OAT-AFE-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT03'],
     'horas_sugeridas': 45, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '8b-Cna-U3', 'nivel': '8b', 'asignatura': 'Cna', 'numero': 3, 'nombre': 'Cambios de la materia',
     'descripcion': 'Conservación de la masa en cambios químicos.',
     'oa_codigos': ['8b-Cna-OA08'], 'oat_codigos': ['OAT-COG-04'], 'habilidades_codigos': [], 'actitudes_codigos': ['Cna-ACT02'],
     'horas_sugeridas': 45, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

CIENCIAS_BASICA = {
    'actitudes': CIENCIAS_ACTITUDES,
    'niveles': {
        '1b': {'oas': CIENCIAS_1B_OAS, 'unidades': CIENCIAS_1B_UNIDADES},
        '8b': {'oas': CIENCIAS_8B_OAS, 'unidades': CIENCIAS_8B_UNIDADES},
    }
}


# ==========================================
# HISTORIA, GEOGRAFÍA Y CS. SOCIALES
# ==========================================

HISTORIA_ACTITUDES = [
    {'codigo': 'His-ACT01', 'asignatura': 'His', 'numero': 1,
     'descripcion': 'Demostrar valoración por la vida en sociedad para el desarrollo y crecimiento de la persona.'},
    {'codigo': 'His-ACT02', 'asignatura': 'His', 'numero': 2,
     'descripcion': 'Comportarse y actuar en la vida cotidiana según principios y virtudes ciudadanas.'},
    {'codigo': 'His-ACT03', 'asignatura': 'His', 'numero': 3,
     'descripcion': 'Establecer lazos de pertenencia con su entorno social y natural a partir del conocimiento.'},
]

HISTORIA_1B_OAS = [
    {'codigo': '1b-His-OA01', 'nivel': '1b', 'asignatura': 'His', 'eje': 'Historia', 'numero': 1,
     'descripcion': 'Nombrar y secuenciar días de la semana y meses del año, utilizando calendarios.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '1b-His-OA05', 'nivel': '1b', 'asignatura': 'His', 'eje': 'Geografía', 'numero': 5,
     'descripcion': 'Reconocer los símbolos representativos de Chile (bandera, escudo, himno nacional).',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '1b-His-OA08', 'nivel': '1b', 'asignatura': 'His', 'eje': 'Formación Ciudadana', 'numero': 8,
     'descripcion': 'Reconocer que los niños tienen derechos que les permiten recibir un cuidado especial.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
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
     'oa_codigos': ['1b-His-OA08'], 'oat_codigos': ['OAT-MOR-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['His-ACT02'],
     'horas_sugeridas': 30, 'semanas_sugeridas': 4, 'priorizado_2025': True},
]

HISTORIA_BASICA = {
    'actitudes': HISTORIA_ACTITUDES,
    'niveles': {
        '1b': {'oas': HISTORIA_1B_OAS, 'unidades': HISTORIA_1B_UNIDADES},
    }
}


# ==========================================
# EDUCACIÓN FÍSICA Y SALUD
# ==========================================

EDUFISICA_ACTITUDES = [
    {'codigo': 'Efs-ACT01', 'asignatura': 'Efs', 'numero': 1,
     'descripcion': 'Valorar los efectos positivos de la práctica regular de actividad física para la salud.'},
    {'codigo': 'Efs-ACT02', 'asignatura': 'Efs', 'numero': 2,
     'descripcion': 'Demostrar disposición a mejorar su condición física e interés por practicar actividad física de forma regular.'},
]

EDUFISICA_8B_OAS = [
    {'codigo': '8b-Efs-OA01', 'nivel': '8b', 'asignatura': 'Efs', 'eje': 'Habilidades Motrices', 'numero': 1,
     'descripcion': 'Aplicar habilidades motrices especializadas en situaciones de juego.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': []},
    {'codigo': '8b-Efs-OA06', 'nivel': '8b', 'asignatura': 'Efs', 'eje': 'Vida Activa y Saludable', 'numero': 6,
     'descripcion': 'Practicar regularmente una variedad de actividades físicas para mantener la salud.',
     'priorizado_2025': True, 'nivel_priorizacion': 'P1', 'indicadores': [],
     'articulaciones': [{'asignatura_codigo': 'Cna', 'asignatura_nombre': 'Ciencias Naturales', 'descripcion': 'Nutrición y metabolismo'}]},
]

EDUFISICA_8B_UNIDADES = [
    {'codigo': '8b-Efs-U1', 'nivel': '8b', 'asignatura': 'Efs', 'numero': 1, 'nombre': 'Deportes colectivos',
     'descripcion': 'Habilidades motrices en deportes de equipo.',
     'oa_codigos': ['8b-Efs-OA01'], 'oat_codigos': ['OAT-SOC-02'], 'habilidades_codigos': [], 'actitudes_codigos': ['Efs-ACT02'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
    {'codigo': '8b-Efs-U2', 'nivel': '8b', 'asignatura': 'Efs', 'numero': 2, 'nombre': 'Vida saludable',
     'descripcion': 'Actividad física y nutrición. ARTICULABLE CON CIENCIAS.',
     'oa_codigos': ['8b-Efs-OA06'], 'oat_codigos': ['OAT-AFE-01'], 'habilidades_codigos': [], 'actitudes_codigos': ['Efs-ACT01'],
     'horas_sugeridas': 40, 'semanas_sugeridas': 5, 'priorizado_2025': True},
]

EDUFISICA_BASICA = {
    'actitudes': EDUFISICA_ACTITUDES,
    'niveles': {
        '8b': {'oas': EDUFISICA_8B_OAS, 'unidades': EDUFISICA_8B_UNIDADES},
    }
}
