# Diagrama BPMN - Sistema de Planificaciones Académicas Didacta

```mermaid
graph TB
    %% Pool Principal del Sistema
    subgraph "Sistema Didacta - Gestión de Planificaciones Académicas"
        
        %% Lane Docente
        subgraph "Lane Docente" 
            A[("Inicio Sesión<br/>Docente")] --> B["Autenticarse"]
            B --> C{"¿Credenciales<br/>Válidas?"}
            C -->|No| D[("Error<br/>Autenticación")]
            D --> B
            C -->|Sí| E["Acceder Dashboard<br/>Docente"]
            
            E --> F{"¿Hay Año<br/>Académico Activo?"}
            F -->|No| G[("Esperar Configuración<br/>UTP")]
            F -->|Sí| H["Ver Mis<br/>Planificaciones"]
            
            H --> I{"¿Crear Nueva<br/>Planificación?"}
            I -->|Sí| J["Completar Formulario<br/>Planificación"]
            I -->|No| K{"¿Gestionar<br/>Existente?"}
            
            J --> L["Guardar como<br/>BORRADOR"]
            L --> M[("Planificación<br/>Creada")]
            M --> H
            
            K -->|Editar| N["Modificar<br/>Planificación"]
            K -->|Enviar| O{"¿Estado =<br/>BORRADOR?"}
            K -->|Eliminar| P["Eliminar<br/>Planificación"]
            
            N --> Q["Guardar<br/>Cambios"]
            Q --> H
            
            O -->|No| R[("No se puede<br/>Enviar")]
            O -->|Sí| S["Enviar a<br/>Validación UTP"]
            S --> T["Estado =<br/>PENDIENTE"]
            T --> U[("Notificación<br/>Enviada")]
            
            P --> V[("Planificación<br/>Eliminada")]
            V --> H
            R --> H
        end
        
        %% Lane UTP
        subgraph "Lane UTP"
            AA[("Inicio Sesión<br/>UTP")] --> BB["Autenticarse<br/>como UTP"]
            BB --> CC{"¿Credenciales<br/>Válidas?"}
            CC -->|No| DD[("Error<br/>Autenticación")]
            DD --> BB
            CC -->|Sí| EE["Acceder Dashboard<br/>UTP"]
            
            EE --> FF{"¿Configurar Año<br/>Académico?"}
            FF -->|Sí| GG["Crear/Gestionar<br/>Año Académico"]
            FF -->|No| HH{"¿Validar<br/>Planificaciones?"}
            
            GG --> II["Configurar<br/>Períodos"]
            II --> JJ["Configurar<br/>Feriados/Vacaciones"]
            JJ --> KK["Activar<br/>Año Académico"]
            KK --> LL[("Año Académico<br/>Configurado")]
            
            HH -->|Sí| MM["Ver Planificaciones<br/>PENDIENTES"]
            HH -->|No| NN{"¿Ver Reportes?"}
            
            MM --> OO{"¿Hay<br/>Pendientes?"}
            OO -->|No| PP[("Sin Planificaciones<br/>por Validar")]
            OO -->|Sí| QQ["Revisar<br/>Planificación"]
            
            QQ --> RR{"¿Decisión<br/>Validación?"}
            RR -->|Aprobar| SS["Agregar Comentarios<br/>Aprobación"]
            RR -->|Rechazar| TT["Agregar Comentarios<br/>Rechazo"]
            RR -->|Revisar más| QQ
            
            SS --> UU["Estado =<br/>APROBADA"]
            UU --> VV[("Notificar<br/>Docente")]
            VV --> MM
            
            TT --> WW["Estado =<br/>RECHAZADA"]
            WW --> XX[("Notificar<br/>Docente")]
            XX --> MM
            
            NN -->|Sí| YY["Ver Planificaciones<br/>Aprobadas/Rechazadas"]
            NN -->|No| ZZ{"¿Gestionar<br/>Años?"}
            
            ZZ -->|Sí| AAA["Gestionar Años<br/>Académicos"]
            AAA --> BBB{"¿Acción?"}
            BBB -->|Activar| CCC["Activar Año<br/>BORRADOR"]
            BBB -->|Cerrar| DDD["Cerrar Año<br/>ACTIVO"]
            BBB -->|Ver| EEE["Consultar<br/>Estados"]
            
            CCC --> FFF[("Año<br/>Activado")]
            DDD --> GGG["Confirmar con<br/>Contraseña"]
            GGG --> HHH{"¿Contraseña<br/>Correcta?"}
            HHH -->|No| III[("Error<br/>Contraseña")]
            HHH -->|Sí| JJJ["Estado =<br/>CERRADO"]
            JJJ --> KKK[("Año<br/>Cerrado")]
            
            III --> GGG
        end
        
        %% Lane Sistema
        subgraph "Lane Sistema"
            SYS1[("Validación<br/>Continua Tokens")] --> SYS2{"¿Token<br/>Válido?"}
            SYS2 -->|No| SYS3["Refresh<br/>Token"]
            SYS2 -->|Sí| SYS4[("Acceso<br/>Permitido")]
            SYS3 --> SYS5{"¿Refresh<br/>Exitoso?"}
            SYS5 -->|No| SYS6[("Logout<br/>Forzado")]
            SYS5 -->|Sí| SYS4
            
            SYS7[("Validación<br/>Reglas Negocio")] --> SYS8{"¿Año Académico<br/>Cerrado?"}
            SYS8 -->|Sí| SYS9[("Bloquear<br/>Modificaciones")]
            SYS8 -->|No| SYS10[("Permitir<br/>Operaciones")]
        end
        
        %% Lane Calendario
        subgraph "Lane Calendario"
            CAL1[("Generar<br/>Calendario")] --> CAL2["Obtener Planificaciones<br/>APROBADAS"]
            CAL2 --> CAL3["Integrar<br/>Feriados"]
            CAL3 --> CAL4["Integrar<br/>Vacaciones"]
            CAL4 --> CAL5["Mostrar<br/>Vista Calendario"]
            CAL5 --> CAL6[("Calendario<br/>Actualizado")]
        end
    end
    
    %% Pool Externo - Notificaciones
    subgraph "Sistema de Notificaciones"
        NOT1[("Evento<br/>Planificación")] --> NOT2["Generar<br/>Notificación"]
        NOT2 --> NOT3["Enviar a<br/>Usuario Destino"]
        NOT3 --> NOT4[("Notificación<br/>Enviada")]
    end
    
    %% Eventos de Mensaje entre Lanes
    U -.->|Mensaje| NOT1
    VV -.->|Mensaje| NOT1
    XX -.->|Mensaje| NOT1
    LL -.->|Mensaje| G
    
    %% Eventos de Timer
    SYS1 -.->|Timer| SYS2
    CAL1 -.->|Timer| CAL2
    
    %% Estilos BPMN
    classDef startEvent fill:#c8e6c9,stroke:#4caf50,stroke-width:3px
    classDef endEvent fill:#ffcdd2,stroke:#f44336,stroke-width:3px
    classDef task fill:#e3f2fd,stroke:#2196f3,stroke-width:2px
    classDef gateway fill:#fff3e0,stroke:#ff9800,stroke-width:2px
    classDef subprocess fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px
    classDef message fill:#e0f2f1,stroke:#009688,stroke-width:2px
    
    class A,AA,SYS1,SYS7,CAL1,NOT1 startEvent
    class M,U,V,LL,PP,FFF,KKK,SYS6,SYS4,SYS9,SYS10,CAL6,NOT4 endEvent
    class B,E,H,J,L,N,Q,S,T,P,GG,II,JJ,KK,MM,QQ,SS,UU,TT,WW,YY,AAA,CCC,DDD,GGG,JJJ,SYS3,CAL2,CAL3,CAL4,CAL5,NOT2,NOT3 task
    class C,F,I,K,O,CC,FF,HH,OO,RR,NN,ZZ,BBB,HHH,SYS2,SYS5,SYS8 gateway
    class EEE subprocess
```

