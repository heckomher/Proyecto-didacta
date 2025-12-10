import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, useParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuth } from '../hooks/useAuth';
import apiClient from '../services/api';

const NuevaPlanificacion = () => {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const { tipo: tipoEdit, id: editId } = useParams(); // Para modo edición
    const { user } = useAuth();

    // Modo edición detectado desde la ruta
    const isEditMode = Boolean(editId && tipoEdit);

    // Determinar tipo inicial desde URL params
    const tipoInicial = tipoEdit || searchParams.get('tipo') || '';
    const anualIdParam = searchParams.get('anual') || '';
    const unidadIdParam = searchParams.get('unidad') || '';

    const [step, setStep] = useState(tipoInicial ? 2 : 1); // Si viene con tipo, saltar al step 2
    const [tipo, setTipo] = useState(tipoInicial);
    const [loading, setLoading] = useState(false);
    const [loadingEdit, setLoadingEdit] = useState(isEditMode); // Loading mientras carga datos en edición
    const [originalEstado, setOriginalEstado] = useState(null); // Para mostrar warning si era aprobada
    const [misCursos, setMisCursos] = useState([]);
    const [planificacionesAnuales, setPlanificacionesAnuales] = useState([]);
    const [planificacionesUnidad, setPlanificacionesUnidad] = useState([]);
    const [anioActivo, setAnioActivo] = useState(null);
    const [periodosAcademicos, setPeriodosAcademicos] = useState([]);
    const [advertenciaFechas, setAdvertenciaFechas] = useState(null);

    // Estado para currículum
    const [unidadesCurriculares, setUnidadesCurriculares] = useState([]);
    const [unidadCurricularSeleccionada, setUnidadCurricularSeleccionada] = useState(null);
    const [loadingCurriculum, setLoadingCurriculum] = useState(false);
    const [codigosCurriculum, setCodigosCurriculum] = useState({ asignaturas: {}, niveles: {} });

    const [formData, setFormData] = useState({
        titulo: '',
        descripcion: '',
        curso: '',
        asignatura: '',
        fecha_inicio: '',
        fecha_fin: '',
        // Campos específicos por tipo
        meses_academicos: 10,
        periodos_evaluacion: 2,
        numero_unidad: 1,
        planificacion_anual: anualIdParam,
        semanas_duracion: 4,
        numero_semana: 1,
        planificacion_unidad: unidadIdParam,
        horas_academicas: 45,
        unidad_curricular_codigo: '' // Nuevo: vincular a unidad curricular MINEDUC
    });

    // Cargar datos iniciales
    useEffect(() => {
        const cargarDatos = async () => {
            try {
                const [cursosRes, anualesRes, unidadesRes, aniosRes, codigosRes, periodosRes] = await Promise.all([
                    apiClient.get('/docentes/mis-cursos/'),
                    apiClient.get('/planificaciones-anuales/'),
                    apiClient.get('/planificaciones-unidad/'),
                    apiClient.get('/anios-academicos/'),
                    apiClient.get('/curriculum/codigos/'),
                    apiClient.get('/periodos-academicos/')
                ]);
                setMisCursos(cursosRes.data);
                setPlanificacionesAnuales(anualesRes.data);
                setPlanificacionesUnidad(unidadesRes.data);
                setCodigosCurriculum(codigosRes.data);
                setPeriodosAcademicos(periodosRes.data);

                // Buscar año activo
                const activo = aniosRes.data.find(a => a.estado === 'ACTIVO');
                if (activo) {
                    setAnioActivo(activo);
                }
            } catch (error) {
                console.error('Error cargando datos:', error);
            }
        };
        cargarDatos();
    }, []);

    // Cargar datos de planificación existente en modo edición
    useEffect(() => {
        const cargarPlanificacionExistente = async () => {
            if (!isEditMode || !editId || misCursos.length === 0) return;

            try {
                setLoadingEdit(true);
                const endpoints = {
                    'anual': '/planificaciones-anuales/',
                    'unidad': '/planificaciones-unidad/',
                    'semanal': '/planificaciones-semanales/'
                };
                const endpoint = endpoints[tipoEdit];
                if (!endpoint) return;

                const res = await apiClient.get(`${endpoint}${editId}/`);
                const data = res.data;

                // Guardar estado original para mostrar warning
                setOriginalEstado(data.estado);

                // Poblar formData con datos existentes
                setFormData(prev => ({
                    ...prev,
                    titulo: data.titulo || '',
                    descripcion: data.descripcion || '',
                    curso: data.curso?.toString() || '',
                    asignatura: data.asignatura?.toString() || '',
                    fecha_inicio: data.fecha_inicio || '',
                    fecha_fin: data.fecha_fin || '',
                    meses_academicos: data.meses_academicos || 10,
                    periodos_evaluacion: data.periodos_evaluacion || 2,
                    numero_unidad: data.numero_unidad || 1,
                    planificacion_anual: data.planificacion_anual?.toString() || '',
                    semanas_duracion: data.semanas_duracion || 4,
                    numero_semana: data.numero_semana || 1,
                    planificacion_unidad: data.planificacion_unidad?.toString() || '',
                    horas_academicas: data.horas_academicas || 45,
                    unidad_curricular_codigo: data.unidad_curricular_codigo || ''
                }));
            } catch (error) {
                console.error('Error cargando planificación:', error);
                toast.error('Error al cargar la planificación');
            } finally {
                setLoadingEdit(false);
            }
        };

        cargarPlanificacionExistente();
    }, [isEditMode, editId, tipoEdit, misCursos]);

    // Auto-llenar fechas cuando se selecciona tipo anual
    useEffect(() => {
        if (tipo === 'anual' && anioActivo && !formData.fecha_inicio && !formData.fecha_fin) {
            setFormData(prev => ({
                ...prev,
                fecha_inicio: anioActivo.fecha_inicio,
                fecha_fin: anioActivo.fecha_fin
            }));
        }
    }, [tipo, anioActivo]);

    // Auto-heredar curso y asignatura de la planificación anual padre (para unidades)
    useEffect(() => {
        if (tipo !== 'unidad' || !formData.planificacion_anual) return;

        const anualPadre = planificacionesAnuales.find(p => p.id === parseInt(formData.planificacion_anual));
        if (anualPadre) {
            setFormData(prev => ({
                ...prev,
                curso: anualPadre.curso?.toString() || '',
                asignatura: anualPadre.asignatura?.toString() || ''
            }));
        }
    }, [tipo, formData.planificacion_anual, planificacionesAnuales]);

    // Función helper para obtener el próximo lunes desde una fecha
    const getNextMonday = (dateString) => {
        const date = new Date(dateString);
        const dayOfWeek = date.getUTCDay();
        const daysUntilMonday = dayOfWeek === 0 ? 1 : (8 - dayOfWeek) % 7 || 7;
        date.setUTCDate(date.getUTCDate() + daysUntilMonday);
        return date.toISOString().split('T')[0];
    };

    // Auto-sugerir fecha de inicio para planificaciones de unidad
    useEffect(() => {
        if (tipo !== 'unidad' || !formData.planificacion_anual) return;

        const anualPadre = planificacionesAnuales.find(p => p.id === parseInt(formData.planificacion_anual));
        if (!anualPadre) return;

        // Buscar unidades existentes de esta planificación anual
        const unidadesHermanas = planificacionesUnidad
            .filter(u => u.planificacion_anual === parseInt(formData.planificacion_anual))
            .sort((a, b) => new Date(a.fecha_fin || 0) - new Date(b.fecha_fin || 0));

        let fechaInicioSugerida;

        if (unidadesHermanas.length === 0) {
            // Primera unidad: usar fecha de inicio de la planificación anual
            fechaInicioSugerida = anualPadre.fecha_inicio;

            // Si la fecha de inicio no cae en lunes, buscar el próximo lunes
            const fecha = new Date(anualPadre.fecha_inicio);
            if (fecha.getUTCDay() !== 1) { // 1 = lunes
                fechaInicioSugerida = getNextMonday(anualPadre.fecha_inicio);
            }
        } else {
            // Ya existen unidades: buscar el próximo lunes después de la última unidad
            const ultimaUnidad = unidadesHermanas[unidadesHermanas.length - 1];
            if (ultimaUnidad.fecha_fin) {
                // Sumar un día a la fecha de fin de la última unidad
                const diaPostFin = new Date(ultimaUnidad.fecha_fin);
                diaPostFin.setUTCDate(diaPostFin.getUTCDate() + 1);
                fechaInicioSugerida = getNextMonday(diaPostFin.toISOString().split('T')[0]);
            }
        }

        if (fechaInicioSugerida && !formData.fecha_inicio) {
            setFormData(prev => ({
                ...prev,
                fecha_inicio: fechaInicioSugerida
            }));
        }
    }, [tipo, formData.planificacion_anual, planificacionesAnuales, planificacionesUnidad]);


    // Cargar unidades curriculares cuando cambia curso/asignatura
    useEffect(() => {
        const cargarUnidadesCurriculares = async () => {
            if (!formData.curso || !formData.asignatura || tipo !== 'unidad') return;

            const curso = misCursos.find(c => c.id === parseInt(formData.curso));
            const asignatura = getAsignaturasCurso().find(a => a.id === parseInt(formData.asignatura));

            if (!curso || !asignatura) return;

            // Normalizar nombres para comparación (quitar acentos y caracteres especiales)
            const normalizarNombre = (str) => str?.toLowerCase()
                .normalize('NFD').replace(/[\u0300-\u036f]/g, '')  // Quitar acentos
                .replace(/[°º]/g, '')  // Quitar símbolos de grado
                .replace(/\s+/g, ' ').trim();

            // Extraer el grado del nombre del curso (ej: "I° A" -> "I°", "1° Medio" -> "1°")
            const extraerGrado = (nombreCurso) => {
                // Buscar patrones como "I°", "II°", "III°", "IV°", "1°", "2°", etc.
                const match = nombreCurso?.match(/^(I{1,3}V?|IV|[1-8])°?\s*/i);
                return match ? match[1] : null;
            };

            // Construir el nivel completo combinando grado + tipo de nivel
            const grado = extraerGrado(curso.nombre_curso);
            const tipoNivel = curso.nivel_nombre?.includes('Básico') ? 'Básico' :
                curso.nivel_nombre?.includes('Media') ? 'Medio' : '';

            // Crear el nombre de nivel para búsqueda (ej: "I° Medio", "8° Básico")
            const nivelCompleto = grado && tipoNivel ? `${grado}° ${tipoNivel}` : curso.nivel_nombre;
            const nivelNormalizado = normalizarNombre(nivelCompleto);
            const asigNormalizada = normalizarNombre(asignatura.nombre);

            console.log('Buscando nivel:', nivelCompleto, '-> normalizado:', nivelNormalizado);
            console.log('Buscando asignatura:', asignatura.nombre, '-> normalizado:', asigNormalizada);

            // Convertir nivel y asignatura a códigos
            const nivelCodigo = Object.entries(codigosCurriculum.niveles || {})
                .find(([nombre]) => {
                    const nombreNorm = normalizarNombre(nombre);
                    return nivelNormalizado?.includes(nombreNorm) || nombreNorm?.includes(nivelNormalizado);
                })?.[1];
            const asigCodigo = Object.entries(codigosCurriculum.asignaturas || {})
                .find(([nombre]) => {
                    const nombreNorm = normalizarNombre(nombre);
                    return asigNormalizada?.includes(nombreNorm) || nombreNorm?.includes(asigNormalizada);
                })?.[1];

            if (!nivelCodigo || !asigCodigo) {
                console.log('No se encontró código para nivel:', nivelCompleto, '-> Código:', nivelCodigo);
                console.log('No se encontró código para asignatura:', asignatura.nombre, '-> Código:', asigCodigo);
                setUnidadesCurriculares([]);
                return;
            }

            try {
                setLoadingCurriculum(true);
                const res = await apiClient.get(`/curriculum/unidades/${nivelCodigo}/${asigCodigo}/`);
                setUnidadesCurriculares(res.data);
            } catch (error) {
                console.error('Error cargando unidades curriculares:', error);
                setUnidadesCurriculares([]);
            } finally {
                setLoadingCurriculum(false);
            }
        };

        cargarUnidadesCurriculares();
    }, [formData.curso, formData.asignatura, tipo, misCursos, codigosCurriculum]);

    // Cargar detalle de unidad curricular cuando se selecciona
    useEffect(() => {
        const cargarDetalleUnidad = async () => {
            if (!formData.unidad_curricular_codigo) {
                setUnidadCurricularSeleccionada(null);
                return;
            }

            try {
                setLoadingCurriculum(true);
                const res = await apiClient.get(`/curriculum/unidad/${formData.unidad_curricular_codigo}/`);
                setUnidadCurricularSeleccionada(res.data);

                // Auto-llenar número de unidad y semanas
                setFormData(prev => ({
                    ...prev,
                    numero_unidad: res.data.numero,
                    semanas_duracion: res.data.semanas_sugeridas,
                    titulo: prev.titulo || res.data.nombre
                }));
            } catch (error) {
                console.error('Error cargando detalle unidad:', error);
            } finally {
                setLoadingCurriculum(false);
            }
        };

        cargarDetalleUnidad();
    }, [formData.unidad_curricular_codigo]);

    // Auto-calcular fecha de fin validando contra periodos académicos
    useEffect(() => {
        if (tipo !== 'unidad' || !formData.fecha_inicio || !formData.semanas_duracion) {
            setAdvertenciaFechas(null);
            return;
        }

        const fechaInicio = new Date(formData.fecha_inicio);
        // Calcular fecha de fin ideal: inicio + semanas, terminando el viernes
        const diasDuracion = (formData.semanas_duracion * 7) - 3; // Termina el viernes
        let fechaFin = new Date(fechaInicio);
        fechaFin.setUTCDate(fechaFin.getUTCDate() + diasDuracion);

        // Ajustar para que siempre termine en viernes
        const diaSemanaFin = fechaFin.getUTCDay();
        if (diaSemanaFin !== 5) { // 5 = viernes
            const diasHastaViernes = diaSemanaFin === 0 ? -2 : (5 - diaSemanaFin);
            fechaFin.setUTCDate(fechaFin.getUTCDate() + diasHastaViernes);
        }

        // Obtener año académico de la planificación anual padre
        const anualPadre = planificacionesAnuales.find(p => p.id === parseInt(formData.planificacion_anual));
        const anioAcademicoId = anualPadre?.anio_academico;

        // Filtrar periodos del año académico correspondiente
        const periodosDelAnio = periodosAcademicos
            .filter(p => p.anio_academico === anioAcademicoId)
            .sort((a, b) => new Date(a.fecha_inicio) - new Date(b.fecha_inicio));

        if (periodosDelAnio.length > 0) {
            // Verificar si la fecha de fin calculada cae dentro de un periodo válido
            const fechaFinDate = fechaFin;
            const periodoValido = periodosDelAnio.find(p => {
                const pInicio = new Date(p.fecha_inicio);
                const pFin = new Date(p.fecha_fin);
                return fechaFinDate >= pInicio && fechaFinDate <= pFin;
            });

            if (!periodoValido) {
                // La fecha cae fuera de un periodo (vacaciones)
                // Buscar el próximo periodo después de la fecha de fin calculada
                const siguientePeriodo = periodosDelAnio.find(p => new Date(p.fecha_inicio) > fechaFinDate);

                if (siguientePeriodo) {
                    // Ajustar al primer viernes del siguiente periodo
                    const inicioPeriodo = new Date(siguientePeriodo.fecha_inicio);
                    const diaSemana = inicioPeriodo.getUTCDay();
                    const diasHastaViernes = diaSemana <= 5 ? (5 - diaSemana) : (12 - diaSemana);
                    const primerViernes = new Date(inicioPeriodo);
                    primerViernes.setUTCDate(inicioPeriodo.getUTCDate() + diasHastaViernes);

                    const fechaFinOriginal = fechaFin.toISOString().split('T')[0];
                    fechaFin = primerViernes;

                    setAdvertenciaFechas({
                        mensaje: `La fecha de término original (${fechaFinOriginal}) cae en periodo de vacaciones. Se ha ajustado al primer viernes del ${siguientePeriodo.nombre}.`,
                        tipo: 'warning'
                    });
                } else {
                    setAdvertenciaFechas({
                        mensaje: 'La fecha de término excede el año académico. Revise las semanas de duración.',
                        tipo: 'error'
                    });
                }
            } else {
                setAdvertenciaFechas(null);
            }
        }

        const fechaFinStr = fechaFin.toISOString().split('T')[0];

        // Solo actualizar si es diferente para evitar loops
        if (formData.fecha_fin !== fechaFinStr) {
            setFormData(prev => ({
                ...prev,
                fecha_fin: fechaFinStr
            }));
        }
    }, [tipo, formData.fecha_inicio, formData.semanas_duracion, formData.planificacion_anual, periodosAcademicos, planificacionesAnuales]);

    // Obtener asignaturas del curso seleccionado
    const getAsignaturasCurso = () => {
        const curso = misCursos.find(c => c.id === parseInt(formData.curso));
        return curso?.mis_asignaturas || [];
    };

    // Manejar envío
    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        const endpoints = {
            anual: '/planificaciones-anuales/',
            unidad: '/planificaciones-unidad/',
            semanal: '/planificaciones-semanales/'
        };

        try {
            // Obtener el año académico del curso seleccionado o usar el activo
            const cursoSeleccionado = misCursos.find(c => c.id === parseInt(formData.curso));
            const anioAcademicoId = cursoSeleccionado?.anio_academico || anioActivo?.id;

            if (!anioAcademicoId) {
                toast.error('No hay un año académico activo');
                setLoading(false);
                return;
            }

            const tipoMap = {
                anual: 'ANUAL',
                unidad: 'UNIDAD',
                semanal: 'SEMANAL'
            };

            const payload = {
                titulo: formData.titulo,
                descripcion: formData.descripcion,
                tipo: tipoMap[tipo],
                fecha_inicio: formData.fecha_inicio,
                fecha_fin: formData.fecha_fin
            };

            // Solo incluir curso/asignatura si es creación nueva (no edición con herencia)
            if (!isEditMode) {
                payload.curso = parseInt(formData.curso);
                payload.asignatura = parseInt(formData.asignatura);
                payload.anio_academico = anioAcademicoId;
                payload.estado = 'BORRADOR';
            }

            // Campos específicos por tipo
            if (tipo === 'anual') {
                payload.meses_academicos = formData.meses_academicos;
                payload.periodos_evaluacion = formData.periodos_evaluacion;
            } else if (tipo === 'unidad') {
                payload.numero_unidad = formData.numero_unidad;
                payload.semanas_duracion = formData.semanas_duracion;
                if (formData.planificacion_anual) {
                    payload.planificacion_anual = parseInt(formData.planificacion_anual);
                }
            } else if (tipo === 'semanal') {
                payload.numero_semana = formData.numero_semana;
                payload.horas_academicas = formData.horas_academicas;
                if (formData.planificacion_unidad) {
                    payload.planificacion_unidad = parseInt(formData.planificacion_unidad);
                }
            }

            if (isEditMode) {
                // PUT para actualizar
                await apiClient.put(`${endpoints[tipo]}${editId}/`, payload);
                toast.success('Planificación actualizada exitosamente');
            } else {
                // POST para crear
                await apiClient.post(endpoints[tipo], payload);
                toast.success('Planificación creada exitosamente');
            }
            navigate('/');
        } catch (error) {
            console.error('Error guardando planificación:', error);
            toast.error('Error al guardar planificación: ' + (error.response?.data?.detail || JSON.stringify(error.response?.data) || error.message));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="mb-6">
                <button
                    onClick={() => navigate('/')}
                    className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 inline-flex items-center"
                >
                    <svg className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                    </svg>
                    Volver al Dashboard
                </button>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                    {isEditMode ? 'Editar Planificación' : 'Nueva Planificación'}
                </h1>

                {/* Warning cuando se edita una planificación aprobada/pendiente */}
                {isEditMode && originalEstado && ['APROBADA', 'PENDIENTE'].includes(originalEstado) && (
                    <div className="mb-6 p-4 bg-yellow-50 dark:bg-yellow-900/30 border border-yellow-200 dark:border-yellow-700 rounded-lg">
                        <div className="flex items-start">
                            <svg className="h-5 w-5 text-yellow-500 mr-3 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                            </svg>
                            <div>
                                <h4 className="font-medium text-yellow-800 dark:text-yellow-200">
                                    Esta planificación está {originalEstado === 'APROBADA' ? 'aprobada' : 'pendiente de aprobación'}
                                </h4>
                                <p className="text-sm text-yellow-700 dark:text-yellow-300 mt-1">
                                    Al guardar cambios, la planificación volverá a estado <strong>Borrador</strong> y deberá ser revisada nuevamente por UTP.
                                </p>
                            </div>
                        </div>
                    </div>
                )}

                {/* Loading mientras carga datos en edición */}
                {loadingEdit && (
                    <div className="flex items-center justify-center py-8">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
                        <span className="ml-3 text-gray-600 dark:text-gray-400">Cargando planificación...</span>
                    </div>
                )}

                {/* Step 1: Seleccionar Tipo */}
                {step === 1 && (
                    <div>
                        <h2 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
                            ¿Qué tipo de planificación deseas crear?
                        </h2>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            {[
                                { id: 'anual', label: 'Planificación Anual', icon: '📅', desc: 'Planificación para todo el año académico' },
                                { id: 'unidad', label: 'Planificación por Unidad', icon: '📚', desc: 'Planificación de una unidad específica' },
                                { id: 'semanal', label: 'Planificación Semanal', icon: '📋', desc: 'Planificación detallada por semana' },
                            ].map(t => (
                                <button
                                    key={t.id}
                                    onClick={() => { setTipo(t.id); setStep(2); }}
                                    className="p-4 border-2 border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary-500 dark:hover:border-primary-500 transition-colors text-left"
                                >
                                    <span className="text-3xl mb-2 block">{t.icon}</span>
                                    <h3 className="font-medium text-gray-900 dark:text-white">{t.label}</h3>
                                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{t.desc}</p>
                                </button>
                            ))}
                        </div>
                    </div>
                )}

                {/* Step 2: Formulario */}
                {step === 2 && (
                    <form onSubmit={handleSubmit}>
                        <div className="mb-4">
                            <button
                                type="button"
                                onClick={() => { setStep(1); setTipo(''); }}
                                className="text-sm text-primary-600 dark:text-primary-400 hover:underline"
                            >
                                ← Cambiar tipo de planificación
                            </button>
                            <span className="ml-2 px-2 py-1 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded text-sm">
                                {tipo === 'anual' ? 'Anual' : tipo === 'unidad' ? 'Por Unidad' : 'Semanal'}
                            </span>
                        </div>

                        <div className="space-y-4">
                            {/* Título */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                    Título de la Planificación *
                                </label>
                                <input
                                    type="text"
                                    required
                                    value={formData.titulo}
                                    onChange={(e) => setFormData({ ...formData, titulo: e.target.value })}
                                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                                    placeholder="Ej: Matemáticas 1° Medio - Álgebra"
                                />
                            </div>

                            {/* Curso y Asignatura - solo para anual, unidad y semanal lo heredan del padre */}
                            {tipo === 'anual' && (
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                            Curso *
                                        </label>
                                        <select
                                            required
                                            value={formData.curso}
                                            onChange={(e) => setFormData({ ...formData, curso: e.target.value, asignatura: '' })}
                                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                                        >
                                            <option value="">Seleccione un curso</option>
                                            {misCursos.map(curso => (
                                                <option key={curso.id} value={curso.id}>
                                                    {curso.nombre_curso} ({curso.nivel_nombre})
                                                </option>
                                            ))}
                                        </select>
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                            Asignatura *
                                        </label>
                                        <select
                                            required
                                            value={formData.asignatura}
                                            onChange={(e) => setFormData({ ...formData, asignatura: e.target.value })}
                                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                                            disabled={!formData.curso}
                                        >
                                            <option value="">Seleccione una asignatura</option>
                                            {getAsignaturasCurso().map(asig => (
                                                <option key={asig.id} value={asig.id}>
                                                    {asig.nombre}
                                                </option>
                                            ))}
                                        </select>
                                    </div>
                                </div>
                            )}

                            {/* Fechas */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                        Fecha Inicio *
                                    </label>
                                    <input
                                        type="date"
                                        required
                                        value={formData.fecha_inicio}
                                        onChange={(e) => setFormData({ ...formData, fecha_inicio: e.target.value })}
                                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                        Fecha Fin *
                                    </label>
                                    <input
                                        type="date"
                                        required
                                        value={formData.fecha_fin}
                                        onChange={(e) => setFormData({ ...formData, fecha_fin: e.target.value })}
                                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                                    />
                                </div>
                            </div>

                            {/* Campos específicos para Anual */}
                            {tipo === 'anual' && (
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                            Meses Académicos
                                        </label>
                                        <input
                                            type="number"
                                            value={formData.meses_academicos}
                                            onChange={(e) => setFormData({ ...formData, meses_academicos: parseInt(e.target.value) })}
                                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                                            min="1" max="12"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                            Períodos de Evaluación
                                        </label>
                                        <input
                                            type="number"
                                            value={formData.periodos_evaluacion}
                                            onChange={(e) => setFormData({ ...formData, periodos_evaluacion: parseInt(e.target.value) })}
                                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                                            min="1" max="6"
                                        />
                                    </div>
                                </div>
                            )}

                            {/* Campos específicos para Unidad */}
                            {tipo === 'unidad' && (
                                <div className="space-y-4 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                                    {/* Selector de Unidad Curricular MINEDUC */}
                                    {formData.curso && formData.asignatura && (
                                        <div className="border-b border-green-200 dark:border-green-800 pb-4 mb-4">
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                                📚 Unidad del Currículum Nacional (MINEDUC)
                                            </label>
                                            {loadingCurriculum ? (
                                                <div className="text-sm text-gray-500">Cargando unidades curriculares...</div>
                                            ) : unidadesCurriculares.length > 0 ? (
                                                <select
                                                    value={formData.unidad_curricular_codigo}
                                                    onChange={(e) => setFormData({ ...formData, unidad_curricular_codigo: e.target.value })}
                                                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                                                >
                                                    <option value="">Seleccionar unidad curricular...</option>
                                                    {unidadesCurriculares.map(u => (
                                                        <option key={u.codigo} value={u.codigo}>
                                                            Unidad {u.numero}: {u.nombre} ({u.horas_sugeridas}h)
                                                            {u.priorizado_2025 ? ' ⭐' : ''}
                                                        </option>
                                                    ))}
                                                </select>
                                            ) : (
                                                <p className="text-sm text-gray-500 italic">No hay unidades curriculares disponibles para este nivel/asignatura</p>
                                            )}
                                        </div>
                                    )}

                                    {/* Preview de OAs y contenido curricular */}
                                    {unidadCurricularSeleccionada && (
                                        <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-green-200 dark:border-green-700">
                                            <h4 className="font-medium text-gray-900 dark:text-white mb-3 flex items-center">
                                                <span className="mr-2">📋</span>
                                                Contenido Curricular: {unidadCurricularSeleccionada.nombre}
                                            </h4>

                                            {/* Objetivos de Aprendizaje */}
                                            {unidadCurricularSeleccionada.objetivos_aprendizaje?.length > 0 && (
                                                <div className="mb-4">
                                                    <h5 className="text-sm font-medium text-blue-700 dark:text-blue-400 mb-2">
                                                        Objetivos de Aprendizaje ({unidadCurricularSeleccionada.objetivos_aprendizaje.length})
                                                    </h5>
                                                    <ul className="space-y-2">
                                                        {unidadCurricularSeleccionada.objetivos_aprendizaje.map(oa => (
                                                            <li key={oa.codigo} className="text-sm text-gray-700 dark:text-gray-300 border-l-2 border-blue-400 pl-3">
                                                                <span className="font-medium text-blue-600 dark:text-blue-300">{oa.codigo}</span>
                                                                <span className="text-gray-500 mx-1">|</span>
                                                                <span>{oa.descripcion.substring(0, 100)}...</span>
                                                                {oa.priorizado_2025 && (
                                                                    <span className="ml-2 px-1.5 py-0.5 text-xs bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200 rounded">
                                                                        Priorizado 2025
                                                                    </span>
                                                                )}
                                                                {/* Etiquetas de articulación */}
                                                                {oa.articulaciones_con?.length > 0 && (
                                                                    <div className="mt-1 flex flex-wrap gap-1">
                                                                        {oa.articulaciones_con.map((art, idx) => (
                                                                            <span key={idx} className="px-2 py-0.5 text-xs bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200 rounded-full">
                                                                                🔗 Articulable con {art.asignatura_nombre}
                                                                            </span>
                                                                        ))}
                                                                    </div>
                                                                )}
                                                            </li>
                                                        ))}
                                                    </ul>
                                                </div>
                                            )}

                                            {/* OAT */}
                                            {unidadCurricularSeleccionada.objetivos_transversales?.length > 0 && (
                                                <div className="mb-4">
                                                    <h5 className="text-sm font-medium text-teal-700 dark:text-teal-400 mb-2">
                                                        OAT ({unidadCurricularSeleccionada.objetivos_transversales.length})
                                                    </h5>
                                                    <div className="flex flex-wrap gap-2">
                                                        {unidadCurricularSeleccionada.objetivos_transversales.map(oat => (
                                                            <span key={oat.codigo} className="px-2 py-1 text-xs bg-teal-100 text-teal-800 dark:bg-teal-900 dark:text-teal-200 rounded" title={oat.descripcion}>
                                                                {oat.codigo}: {oat.dimension}
                                                            </span>
                                                        ))}
                                                    </div>
                                                </div>
                                            )}

                                            {/* Habilidades */}
                                            {unidadCurricularSeleccionada.habilidades?.length > 0 && (
                                                <div className="mb-4">
                                                    <h5 className="text-sm font-medium text-orange-700 dark:text-orange-400 mb-2">
                                                        Habilidades ({unidadCurricularSeleccionada.habilidades.length})
                                                    </h5>
                                                    <div className="flex flex-wrap gap-2">
                                                        {unidadCurricularSeleccionada.habilidades.map(hab => (
                                                            <span key={hab.codigo} className="px-2 py-1 text-xs bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200 rounded" title={hab.descripcion}>
                                                                {hab.codigo}
                                                            </span>
                                                        ))}
                                                    </div>
                                                </div>
                                            )}

                                            {/* Actitudes */}
                                            {unidadCurricularSeleccionada.actitudes?.length > 0 && (
                                                <div>
                                                    <h5 className="text-sm font-medium text-pink-700 dark:text-pink-400 mb-2">
                                                        Actitudes ({unidadCurricularSeleccionada.actitudes.length})
                                                    </h5>
                                                    <div className="flex flex-wrap gap-2">
                                                        {unidadCurricularSeleccionada.actitudes.map(act => (
                                                            <span key={act.codigo} className="px-2 py-1 text-xs bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-200 rounded" title={act.descripcion}>
                                                                {act.codigo}
                                                            </span>
                                                        ))}
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    )}

                                    {/* Campos de unidad */}
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                                Número de Unidad *
                                            </label>
                                            <input
                                                type="number"
                                                required
                                                value={formData.numero_unidad}
                                                onChange={(e) => setFormData({ ...formData, numero_unidad: parseInt(e.target.value) })}
                                                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                                                min="1"
                                            />
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                                Semanas de Duración
                                            </label>
                                            <input
                                                type="number"
                                                value={formData.semanas_duracion}
                                                onChange={(e) => setFormData({ ...formData, semanas_duracion: parseInt(e.target.value) })}
                                                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                                                min="1"
                                            />
                                        </div>
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                            📅 Planificación Anual *
                                        </label>
                                        <select
                                            required
                                            value={formData.planificacion_anual}
                                            onChange={(e) => setFormData({ ...formData, planificacion_anual: e.target.value })}
                                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                                        >
                                            <option value="">Seleccione planificación anual...</option>
                                            {planificacionesAnuales.map(p => (
                                                <option key={p.id} value={p.id}>
                                                    {p.titulo} ({p.curso_info?.nombre_curso})
                                                </option>
                                            ))}
                                        </select>
                                        {planificacionesAnuales.length === 0 && (
                                            <p className="mt-2 text-sm text-amber-600 dark:text-amber-400">
                                                ⚠️ No hay planificaciones anuales. <a href="/nueva-planificacion?tipo=anual" className="underline">Crear una primero</a>.
                                            </p>
                                        )}
                                    </div>

                                    {/* Advertencia de fechas */}
                                    {advertenciaFechas && (
                                        <div className={`mt-4 p-4 rounded-lg flex items-start ${advertenciaFechas.tipo === 'error'
                                            ? 'bg-red-100 dark:bg-red-900/30 border border-red-300 dark:border-red-700'
                                            : 'bg-yellow-100 dark:bg-yellow-900/30 border border-yellow-300 dark:border-yellow-700'
                                            }`}>
                                            <span className="text-xl mr-3">
                                                {advertenciaFechas.tipo === 'error' ? '❌' : '⚠️'}
                                            </span>
                                            <div>
                                                <p className={`text-sm font-medium ${advertenciaFechas.tipo === 'error'
                                                    ? 'text-red-800 dark:text-red-200'
                                                    : 'text-yellow-800 dark:text-yellow-200'
                                                    }`}>
                                                    {advertenciaFechas.tipo === 'error' ? 'Error de fechas' : 'Ajuste de fechas'}
                                                </p>
                                                <p className={`text-sm mt-1 ${advertenciaFechas.tipo === 'error'
                                                    ? 'text-red-700 dark:text-red-300'
                                                    : 'text-yellow-700 dark:text-yellow-300'
                                                    }`}>
                                                    {advertenciaFechas.mensaje}
                                                </p>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            )}

                            {/* Campos específicos para Semanal */}
                            {tipo === 'semanal' && (
                                <div className="space-y-4 p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                                Número de Semana *
                                            </label>
                                            <input
                                                type="number"
                                                required
                                                value={formData.numero_semana}
                                                onChange={(e) => setFormData({ ...formData, numero_semana: parseInt(e.target.value) })}
                                                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                                                min="1"
                                            />
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                                Horas Académicas
                                            </label>
                                            <input
                                                type="number"
                                                value={formData.horas_academicas}
                                                onChange={(e) => setFormData({ ...formData, horas_academicas: parseInt(e.target.value) })}
                                                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                                                min="1"
                                            />
                                        </div>
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                            Vincular a Unidad (opcional)
                                        </label>
                                        <select
                                            value={formData.planificacion_unidad}
                                            onChange={(e) => setFormData({ ...formData, planificacion_unidad: e.target.value })}
                                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                                        >
                                            <option value="">Sin vincular</option>
                                            {planificacionesUnidad.map(p => (
                                                <option key={p.id} value={p.id}>
                                                    Unidad {p.numero_unidad}: {p.titulo}
                                                </option>
                                            ))}
                                        </select>
                                    </div>
                                </div>
                            )}

                            {/* Descripción */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                    Descripción
                                </label>
                                <textarea
                                    value={formData.descripcion}
                                    onChange={(e) => setFormData({ ...formData, descripcion: e.target.value })}
                                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                                    rows="3"
                                    placeholder="Descripción opcional de la planificación..."
                                />
                            </div>

                            {/* Botones */}
                            <div className="flex gap-3 pt-4">
                                <button
                                    type="submit"
                                    disabled={loading}
                                    className="flex-1 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50"
                                >
                                    {loading ? 'Creando...' : 'Crear Planificación'}
                                </button>
                                <button
                                    type="button"
                                    onClick={() => navigate('/')}
                                    className="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-lg font-medium hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
                                >
                                    Cancelar
                                </button>
                            </div>
                        </div>
                    </form>
                )}
            </div>
        </div>
    );
};

export default NuevaPlanificacion;
