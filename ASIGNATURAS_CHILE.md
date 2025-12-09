# Sistema de Asignaturas del Currículum Chileno

## Implementación completada ✓

Se ha implementado un sistema completo de asignaturas basado en el currículum nacional chileno del Ministerio de Educación.

## Asignaturas Disponibles

### Educación Parvularia (3 ámbitos)
- Ámbito: Desarrollo Personal y Social
- Ámbito: Comunicación Integral
- Ámbito: Interacción y Comprensión del Entorno

### Educación Básica (11 asignaturas obligatorias)
**Asignaturas Obligatorias (1° a 8° básico):**
- Lengua y Literatura
- Matemática
- Historia, Geografía y Ciencias Sociales
- Ciencias Naturales
- Inglés
- Educación Física y Salud
- Artes Visuales
- Música
- Tecnología
- Orientación
- Religión (optativa)

### Educación Media (48 asignaturas)

**Plan Común (1° y 2° medio):**
- Lengua y Literatura
- Matemática
- Historia, Geografía y Ciencias Sociales
- Inglés
- Educación Física y Salud
- Ciencias Naturales: Biología
- Ciencias Naturales: Química
- Ciencias Naturales: Física
- Artes: Artes Visuales
- Artes: Música
- Tecnología
- Orientación
- Religión

**3° y 4° medio - Plan Común Diferenciado:**
- Educación Ciudadana
- Filosofía
- Ciencias para la Ciudadanía

**Electivos de Profundización (3° y 4° medio):**

*Matemática:*
- Límites, Derivadas e Integrales
- Probabilidades y Estadística Descriptiva e Inferencial
- Geometría 3D

*Historia y Ciencias Sociales:*
- Participación y Argumentación en Democracia
- Comprensión Histórica del Presente
- Economía y Sociedad
- Geografía, Territorio y Desafíos Socioambientales

*Ciencias Naturales:*
- Biología Celular y Molecular
- Ciencias de la Salud
- Biología de los Ecosistemas
- Química
- Física

*Educación Física:*
- Ciencias del Ejercicio Físico y Deportivo

*Artes:*
- Interpretación y Creación en Danza
- Creación y Composición Musical
- Interpretación Musical
- Artes Visuales, Audiovisuales y Multimediales
- Diseño y Arquitectura

*Lenguaje:*
- Participación y Argumentación en Democracia (profundización)
- Lectura y Escritura Especializadas
- Literatura e Identidad
- Inglés

**Técnico-Profesional:**
- Módulo Técnico Profesional 1
- Módulo Técnico Profesional 2
- Módulo Técnico Profesional 3
- Módulo Técnico Profesional 4

### Educación de Adultos (7 asignaturas)
- Lengua Castellana y Comunicación
- Matemática
- Estudios Sociales
- Ciencias Naturales
- Inglés
- Consumo y Calidad de Vida
- Convivencia Social

## Uso del Sistema

### 1. Poblar la Base de Datos
```bash
docker-compose exec backend python manage.py populate_asignaturas_chile
```

### 2. API Endpoints

**Listar todas las asignaturas:**
```
GET /api/asignaturas/
```

**Obtener asignaturas sugeridas por nivel educativo:**
```
GET /api/asignaturas/sugeridas-por-nivel/{nivel_nombre}/
```

Ejemplos:
- `/api/asignaturas/sugeridas-por-nivel/Educación Básica/`
- `/api/asignaturas/sugeridas-por-nivel/1° Medio/`
- `/api/asignaturas/sugeridas-por-nivel/Educación Parvularia/`

### 3. Asignar Asignaturas a un Curso

Al crear o editar un curso, puedes:
1. Ver las asignaturas sugeridas según el nivel educativo
2. Seleccionar las asignaturas que aplicarán para ese curso
3. El sistema automáticamente filtra las asignaturas relevantes

## Características

✓ **63 asignaturas totales** del currículum chileno
✓ Organizadas por nivel educativo
✓ Sistema de sugerencias automáticas según nivel
✓ Compatible con el plan de estudios 2020-2024
✓ Incluye asignaturas electivas de 3° y 4° medio
✓ Contempla modalidad técnico-profesional
✓ Base de datos persistente

## Próximos Pasos

Para usar este sistema en el frontend:
1. Al crear un curso, seleccionar el nivel educativo
2. El sistema sugerirá automáticamente las asignaturas correspondientes
3. El usuario puede seleccionar cuáles aplicarán para ese curso específico
4. Las planificaciones se crearán en base a las asignaturas asignadas
