# Protocolos de Prueba - Sistema Didacta

## CU-01: Autenticación e Inicio de Sesión

### TC-01.1: Login exitoso con credenciales válidas
| Campo | Valor |
|-------|-------|
| **Precondición** | Usuario registrado existe en el sistema |
| **Pasos** | 1. Navegar a /login<br>2. Ingresar username válido<br>3. Ingresar password válido<br>4. Click "Iniciar Sesión" |
| **Resultado Esperado** | Redirección a dashboard, token JWT almacenado |
| **Datos de Prueba** | Usuario: admin / Password: admin123 |

### TC-01.2: Login fallido con credenciales inválidas
| Campo | Valor |
|-------|-------|
| **Precondición** | N/A |
| **Pasos** | 1. Navegar a /login<br>2. Ingresar username inválido<br>3. Ingresar password inválido<br>4. Click "Iniciar Sesión" |
| **Resultado Esperado** | Error "Credenciales inválidas", sin redirección |
| **Datos de Prueba** | Usuario: test_invalido / Password: wrong123 |

### TC-01.3: Login con campos vacíos
| Campo | Valor |
|-------|-------|
| **Precondición** | N/A |
| **Pasos** | 1. Navegar a /login<br>2. Dejar campos vacíos<br>3. Click "Iniciar Sesión" |
| **Resultado Esperado** | Validación de campos requeridos |

### TC-01.4: Persistencia de sesión (token refresh)
| Campo | Valor |
|-------|-------|
| **Precondición** | Usuario autenticado |
| **Pasos** | 1. Login exitoso<br>2. Esperar 4+ minutos<br>3. Realizar acción en el sistema |
| **Resultado Esperado** | Token renovado automáticamente |

---

## CU-02: Registro y Gestión de Usuarios

### TC-02.1: Registro de nuevo usuario por UTP
| Campo | Valor |
|-------|-------|
| **Precondición** | Usuario UTP autenticado |
| **Pasos** | 1. Ir a Gestión de Usuarios<br>2. Click "Nuevo Usuario"<br>3. Completar formulario<br>4. Guardar |
| **Resultado Esperado** | Usuario creado, aparece en lista |
| **Datos de Prueba** | Rol: DOCENTE, Nombre: Test User |

### TC-02.2: Bloqueo de registro por usuario sin permisos
| Campo | Valor |
|-------|-------|
| **Precondición** | Usuario DOCENTE autenticado |
| **Pasos** | 1. Intentar acceder a /register o API /auth/register/ |
| **Resultado Esperado** | Error 403 Forbidden |

### TC-02.3: Edición de perfil de usuario
| Campo | Valor |
|-------|-------|
| **Precondición** | Usuario UTP autenticado |
| **Pasos** | 1. Ir a Gestión de Usuarios<br>2. Seleccionar usuario<br>3. Editar datos<br>4. Guardar |
| **Resultado Esperado** | Datos actualizados correctamente |

### TC-02.4: Desactivación de usuario
| Campo | Valor |
|-------|-------|
| **Precondición** | Usuario UTP autenticado |
| **Pasos** | 1. Ir a Gestión de Usuarios<br>2. Click toggle "Activo"<br>3. Verificar usuario desactivado no puede loguearse |
| **Resultado Esperado** | Usuario desactivado, no puede acceder |

---

## CU-03: Creación de Planificaciones

### TC-03.1: Crear planificación anual
| Campo | Valor |
|-------|-------|
| **Precondición** | Docente autenticado con cursos asignados |
| **Pasos** | 1. Dashboard → Nueva Planificación<br>2. Tipo: Anual<br>3. Seleccionar curso y asignatura<br>4. Completar datos<br>5. Guardar |
| **Resultado Esperado** | Planificación creada en estado BORRADOR |

### TC-03.2: Crear planificación de unidad
| Campo | Valor |
|-------|-------|
| **Precondición** | Planificación anual existente |
| **Pasos** | 1. Nueva Planificación → Unidad<br>2. Seleccionar planificación anual padre<br>3. Completar datos<br>4. Guardar |
| **Resultado Esperado** | Unidad creada, hereda curso/asignatura del padre |

