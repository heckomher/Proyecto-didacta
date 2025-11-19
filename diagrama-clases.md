```mermaid
classDiagram
    class Usuario {
        +idUsuario: String
        +nombre: String
        +email: String
        +login()
        +logout()
    }

    class Docente {
        +especialidad: String
        +crearPlanificacion()
        +editarPlanificacion()
        +visualizarPlanificacion()
        +reprogramarActividad()
        +registrarCumplimientoObjetivos()
    }

    class EquipoDirectivo {
        +departamento: String
        +visualizarReportes()
        +crearUsuario()
        +gestionarUsuarios()
    }

    class SistemaDidacta {
        +idSistema: String
        +nombre: String
        +sugerirPlanificacion(objetivos: List<ObjetivoAprendizaje>): Planificacion
        +gestionarCalendario(): Calendario
        +medirLogro(): ReporteLogro
    }

    class Planificacion {
        <<abstract>>
        +idPlanificacion: String
        +fechaInicio: Date
        +fechaFin: Date
        +contenido: String
        +estado: String
        +guardar()
        +actualizar()
        +eliminar()
        +obtenerDetalles()
        +enviarParaValidacion()
        +aprobar()
        +rechazar()
    }

    class PlanificacionAnual {
        +año: Integer
        +generarUnidades()
    }

    class PlanificacionUnidad {
        +nombreUnidad: String
        +numeroUnidad: Integer
        +generarSemanas()
    }

    class PlanificacionSemanal {
        +numeroSemana: Integer
        +registrarEvaluacionLogro()
    }

    class ObjetivoAprendizaje {
        +idObjetivo: String
        +descripcion: String
        +nivel: String
        +curso: String
        +agregar()
        +modificar()
        +eliminar()
    }

    class RecursoPedagogico {
        +idRecurso: String
        +nombre: String
        +tipo: String
        +agregar()
        +modificar()
        +eliminar()
    }

    class ReporteLogro {
        +idReporte: String
        +fechaGeneracion: Date
        +datosCumplimiento: Map<ObjetivoAprendizaje, Double>
        +retroalimentarSistema()
    }

    class Calendario {
        +idCalendario: String
        +reprogramarAutomaticamente()
        +comunicarCambios()
        +integrarPlanificacion()
    }

    class Evento {
        +idEvento: String
        +nombre: String
        +fecha: Date
        +curso_involucrado: String
        +hora_inicio: Time
        +hora_termino: Time
        +crear()
        +modificar()
        +eliminar()
    }

    class NivelEducativo {
        +idNivel: String
        +nombre: String
        +agregar()
        +modificar()
        +eliminar()
    }

    class Curso {
        +idCurso: String
        +nombre: String
        +agregar()
        +modificar()
        +eliminar()
    }

    Usuario <|-- Docente
    Usuario <|-- EquipoDirectivo

    Docente "1" -- "*" Planificacion : crea
    Planificacion <|-- PlanificacionAnual
    Planificacion <|-- PlanificacionUnidad
    Planificacion <|-- PlanificacionSemanal

    PlanificacionAnual "1" -- "3..8" PlanificacionUnidad : contiene
    PlanificacionUnidad "1" -- "*" PlanificacionSemanal : contiene

    Planificacion "1" -- "*" ObjetivoAprendizaje : incluye
    Planificacion "1" -- "*" RecursoPedagogico : utiliza

    Docente "1" -- "*" ReporteLogro : registra
    EquipoDirectivo "1" -- "*" ReporteLogro : visualiza
    EquipoDirectivo "1" -- "1" Calendario : gestiona

    SistemaDidacta "1" -- "*" Planificacion : sugiere
    SistemaDidacta "1" -- "1" Calendario : gestiona
    SistemaDidacta "1" -- "*" ReporteLogro : mide

    Calendario "1" -- "*" Evento : contiene

    NivelEducativo "1" -- "*" Curso : tiene
    Curso "1" -- "*" Docente : asignado
    ObjetivoAprendizaje "*" -- "1" NivelEducativo : asociado a
    ObjetivoAprendizaje "*" -- "1" Curso : asociado a

