"""
Modelos MongoDB para el Currículum Nacional Chileno (MINEDUC)
Usa mongoengine para interactuar con MongoDB
"""
from mongoengine import (
    Document, EmbeddedDocument, 
    StringField, IntField, BooleanField, ListField, 
    EmbeddedDocumentField, DateTimeField
)
from datetime import datetime


class IndicadorEvaluacion(EmbeddedDocument):
    """
    Indicador de evaluación asociado a un OA.
    Los verbos deben estar en INFINITIVO.
    Ejemplo: "1b-Lyc-OA1-I1"
    """
    codigo = StringField(required=True)  # Ej: "1b-Lyc-OA1-I1"
    descripcion = StringField(required=True)  # "Identificar los sonidos..."
    verbo_infinitivo = StringField()  # "Identificar"
    
    def __str__(self):
        return f"{self.codigo}: {self.descripcion[:50]}..."


class ArticulacionCurricular(EmbeddedDocument):
    """
    Articulación entre asignaturas del mismo nivel.
    Ejemplo: OA de Ciencias Naturales articulable con Ed. Física
    """
    asignatura_codigo = StringField(required=True)  # "Efs", "Lyc", etc.
    asignatura_nombre = StringField(required=True)  # "Educación Física y Salud"
    oa_relacionado = StringField()  # Código del OA relacionado si existe
    descripcion = StringField()  # Descripción de la articulación
    
    def __str__(self):
        return f"Articulable con {self.asignatura_nombre}"


class ObjetivoAprendizaje(Document):
    """
    Objetivo de Aprendizaje (OA) del Currículum Nacional.
    Nomenclatura: {nivel}-{asignatura}-OA{numero}
    Ejemplo: "1b-Lyc-OA1" = 1° Básico, Lenguaje y Comunicación, OA 1
    """
    # Identificación única
    codigo = StringField(primary_key=True)  # "1b-Lyc-OA1"
    
    # Clasificación
    nivel = StringField(required=True)  # "1b", "2b", ..., "1m", "2m", "3m", "4m"
    asignatura = StringField(required=True)  # "Lyc", "Mat", "Cna", "His"
    eje = StringField()  # Eje temático dentro de la asignatura
    numero = IntField(required=True)  # Número del OA
    
    # Contenido
    descripcion = StringField(required=True)
    habilidades_asociadas = ListField(StringField())  # Códigos de habilidades
    conocimientos_previos = ListField(StringField())  # OAs prerrequisitos
    
    # Indicadores de evaluación (embebidos)
    indicadores = ListField(EmbeddedDocumentField(IndicadorEvaluacion))
    
    # Articulación curricular con otras asignaturas
    articulaciones_con = ListField(EmbeddedDocumentField(ArticulacionCurricular))
    
    # Priorización curricular
    priorizado_2025 = BooleanField(default=False)
    nivel_priorizacion = StringField(choices=['P1', 'P2', 'P3', 'COMPLEMENTARIO'])
    
    # Metadatos
    fecha_creacion = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'objetivos_aprendizaje',
        'indexes': ['nivel', 'asignatura', 'eje', 'priorizado_2025']
    }
    
    def __str__(self):
        return f"{self.codigo}: {self.descripcion[:50]}..."



class ObjetivoTransversal(Document):
    """
    Objetivos de Aprendizaje Transversales (OAT).
    Son comunes a todas las asignaturas.
    Nomenclatura: OAT-{dimension}-{numero}
    Ejemplo: "OAT-COG-01" = OAT Cognitivo 01
    """
    codigo = StringField(primary_key=True)  # "OAT-COG-01"
    
    # Clasificación
    dimension = StringField(required=True, choices=[
        'FISICA', 'AFECTIVA', 'COGNITIVA', 'SOCIOCULTURAL', 'MORAL', 'ESPIRITUAL'
    ])
    numero = IntField(required=True)
    
    # Contenido
    descripcion = StringField(required=True)
    
    meta = {
        'collection': 'objetivos_transversales',
        'indexes': ['dimension']
    }
    
    def __str__(self):
        return f"{self.codigo}: {self.descripcion[:50]}..."


class Habilidad(Document):
    """
    Habilidades específicas por asignatura.
    Nomenclatura: {nivel}-{asignatura}-HAB{numero}
    Ejemplo: "1b-Lyc-HAB01"
    """
    codigo = StringField(primary_key=True)  # "1b-Lyc-HAB01"
    
    # Clasificación
    nivel = StringField(required=True)
    asignatura = StringField(required=True)
    numero = IntField(required=True)
    
    # Contenido
    descripcion = StringField(required=True)
    tipo = StringField(choices=['BASICA', 'INTERMEDIA', 'AVANZADA'])
    
    meta = {
        'collection': 'habilidades',
        'indexes': ['nivel', 'asignatura']
    }
    
    def __str__(self):
        return f"{self.codigo}: {self.descripcion[:50]}..."


