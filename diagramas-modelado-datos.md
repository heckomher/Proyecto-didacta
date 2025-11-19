# Diagramas de Modelado de Datos - Proyecto Didacta

## 1. Base de Datos SQL (MySQL/PostgreSQL) - Entidades Relacionales

```mermaid
erDiagram
    %% Entidades principales del sistema
    
    USER {
        int id PK "Auto-incremento"
        string username UK "Nombre de usuario único"
        string email UK "Email único"
        string password "Hash de contraseña"
        string first_name "Nombre"
        string last_name "Apellido"
        enum role "DOCENTE, UTP"
        boolean is_active "Usuario activo"
        boolean is_staff "Es staff"
        boolean is_superuser "Es superusuario"
        datetime date_joined "Fecha de registro"
        datetime last_login "Último login"
    }
    
    ANIO_ACADEMICO {
        int id PK "Auto-incremento"
        string nombre UK "Ej: 2025"
        date fecha_inicio "Fecha inicio año"
        date fecha_fin "Fecha fin año"
        enum estado "BORRADOR, ACTIVO, CERRADO"
        boolean activo "Campo legacy derivado"
        boolean cerrado "Campo legacy derivado"
        enum tipo_periodo "SEMESTRE, TRIMESTRE, ANUAL"
        datetime created_at "Fecha creación"
        datetime updated_at "Fecha actualización"
    }
    
    PLANIFICACION {
        int id PK "Auto-incremento"
        int autor_id FK "Usuario que crea"
        int anio_academico_id FK "Año académico obligatorio"
        enum estado "BORRADOR, PENDIENTE, APROBADA, RECHAZADA"
        datetime fecha_creacion "Auto-generada"
        date fecha_inicio "Fecha inicio planificación"
        date fecha_fin "Fecha fin planificación"
        enum tipo "CURSO, TALLER, SEMINARIO"
        string titulo "Título planificación"
        text comentarios_validacion "Comentarios UTP"
    }
    
    PERIODO_ACADEMICO {
        int id PK "Auto-incremento"
        int anio_academico_id FK "Año académico padre"
        string nombre "Ej: Primer Semestre"
        int numero "1, 2, 3..."
        date fecha_inicio "Inicio del período"
        date fecha_fin "Fin del período"
    }
    
    FERIADO {
        int id PK "Auto-incremento"
        string nombre "Nombre del feriado"
        date fecha "Fecha del feriado"
        int anio_academico_id FK "Año académico (opcional)"
        enum tipo "FERIADO, INSTITUCIONAL, RECESO"
    }
    
    PERIODO_VACACIONES {
        int id PK "Auto-incremento"
        string nombre "Ej: Vacaciones de Invierno"
        date fecha_inicio "Inicio vacaciones"
        date fecha_fin "Fin vacaciones"
        int anio_academico_id FK "Año académico padre"
        enum tipo "INVIERNO, VERANO, RECESO"
    }
    
    %% Relaciones con cardinalidad
    USER ||--o{ PLANIFICACION : "crea"
    ANIO_ACADEMICO ||--o{ PLANIFICACION : "contiene"
    ANIO_ACADEMICO ||--o{ PERIODO_ACADEMICO : "tiene_periodos"
    ANIO_ACADEMICO ||--o{ FERIADO : "define_feriados"
    ANIO_ACADEMICO ||--o{ PERIODO_VACACIONES : "define_vacaciones"
    
    %% Estilos para diferentes tipos de entidades
    classDef userEntity fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef planEntity fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px  
    classDef configEntity fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef timeEntity fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    
    class USER userEntity
    class PLANIFICACION planEntity
    class ANIO_ACADEMICO configEntity
    class PERIODO_ACADEMICO,FERIADO,PERIODO_VACACIONES timeEntity
```

## 2. Base de Datos NoSQL (MongoDB) - Documentos

