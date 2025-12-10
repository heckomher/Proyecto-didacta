import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuth } from '../hooks/useAuth';
import apiClient from '../services/api';

const NuevaPlanificacion = () => {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const { user } = useAuth();

    // Determinar tipo inicial desde URL params
    const tipoInicial = searchParams.get('tipo') || '';

    const [step, setStep] = useState(tipoInicial ? 2 : 1); // Si viene con tipo, saltar al step 2
    const [tipo, setTipo] = useState(tipoInicial);
    const [loading, setLoading] = useState(false);
    const [misCursos, setMisCursos] = useState([]);
    const [planificacionesAnuales, setPlanificacionesAnuales] = useState([]);
    const [planificacionesUnidad, setPlanificacionesUnidad] = useState([]);

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
        planificacion_anual: '',
        semanas_duracion: 4,
        numero_semana: 1,
        planificacion_unidad: '',
        horas_academicas: 45
    });

    // Cargar datos iniciales
    useEffect(() => {
        const cargarDatos = async () => {
            try {
                const [cursosRes, anualesRes, unidadesRes] = await Promise.all([
                    apiClient.get('/docentes/mis-cursos/'),
                    apiClient.get('/planificaciones-anuales/'),
                    apiClient.get('/planificaciones-unidad/')
                ]);
                setMisCursos(cursosRes.data);
                setPlanificacionesAnuales(anualesRes.data);
                setPlanificacionesUnidad(unidadesRes.data);
            } catch (error) {
                console.error('Error cargando datos:', error);
            }
        };
        cargarDatos();
    }, []);

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
            const payload = {
                titulo: formData.titulo,
                descripcion: formData.descripcion,
                curso: parseInt(formData.curso),
                asignatura: parseInt(formData.asignatura),
                fecha_inicio: formData.fecha_inicio,
                fecha_fin: formData.fecha_fin,
                estado: 'BORRADOR'
            };

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

            await apiClient.post(endpoints[tipo], payload);
            toast.success('Planificación creada exitosamente');
            navigate('/');
        } catch (error) {
            console.error('Error creando planificación:', error);
            toast.error('Error al crear planificación: ' + (error.response?.data?.detail || JSON.stringify(error.response?.data) || error.message));
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
                    Nueva Planificación
                </h1>

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

                            {/* Curso y Asignatura */}
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
                                            Vincular a Planificación Anual (opcional)
                                        </label>
                                        <select
                                            value={formData.planificacion_anual}
                                            onChange={(e) => setFormData({ ...formData, planificacion_anual: e.target.value })}
                                            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                                        >
                                            <option value="">Sin vincular</option>
                                            {planificacionesAnuales.map(p => (
                                                <option key={p.id} value={p.id}>
                                                    {p.titulo} ({p.curso_info?.nombre_curso})
                                                </option>
                                            ))}
                                        </select>
                                    </div>
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