### TC-03.3: Crear planificación semanal
| Campo | Valor |
|-------|-------|
| **Precondición** | Planificación de unidad existente |
| **Pasos** | 1. Nueva Planificación → Semanal<br>2. Seleccionar unidad padre<br>3. Completar datos<br>4. Guardar |
| **Resultado Esperado** | Semanal creada, NO pide curso/asignatura |

### TC-03.4: Editar planificación aprobada
| Campo | Valor |
|-------|-------|
| **Precondición** | Planificación en estado APROBADA |
| **Pasos** | 1. Dashboard → Editar planificación<br>2. Modificar datos<br>3. Guardar |
| **Resultado Esperado** | Estado cambia a BORRADOR, warning mostrado |

---

## CU-04: Validación de Planificaciones

### TC-04.1: Enviar planificación a validación
| Campo | Valor |
|-------|-------|
| **Precondición** | Planificación en BORRADOR |
| **Pasos** | 1. Dashboard → Planificación<br>2. Click "Enviar a Validación" |
| **Resultado Esperado** | Estado cambia a PENDIENTE |

### TC-04.2: UTP aprueba planificación
| Campo | Valor |
|-------|-------|
| **Precondición** | Usuario UTP, planificación PENDIENTE |
| **Pasos** | 1. Ver planificación<br>2. Click "Aprobar" |
| **Resultado Esperado** | Estado cambia a APROBADA |

### TC-04.3: UTP rechaza planificación con comentarios
| Campo | Valor |
|-------|-------|
| **Precondición** | Usuario UTP, planificación PENDIENTE |
| **Pasos** | 1. Ver planificación<br>2. Ingresar comentarios<br>3. Click "Rechazar" |
| **Resultado Esperado** | Estado BORRADOR, comentarios visibles para docente |

---

## CU-05: Gestión del Calendario

### TC-05.1: Visualización de períodos académicos
| Campo | Valor |
|-------|-------|
| **Precondición** | Año académico activo con períodos |
| **Pasos** | 1. Ir a Calendario |
| **Resultado Esperado** | Períodos visibles, feriados marcados |

### TC-05.2: Crear evento en calendario
| Campo | Valor |
|-------|-------|
| **Precondición** | Usuario autenticado |
| **Pasos** | 1. Calendario → Click en día<br>2. Completar datos<br>3. Guardar |
| **Resultado Esperado** | Evento visible en calendario |

---

## CU-06: Seguridad

### TC-06.1: Protección de rutas sin autenticación
| Campo | Valor |
|-------|-------|
| **Precondición** | Sin sesión activa |
| **Pasos** | 1. Acceder directamente a /gestionar-usuarios |
| **Resultado Esperado** | Redirección a /login |

### TC-06.2: Protección de API sin token
| Campo | Valor |
|-------|-------|
| **Precondición** | Sin token JWT |
| **Pasos** | 1. GET /api/cursos/ sin header Authorization |
| **Resultado Esperado** | 401 Unauthorized |

### TC-06.3: Control de roles (DOCENTE no puede crear usuarios)
| Campo | Valor |
|-------|-------|
| **Precondición** | Usuario DOCENTE autenticado |
| **Pasos** | 1. POST /api/auth/register/ con datos válidos |
| **Resultado Esperado** | 403 Forbidden |

### TC-06.4: Validación de inyección SQL
| Campo | Valor |
|-------|-------|
| **Precondición** | Formulario de login |
| **Pasos** | 1. Ingresar: ' OR '1'='1 como username |
| **Resultado Esperado** | Error de autenticación, sin bypass |

### TC-06.5: Protección XSS
| Campo | Valor |
|-------|-------|
| **Precondición** | Formulario con campo de texto |
| **Pasos** | 1. Ingresar: <script>alert('xss')</script> |
| **Resultado Esperado** | Texto escapado, sin ejecución de script |