class Actitud(Document):
    """
    Actitudes a desarrollar (disciplinares o transversales).
    Nomenclatura: {asignatura}-ACT{numero} o TRANS-ACT{numero}
    Ejemplo: "Lyc-ACT01" o "TRANS-ACT01"
    """
    codigo = StringField(primary_key=True)  # "Lyc-ACT01"
    
    # Clasificación
    asignatura = StringField(required=True)  # "Lyc", "Mat", o "TRANS"
    numero = IntField(required=True)
    
    # Contenido
    descripcion = StringField(required=True)
    
    meta = {
        'collection': 'actitudes',
        'indexes': ['asignatura']
    }
    
    def __str__(self):
        return f"{self.codigo}: {self.descripcion[:50]}..."


class UnidadCurricular(Document):
    """
    Unidad Curricular definida por MINEDUC.
    Nomenclatura: {nivel}-{asignatura}-U{numero}
    Ejemplo: "1b-Lyc-U1" = 1° Básico, Lenguaje, Unidad 1
    """
    codigo = StringField(primary_key=True)  # "1b-Lyc-U1"
    
    # Clasificación
    nivel = StringField(required=True)  # "1b", "2b", etc.
    asignatura = StringField(required=True)  # "Lyc", "Mat", etc.
    numero = IntField(required=True)  # Número de unidad
    
    # Contenido
    nombre = StringField(required=True)  # "Descubriendo el lenguaje"
    descripcion = StringField()
    
    # Referencias a OA, OAT, Habilidades, Actitudes (por código)
    oa_codigos = ListField(StringField())  # ["1b-Lyc-OA1", "1b-Lyc-OA2"]
    oat_codigos = ListField(StringField())  # ["OAT-COG-01"]
    habilidades_codigos = ListField(StringField())  # ["1b-Lyc-HAB01"]
    actitudes_codigos = ListField(StringField())  # ["Lyc-ACT01"]
    
    # Tiempo
    horas_sugeridas = IntField(default=40)
    semanas_sugeridas = IntField(default=4)
    
    # Priorización
    priorizado_2025 = BooleanField(default=False)
    
    meta = {
        'collection': 'unidades_curriculares',
        'indexes': ['nivel', 'asignatura', 'priorizado_2025']
    }
    
    def __str__(self):
        return f"{self.codigo}: {self.nombre}"
    
    def get_objetivos_aprendizaje(self):
        """Retorna los OA completos asociados a esta unidad"""
        return ObjetivoAprendizaje.objects(codigo__in=self.oa_codigos)
    
    def get_objetivos_transversales(self):
        """Retorna los OAT completos asociados a esta unidad"""
        return ObjetivoTransversal.objects(codigo__in=self.oat_codigos)
    
    def get_habilidades(self):
        """Retorna las habilidades completas asociadas a esta unidad"""
        return Habilidad.objects(codigo__in=self.habilidades_codigos)
    
    def get_actitudes(self):
        """Retorna las actitudes completas asociadas a esta unidad"""
        return Actitud.objects(codigo__in=self.actitudes_codigos)


# Códigos de asignaturas para la nomenclatura
ASIGNATURAS_CODIGO = {
    'Lenguaje y Comunicación': 'Lyc',
    'Lengua y Literatura': 'Lyl',
    'Matemática': 'Mat',
    'Ciencias Naturales': 'Cna',
    'Historia, Geografía y Ciencias Sociales': 'His',
    'Inglés': 'Ing',
    'Educación Física y Salud': 'Efs',
    'Artes Visuales': 'Arv',
    'Música': 'Mus',
    'Tecnología': 'Tec',
    'Orientación': 'Ori',
    'Religión': 'Rel',
    'Filosofía': 'Fil',
    'Biología': 'Bio',
    'Física': 'Fis',
    'Química': 'Qui',
    'Educación Ciudadana': 'Edc',
}

# Códigos de niveles para la nomenclatura
NIVELES_CODIGO = {
    '1° Básico': '1b',
    '2° Básico': '2b',
    '3° Básico': '3b',
    '4° Básico': '4b',
    '5° Básico': '5b',
    '6° Básico': '6b',
    '7° Básico': '7b',
    '8° Básico': '8b',
    'I° Medio': '1m',
    'II° Medio': '2m',
    'III° Medio': '3m',
    'IV° Medio': '4m',
}