## Descripción del Proceso BPMN

### **Pool Principal: Sistema Didacta**

#### **Lane Docente:**
- **Proceso de Autenticación y Acceso**
- **Gestión de Planificaciones** (Crear, Editar, Eliminar, Enviar)
- **Estados:** BORRADOR → PENDIENTE

#### **Lane UTP:**
- **Configuración de Años Académicos**
- **Validación de Planificaciones**
- **Gestión de Estados:** BORRADOR → ACTIVO → CERRADO
- **Aprobación/Rechazo:** PENDIENTE → APROBADA/RECHAZADA

#### **Lane Sistema:**
- **Validación Continua de Tokens**
- **Aplicación de Reglas de Negocio**
- **Control de Acceso por Estados**

#### **Lane Calendario:**
- **Generación Automática del Calendario**
- **Integración de Eventos Aprobados**
- **Visualización Consolidada**

### **Pool Externo: Sistema de Notificaciones**
- **Gestión de Mensajes entre Usuarios**
- **Notificaciones de Cambios de Estado**

### **Elementos BPMN Utilizados:**
- 🟢 **Eventos de Inicio** (círculos verdes)
- 🔴 **Eventos de Fin** (círculos rojos)
- 🔷 **Tareas** (rectángulos azules)
- 🔶 **Gateways de Decisión** (diamantes naranjas)
- 💜 **Subprocesos** (rectángulos morados)
- ⚡ **Eventos de Mensaje** (líneas punteadas)
- ⏱️ **Eventos de Timer** (activación automática)