```mermaid
graph TB
    subgraph "📄 Colección: planificacion_detalles"
        PlanifDetalle["🗂️ PlanificacionDetalle<br/>
        {<br/>
          _id: ObjectId,<br/>
          planificacion: String (FK SQL),<br/>
          objetivos: {<br/>
            general: String,<br/>
            especificos: [String],<br/>
            competencias: [String]<br/>
          },<br/>
          actividades: {<br/>
            semana_1: {<br/>
              contenidos: [String],<br/>
              metodologia: String,<br/>
              recursos: [String],<br/>
              evaluacion: String<br/>
            },<br/>
            semana_2: {...},<br/>
            ...<br/>
          },<br/>
          recursos: {<br/>
            tecnologicos: [String],<br/>
            bibliograficos: [String],<br/>
            materiales: [String],<br/>
            espacios: [String]<br/>
          },<br/>
          created_at: Date,<br/>
          updated_at: Date<br/>
        }"]
    end
    
    subgraph "📄 Colección: eventos"
        Evento["🗓️ Evento<br/>
        {<br/>
          _id: ObjectId,<br/>
          titulo: String (required),<br/>
          descripcion: String,<br/>
          fecha_inicio: Date (required),<br/>
          fecha_fin: Date (required),<br/>
          creado_por: String (username),<br/>
          tipo: String,<br/>
          ubicacion: String,<br/>
          participantes: [String],<br/>
          estado: String,<br/>
          metadata: {<br/>
            color: String,<br/>
            icono: String,<br/>
            categoria: String<br/>
          }<br/>
        }"]
    end
    
    subgraph "📄 Colección: calendarios"
        Calendario["📅 Calendario<br/>
        {<br/>
          _id: ObjectId,<br/>
          nombre: String (required),<br/>
          descripcion: String,<br/>
          eventos: [ObjectId] (ref eventos),<br/>
          planificaciones_aprobadas: [String] (IDs SQL),<br/>
          configuracion: {<br/>
            vista_defecto: String,<br/>
            colores_tema: {},<br/>
            filtros_activos: [String]<br/>
          },<br/>
          propietario: String (username),<br/>
          compartido_con: [String],<br/>
          activo: Boolean,<br/>
          created_at: Date,<br/>
          updated_at: Date<br/>
        }"]
    end
    
    subgraph "📄 Colección: notificaciones"
        Notificacion["🔔 Notificacion<br/>
        {<br/>
          _id: ObjectId,<br/>
          destinatario: String (username),<br/>
          remitente: String (username),<br/>
          tipo: String,<br/>
          titulo: String,<br/>
          mensaje: String,<br/>
          datos_contexto: {<br/>
            planificacion_id: Number,<br/>
            evento_id: ObjectId,<br/>
            accion: String,<br/>
            url_accion: String<br/>
          },<br/>
          leida: Boolean,<br/>
          fecha_envio: Date,<br/>
          fecha_lectura: Date<br/>
        }"]
    end
    
    subgraph "📄 Colección: configuracion_sistema"
        Config["⚙️ ConfiguracionSistema<br/>
        {<br/>
          _id: ObjectId,<br/>
          clave: String (unique),<br/>
          valor: Mixed,<br/>
          tipo: String,<br/>
          descripcion: String,<br/>
          categoria: String,<br/>
          activo: Boolean,<br/>
          created_at: Date,<br/>
          updated_at: Date<br/>
        }"]
    end
    
    %% Referencias entre documentos
    PlanifDetalle -.->|"planificacion (String ID)"| SQLPlanif["🗃️ SQL: Planificacion.id"]
    Calendario -.->|"eventos (ObjectId[])"| Evento
    Calendario -.->|"planificaciones_aprobadas (String[])"| SQLPlanif
    
    %% Estilos para documentos NoSQL
    classDef documentEntity fill:#fff3e0,stroke:#f57c00,stroke-width:3px,color:#000
    classDef referenceEntity fill:#e8eaf6,stroke:#3f51b5,stroke-width:2px,color:#000
    classDef sqlReference fill:#ffebee,stroke:#e91e63,stroke-width:2px,color:#000
    
    class PlanifDetalle,Evento,Calendario,Notificacion,Config documentEntity
    class SQLPlanif sqlReference
```

## 3. Modelo Híbrido - Relación entre SQL y NoSQL

```mermaid
graph LR
    subgraph "🗃️ Base de Datos SQL (MySQL)"
        subgraph "Entidades Principales"
            U[User<br/>id, username, role]
            A[AnioAcademico<br/>id, nombre, estado]
            P[Planificacion<br/>id, autor_id, estado]
        end
        
        subgraph "Configuración Temporal"
            PA[PeriodoAcademico]
            F[Feriado] 
            PV[PeriodoVacaciones]
        end
        
        U -->|1:N| P
        A -->|1:N| P
        A -->|1:N| PA
        A -->|1:N| F
        A -->|1:N| PV
    end
    
    subgraph "📄 Base de Datos NoSQL (MongoDB)"
        subgraph "Documentos Flexibles"
            PD[PlanificacionDetalle<br/>objetivos, actividades]
            E[Evento<br/>titulo, fechas]
            C[Calendario<br/>eventos, planificaciones]
        end
        
        subgraph "Sistema de Soporte"
            N[Notificacion<br/>mensajes, alertas]
            CFG[ConfiguracionSistema<br/>configuraciones globales]
        end
    end
    
    %% Enlaces híbridos SQL ↔ NoSQL
    P -.->|"ID como String"| PD
    P -.->|"IDs en Array"| C
    E -.->|"ObjectId en Array"| C
    U -.->|"username como String"| N
    
    %% Estilos para el modelo híbrido
    classDef sqlEntity fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef nosqlEntity fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef hybridLink stroke:#e91e63,stroke-width:3px,stroke-dasharray: 5 5
    
    class U,A,P,PA,F,PV sqlEntity
    class PD,E,C,N,CFG nosqlEntity
```

## Descripción del Modelo de Datos

### **🗃️ SQL (Relacional) - Estructura y Transacciones**
- **Entidades normalizadas** con integridad referencial
- **Transacciones ACID** para operaciones críticas
- **Consultas complejas** con JOINs para reportes
- **Validaciones estrictas** de estado y permisos

### **📄 NoSQL (Documentos) - Flexibilidad y Escalabilidad**
- **Documentos JSON** para datos variables y anidados
- **Esquemas flexibles** para contenido educativo
- **Consultas rápidas** por índices en MongoDB
- **Escalabilidad horizontal** para grandes volúmenes

### **🔗 Arquitectura Híbrida**
- **SQL**: Datos estructurados, usuarios, planificaciones básicas
- **NoSQL**: Contenido detallado, eventos, configuraciones
- **Referencias cruzadas** mediante IDs y usernames
- **Consistencia eventual** entre ambas bases