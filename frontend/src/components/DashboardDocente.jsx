import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuth } from '../hooks/useAuth';
import apiClient from '../services/api';

const DashboardDocente = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  // Estados
  const [misCursos, setMisCursos] = useState([]);
  const [planificacionesAnuales, setPlanificacionesAnuales] = useState([]);
  const [planificacionesUnidad, setPlanificacionesUnidad] = useState([]);
  const [planificacionesSemanales, setPlanificacionesSemanales] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('anuales');
  const [expandedAnual, setExpandedAnual] = useState(null);
  const [expandedUnidad, setExpandedUnidad] = useState(null);

  // Cargar datos
  const cargarDatos = useCallback(async () => {
    try {
      const [cursosRes, anualesRes, unidadesRes, semanalesRes] = await Promise.all([
        apiClient.get('/docentes/mis-cursos/'),
        apiClient.get('/planificaciones-anuales/'),
        apiClient.get('/planificaciones-unidad/'),
        apiClient.get('/planificaciones-semanales/')
      ]);

      setMisCursos(cursosRes.data);
      setPlanificacionesAnuales(anualesRes.data);
      setPlanificacionesUnidad(unidadesRes.data);
      setPlanificacionesSemanales(semanalesRes.data);
    } catch (error) {
      console.error('Error cargando datos:', error);
      toast.error('Error al cargar datos del dashboard');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    cargarDatos();
  }, [cargarDatos]);

  // Helper para badges de estado
  const getStatusBadge = (estado) => {
    const badges = {
      BORRADOR: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
      PENDIENTE: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
      APROBADA: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
      RECHAZADA: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300',
    };
    return badges[estado] || badges.BORRADOR;
  };

  // Enviar a validación
  const handleEnviarValidacion = async (tipo, id) => {
    const endpoints = {
      anual: '/planificaciones-anuales',
      unidad: '/planificaciones-unidad',
      semanal: '/planificaciones-semanales'
    };

    try {
      await apiClient.post(`${endpoints[tipo]}/${id}/enviar-validacion/`);
      toast.success('Planificación enviada a validación');
      cargarDatos();
    } catch (error) {
      console.error('Error enviando a validación:', error);
      toast.error('Error al enviar a validación');
    }
  };

  // Obtener unidades de una planificación anual
  const getUnidadesDeAnual = (anualId) => {
    return planificacionesUnidad.filter(u => u.planificacion_anual === anualId);
  };

  // Obtener semanas de una unidad
  const getSemanasDeUnidad = (unidadId) => {
    return planificacionesSemanales.filter(s => s.planificacion_unidad === unidadId);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Cargando...</div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Dashboard Docente
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Bienvenido, {user?.nombre || user?.username}. Gestiona tus cursos y planificaciones.
        </p>
      </div>

      {/* Sección: Mis Cursos Asignados */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
          <svg className="h-6 w-6 mr-2 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
          Mis Cursos Asignados
        </h2>

        {misCursos.length === 0 ? (
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 text-center text-gray-500 dark:text-gray-400">
            No tienes cursos asignados actualmente.
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {misCursos.map(curso => (
              <div key={curso.id} className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white">
                      {curso.nombre_curso}
                    </h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {curso.nivel_nombre}
                    </p>
                  </div>
                  <span className="text-xs bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-200 px-2 py-1 rounded">
                    {curso.anio_academico_nombre}
                  </span>
                </div>
                <div className="mt-3">
                  <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Mis asignaturas:</p>
                  <div className="flex flex-wrap gap-1">
                    {curso.mis_asignaturas?.map(asig => (
                      <span key={asig.id} className="text-xs bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 px-2 py-0.5 rounded">
                        {asig.nombre}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Sección: Mis Planificaciones */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center">
            <svg className="h-6 w-6 mr-2 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
            Mis Planificaciones
          </h2>
          <button
            onClick={() => navigate('/planificaciones/nueva')}
            className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-colors inline-flex items-center"
          >
            <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Nueva Planificación
          </button>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200 dark:border-gray-700 mb-4">
          <nav className="-mb-px flex space-x-8">
            {[
              { id: 'anuales', label: 'Anuales', count: planificacionesAnuales.length },
              { id: 'unidades', label: 'Por Unidad', count: planificacionesUnidad.length },
              { id: 'semanales', label: 'Semanales', count: planificacionesSemanales.length },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-2 px-1 border-b-2 font-medium text-sm transition-colors ${activeTab === tab.id
                  ? 'border-primary-500 text-primary-600 dark:text-primary-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
                  }`}
              >
                {tab.label}
                <span className={`ml-2 px-2 py-0.5 rounded-full text-xs ${activeTab === tab.id
                  ? 'bg-primary-100 text-primary-600 dark:bg-primary-900 dark:text-primary-300'
                  : 'bg-gray-100 text-gray-500 dark:bg-gray-700 dark:text-gray-400'
                  }`}>
                  {tab.count}
                </span>
              </button>
            ))}
          </nav>
        </div>

        {/* Contenido de Tabs */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          {/* Tab Anuales - Vista jerárquica */}
          {activeTab === 'anuales' && (
            <div className="divide-y divide-gray-200 dark:divide-gray-700">
              {planificacionesAnuales.length === 0 ? (
                <div className="p-6 text-center text-gray-500 dark:text-gray-400">
                  No tienes planificaciones anuales. Crea una para comenzar.
                </div>
              ) : (
                planificacionesAnuales.map(anual => (
                  <div key={anual.id} className="p-4">
                    {/* Planificación Anual */}
                    <div
                      className="flex items-center justify-between cursor-pointer"
                      onClick={() => setExpandedAnual(expandedAnual === anual.id ? null : anual.id)}
                    >
                      <div className="flex items-center">
                        <svg
                          className={`h-5 w-5 mr-2 text-gray-400 transition-transform ${expandedAnual === anual.id ? 'rotate-90' : ''}`}
                          fill="none" viewBox="0 0 24 24" stroke="currentColor"
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                        <div>
                          <h3 className="font-medium text-gray-900 dark:text-white">{anual.titulo}</h3>
                          <p className="text-sm text-gray-500 dark:text-gray-400">
                            {anual.curso_info?.nombre_curso} • {anual.asignatura_info?.nombre_asignatura}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${getStatusBadge(anual.estado)}`}>
                          {anual.estado}
                        </span>
                        <span className="text-xs text-gray-400">
                          {anual.unidades_count || 0} unidades
                        </span>
                        <button
                          onClick={(e) => { e.stopPropagation(); navigate(`/planificaciones/editar/anual/${anual.id}`); }}
                          className="p-1 text-gray-500 hover:text-primary-600 dark:text-gray-400 dark:hover:text-primary-400 rounded"
                          title="Editar planificación"
                        >
                          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                          </svg>
                        </button>
                        {anual.estado === 'BORRADOR' && (
                          <button
                            onClick={(e) => { e.stopPropagation(); handleEnviarValidacion('anual', anual.id); }}
                            className="text-xs bg-primary-600 hover:bg-primary-700 text-white px-2 py-1 rounded"
                          >
                            Enviar
                          </button>
                        )}
                      </div>
                    </div>

                    {/* Unidades expandidas */}
                    {expandedAnual === anual.id && (
                      <div className="mt-3 ml-7 space-y-2">
                        {getUnidadesDeAnual(anual.id).map(unidad => (
                          <div key={unidad.id} className="border-l-2 border-blue-300 dark:border-blue-600 pl-4 py-2">
                            <div
                              className="flex items-center justify-between cursor-pointer"
                              onClick={(e) => { e.stopPropagation(); setExpandedUnidad(expandedUnidad === unidad.id ? null : unidad.id); }}
                            >
                              <div className="flex items-center">
                                <svg
                                  className={`h-4 w-4 mr-2 text-gray-400 transition-transform ${expandedUnidad === unidad.id ? 'rotate-90' : ''}`}
                                  fill="none" viewBox="0 0 24 24" stroke="currentColor"
                                >
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                </svg>
                                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                  Unidad {unidad.numero_unidad}: {unidad.titulo}
                                </span>
                              </div>
                              <div className="flex items-center gap-2">
                                <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${getStatusBadge(unidad.estado)}`}>
                                  {unidad.estado}
                                </span>
                                <button
                                  onClick={(e) => { e.stopPropagation(); navigate(`/planificaciones/editar/unidad/${unidad.id}`); }}
                                  className="p-1 text-gray-500 hover:text-primary-600 dark:text-gray-400 dark:hover:text-primary-400 rounded"
                                  title="Editar unidad"
                                >
                                  <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                                  </svg>
                                </button>
                                <button
                                  onClick={(e) => { e.stopPropagation(); navigate(`/planificaciones/nueva?tipo=semanal&unidad=${unidad.id}`); }}
                                  className="text-xs bg-purple-600 hover:bg-purple-700 text-white px-2 py-0.5 rounded"
                                  title="Añadir Semana"
                                >
                                  + Semana
                                </button>
                              </div>
                            </div>

                            {/* Semanas expandidas */}
                            {expandedUnidad === unidad.id && (
                              <div className="mt-2 ml-6 space-y-1">
                                {getSemanasDeUnidad(unidad.id).map(semana => (
                                  <div className="flex items-center py-1 border-l-2 border-purple-300 dark:border-purple-600 pl-4">
                                    <span className="text-sm text-gray-600 dark:text-gray-400 flex-1">
                                      Semana {semana.numero_semana}: {semana.titulo}
                                    </span>
                                    <div className="flex items-center gap-2">
                                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${getStatusBadge(semana.estado)}`}>
                                        {semana.estado}
                                      </span>
                                      <button
                                        onClick={(e) => { e.stopPropagation(); navigate(`/planificaciones/editar/semanal/${semana.id}`); }}
                                        className="p-1 text-gray-500 hover:text-primary-600 dark:text-gray-400 dark:hover:text-primary-400 rounded"
                                        title="Editar semana"
                                      >
                                        <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                                        </svg>
                                      </button>
                                    </div>
                                  </div>
                                ))}
                                {getSemanasDeUnidad(unidad.id).length === 0 && (
                                  <p className="text-xs text-gray-400 italic pl-4">Sin semanas planificadas</p>
                                )}
                              </div>
                            )}
                          </div>
                        ))}
                        {/* Botón añadir unidad */}
                        <button
                          onClick={(e) => { e.stopPropagation(); navigate(`/planificaciones/nueva?tipo=unidad&anual=${anual.id}`); }}
                          className="flex items-center text-sm text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 mt-2"
                        >
                          <svg className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                          </svg>
                          Añadir Unidad
                        </button>
                        {getUnidadesDeAnual(anual.id).length === 0 && (
                          <p className="text-sm text-gray-400 italic">Sin unidades planificadas</p>
                        )}
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          )}

          {/* Tab Unidades - Lista plana */}
          {activeTab === 'unidades' && (
            <div className="divide-y divide-gray-200 dark:divide-gray-700">
              {planificacionesUnidad.length === 0 ? (
                <div className="p-6 text-center text-gray-500 dark:text-gray-400">
                  No tienes planificaciones por unidad.
                </div>
              ) : (
                planificacionesUnidad.map(unidad => (
                  <div key={unidad.id} className="p-4 flex items-center justify-between">
                    <div>
                      <h3 className="font-medium text-gray-900 dark:text-white">
                        Unidad {unidad.numero_unidad}: {unidad.titulo}
                      </h3>
                      <p className="text-sm text-gray-500 dark:text-gray-400">
                        {unidad.curso_info?.nombre_curso} • {unidad.asignatura_info?.nombre_asignatura}
                        {unidad.planificacion_anual_titulo && (
                          <span className="ml-2 text-blue-500">→ {unidad.planificacion_anual_titulo}</span>
                        )}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${getStatusBadge(unidad.estado)}`}>
                        {unidad.estado}
                      </span>
                      {unidad.estado === 'BORRADOR' && (
                        <button
                          onClick={() => handleEnviarValidacion('unidad', unidad.id)}
                          className="text-xs bg-primary-600 hover:bg-primary-700 text-white px-2 py-1 rounded"
                        >
                          Enviar
                        </button>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          )}

          {/* Tab Semanales - Lista plana */}
          {activeTab === 'semanales' && (
            <div className="divide-y divide-gray-200 dark:divide-gray-700">
              {planificacionesSemanales.length === 0 ? (
                <div className="p-6 text-center text-gray-500 dark:text-gray-400">
                  No tienes planificaciones semanales.
                </div>
              ) : (
                planificacionesSemanales.map(semana => (
                  <div key={semana.id} className="p-4 flex items-center justify-between">
                    <div>
                      <h3 className="font-medium text-gray-900 dark:text-white">
                        Semana {semana.numero_semana}: {semana.titulo}
                      </h3>
                      <p className="text-sm text-gray-500 dark:text-gray-400">
                        {semana.curso_info?.nombre_curso} • {semana.asignatura_info?.nombre_asignatura}
                        {semana.planificacion_unidad_titulo && (
                          <span className="ml-2 text-purple-500">→ {semana.planificacion_unidad_titulo}</span>
                        )}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${getStatusBadge(semana.estado)}`}>
                        {semana.estado}
                      </span>
                      {semana.estado === 'BORRADOR' && (
                        <button
                          onClick={() => handleEnviarValidacion('semanal', semana.id)}
                          className="text-xs bg-primary-600 hover:bg-primary-700 text-white px-2 py-1 rounded"
                        >
                          Enviar
                        </button>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      </div>
    </div >
  );
};

export default DashboardDocente;