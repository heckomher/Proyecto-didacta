import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuth } from '../hooks/useAuth';
import apiClient from '../services/api';

const GestionCursos = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [cursos, setCursos] = useState([]);
  const [nivelesEducativos, setNivelesEducativos] = useState([]);
  const [asignaturas, setAsignaturas] = useState([]);
  const [asignaturasSugeridas, setAsignaturasSugeridas] = useState([]);
  const [electivosSugeridos, setElectivosSugeridos] = useState([]);
  const [aniosAcademicos, setAniosAcademicos] = useState([]);
  const [docentes, setDocentes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [showDocentesModal, setShowDocentesModal] = useState(false);
  const [cursoParaDocentes, setCursoParaDocentes] = useState(null);
  const [editingCurso, setEditingCurso] = useState(null);
  const [formData, setFormData] = useState({
    nombre_curso: '',
    nivel: '',
    paralelo: '',
    anio_academico: '',
    capacidad_maxima: 40,
    asignaturas: [],
    plan_diferenciado: ''
  });

  const isUTP = user?.role === 'UTP';

  useEffect(() => {
    cargarDatos();
  }, []);

  const cargarDatos = async () => {
    try {
      const [cursosRes, nivelesRes, asignaturasRes, aniosRes, docentesRes] = await Promise.all([
        apiClient.get('/cursos/'),
        apiClient.get('/niveles-educativos/'),
        apiClient.get('/asignaturas/'),
        apiClient.get('/anios-academicos/'),
        apiClient.get('/docentes/')
      ]);

      // Solo mostrar cursos NO archivados (años activos o en borrador)
      setCursos(cursosRes.data.filter(c => !c.archivado));
      setNivelesEducativos(nivelesRes.data);
      setAsignaturas(asignaturasRes.data);
      setDocentes(docentesRes.data);
      // Solo años activos o en borrador pueden tener cursos nuevos
      setAniosAcademicos(aniosRes.data.filter(a => a.estado === 'ACTIVO' || a.estado === 'BORRADOR'));
    } catch (error) {
      console.error('Error cargando datos:', error);
      toast.error('Error al cargar datos: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const cargarAsignaturasSugeridas = async (nivelId) => {
    if (!nivelId) {
      setAsignaturasSugeridas([]);
      return;
    }

    try {
      const nivel = nivelesEducativos.find(n => n.id === parseInt(nivelId));
      if (!nivel) return;

      const response = await apiClient.get(`/asignaturas/sugeridas-por-nivel/${encodeURIComponent(nivel.nombre)}/`);
      setAsignaturasSugeridas(response.data);
    } catch (error) {
      console.error('Error cargando asignaturas sugeridas:', error);
      setAsignaturasSugeridas(asignaturas.filter(a => a.tipo === 'COMUN'));
    }
  };

  const cargarElectivos = async (plan) => {
    if (!plan || plan === 'MEDIO_1_2') {
      setElectivosSugeridos([]);
      return;
    }

    try {
      const response = await apiClient.get(`/asignaturas/electivos-por-plan/${plan}/`);
      setElectivosSugeridos(response.data);
    } catch (error) {
      console.error('Error cargando electivos:', error);
      setElectivosSugeridos([]);
    }
  };

  // Detectar si el nivel es Educación Media
  const esEducacionMedia = () => {
    if (!formData.nivel) return false;
    const nivel = nivelesEducativos.find(n => n.id === parseInt(formData.nivel));
    return nivel?.nombre?.toLowerCase().includes('media');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    console.log('Guardando curso con datos:', formData);

    try {
      if (editingCurso) {
        const response = await apiClient.put(`/cursos/${editingCurso.id}/`, formData);
        console.log('Respuesta del servidor:', response.data);
        toast.success('Curso actualizado exitosamente');
      } else {
        const response = await apiClient.post('/cursos/', formData);
        console.log('Respuesta del servidor:', response.data);
        toast.success('Curso creado exitosamente');
      }
      setShowForm(false);
      setEditingCurso(null);
      setFormData({
        nombre_curso: '',
        nivel: '',
        paralelo: '',
        anio_academico: '',
        capacidad_maxima: 40,
        asignaturas: [],
        plan_diferenciado: ''
      });
      setElectivosSugeridos([]);
      cargarDatos();
    } catch (error) {
      console.error('Error guardando curso:', error);
      toast.error('Error al guardar curso: ' + (error.response?.data?.detail || error.message));
    }
  };

  const editarCurso = (curso) => {
    setEditingCurso(curso);
    // Extraer solo los IDs de las asignaturas
    const asignaturasIds = curso.asignaturas?.map(a => typeof a === 'number' ? a : a.id) || [];
    setFormData({
      nombre_curso: curso.nombre_curso,
      nivel: curso.nivel,
      paralelo: curso.paralelo || '',
      anio_academico: curso.anio_academico,
      capacidad_maxima: curso.capacidad_maxima,
      asignaturas: asignaturasIds,
      plan_diferenciado: curso.plan_diferenciado || ''
    });
    cargarAsignaturasSugeridas(curso.nivel);
    if (curso.plan_diferenciado && curso.plan_diferenciado !== 'MEDIO_1_2') {
      cargarElectivos(curso.plan_diferenciado);
    }
    setShowForm(true);
  };

  const eliminarCurso = async (id) => {
    if (!confirm('¿Está seguro de eliminar este curso?')) return;

    try {
      await apiClient.delete(`/cursos/${id}/`);
      toast.success('Curso eliminado');
      cargarDatos();
    } catch (error) {
      console.error('Error eliminando curso:', error);
      toast.error('Error al eliminar curso');
    }
  };

  const abrirGestionDocentes = (curso) => {
    setCursoParaDocentes(curso);
    setShowDocentesModal(true);
  };

  const asignarDocente = async (asignaturaId, docenteId) => {
    try {
      await apiClient.post(
        `/cursos/${cursoParaDocentes.id}/asignar-docente/`,
        { asignatura_id: asignaturaId, docente_id: docenteId }
      );
      // Recargar datos del curso
      const cursoRes = await apiClient.get(`/cursos/${cursoParaDocentes.id}/`);
      setCursoParaDocentes(cursoRes.data);
      cargarDatos();
    } catch (error) {
      console.error('Error asignando docente:', error);
      toast.error('Error al asignar docente: ' + (error.response?.data?.detail || error.message));
    }
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
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Gestión de Cursos</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">Administra los cursos del año académico activo o en borrador</p>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-500">Los cursos se archivan automáticamente cuando se cierra el año académico</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => navigate('/')}
            className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg font-medium transition-colors"
          >
            ← Volver al Dashboard
          </button>
          {isUTP && (
            <button
              onClick={() => setShowForm(true)}
              className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-colors inline-flex items-center"
            >
              <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              Nuevo Curso
            </button>
          )}
        </div>
      </div>

      {/* Lista de cursos */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead className="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Curso</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Nivel</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Año Académico</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Capacidad</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            {cursos.map((curso) => (
              <tr key={curso.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  {curso.nombre_curso} {curso.paralelo}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {curso.nivel_nombre}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {curso.anio_academico_nombre}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {curso.capacidad_maxima} estudiantes
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  {isUTP ? (
                    <div className="flex gap-2">
                      <button
                        onClick={() => editarCurso(curso)}
                        className="inline-flex items-center px-3 py-1.5 bg-blue-100 hover:bg-blue-200 dark:bg-blue-900/30 dark:hover:bg-blue-900/50 text-blue-700 dark:text-blue-400 rounded-lg font-medium transition-colors"
                      >
                        <svg className="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                        Editar
                      </button>
                      <button
                        onClick={() => abrirGestionDocentes(curso)}
                        className="inline-flex items-center px-3 py-1.5 bg-green-100 hover:bg-green-200 dark:bg-green-900/30 dark:hover:bg-green-900/50 text-green-700 dark:text-green-400 rounded-lg font-medium transition-colors"
                      >
                        <svg className="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                        </svg>
                        Docentes
                      </button>
                      <button
                        onClick={() => eliminarCurso(curso.id)}
                        className="inline-flex items-center px-3 py-1.5 bg-red-100 hover:bg-red-200 dark:bg-red-900/30 dark:hover:bg-red-900/50 text-red-700 dark:text-red-400 rounded-lg font-medium transition-colors"
                      >
                        <svg className="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                        Eliminar
                      </button>
                    </div>
                  ) : (
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      Solo lectura
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {cursos.length === 0 && (
          <div className="text-center py-12 text-gray-500 dark:text-gray-400">
            No hay cursos activos. Crea uno nuevo para comenzar.
            <p className="mt-2 text-sm">Los cursos archivados se pueden consultar en el Historial de Cursos.</p>
          </div>
        )}
      </div>

      {/* Modal Formulario */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-gray-100">
              {editingCurso ? 'Editar Curso' : 'Crear Nuevo Curso'}
            </h3>
            <form onSubmit={handleSubmit}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Nombre del Curso</label>
                  <input
                    type="text"
                    value={formData.nombre_curso}
                    onChange={(e) => setFormData({ ...formData, nombre_curso: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                    placeholder="Ej: 1° Básico, 2° Medio"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Nivel Educativo</label>
                  <select
                    value={formData.nivel}
                    onChange={(e) => {
                      setFormData({ ...formData, nivel: e.target.value, asignaturas: [] });
                      cargarAsignaturasSugeridas(e.target.value);
                    }}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                    required
                  >
                    <option value="">Seleccione un nivel</option>
                    {nivelesEducativos.map(nivel => (
                      <option key={nivel.id} value={nivel.id}>{nivel.nombre}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Paralelo (opcional)</label>
                  <input
                    type="text"
                    value={formData.paralelo}
                    onChange={(e) => setFormData({ ...formData, paralelo: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                    placeholder="Ej: A, B, C"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Año Académico</label>
                  <select
                    value={formData.anio_academico}
                    onChange={(e) => setFormData({ ...formData, anio_academico: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                    required
                  >
                    <option value="">Seleccione un año académico</option>
                    {aniosAcademicos.map(anio => (
                      <option key={anio.id} value={anio.id}>
                        {anio.nombre} ({anio.estado})
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Capacidad Máxima</label>
                  <input
                    type="number"
                    value={formData.capacidad_maxima}
                    onChange={(e) => setFormData({ ...formData, capacidad_maxima: parseInt(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                    min="1"
                    required
                  />
                </div>
              </div>

              {/* Plan Diferenciado - Solo para Educación Media */}
              {esEducacionMedia() && (
                <div className="mt-4 p-4 border border-blue-200 dark:border-blue-800 rounded-lg bg-blue-50 dark:bg-blue-900/20">
                  <label className="block text-sm font-medium mb-2 text-blue-800 dark:text-blue-200">
                    Plan Diferenciado (Educación Media)
                  </label>
                  <select
                    value={formData.plan_diferenciado}
                    onChange={(e) => {
                      const nuevoPlan = e.target.value;
                      setFormData({ ...formData, plan_diferenciado: nuevoPlan });
                      cargarElectivos(nuevoPlan);
                    }}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  >
                    <option value="">Seleccione un plan</option>
                    <option value="MEDIO_1_2">1°-2° Medio (Plan Común)</option>
                    <option value="CH">3°-4° Científico-Humanista</option>
                    <option value="TP">3°-4° Técnico Profesional</option>
                    <option value="ARTISTICO">3°-4° Artístico</option>
                  </select>
                  <p className="mt-2 text-xs text-blue-600 dark:text-blue-400">
                    {formData.plan_diferenciado && formData.plan_diferenciado !== 'MEDIO_1_2' &&
                      'Los electivos se compartirán con otros cursos del mismo plan.'
                    }
                  </p>
                </div>
              )}

              {/* Asignaturas Comunes */}
              {formData.nivel && asignaturasSugeridas.length > 0 && (
                <div className="mt-6">
                  <div className="flex justify-between items-center mb-2">
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                      📚 Asignaturas Comunes
                      <span className="text-xs text-gray-500 dark:text-gray-400 ml-2">
                        (Obligatorias para este nivel)
                      </span>
                    </label>
                    <button
                      type="button"
                      onClick={() => {
                        const comunesIds = asignaturasSugeridas.map(a => a.id);
                        const otrasSeleccionadas = formData.asignaturas.filter(id => !comunesIds.includes(id));
                        if (formData.asignaturas.filter(id => comunesIds.includes(id)).length === comunesIds.length) {
                          // Si todas las comunes están seleccionadas, deseleccionar solo las comunes
                          setFormData({ ...formData, asignaturas: otrasSeleccionadas });
                        } else {
                          // Seleccionar todas las comunes, mantener las electivas
                          setFormData({ ...formData, asignaturas: [...new Set([...otrasSeleccionadas, ...comunesIds])] });
                        }
                      }}
                      className="px-3 py-1 text-xs bg-primary-100 hover:bg-primary-200 dark:bg-primary-900/30 dark:hover:bg-primary-900/50 text-primary-700 dark:text-primary-400 rounded-lg font-medium transition-colors"
                    >
                      {asignaturasSugeridas.every(a => formData.asignaturas.includes(a.id)) ? 'Deseleccionar comunes' : 'Seleccionar todas las comunes'}
                    </button>
                  </div>
                  <div className="border border-gray-300 dark:border-gray-600 rounded-lg p-4 max-h-60 overflow-y-auto bg-gray-50 dark:bg-gray-700/50">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {asignaturasSugeridas.map(asignatura => (
                        <label key={asignatura.id} className="flex items-start space-x-2 p-2 hover:bg-gray-100 dark:hover:bg-gray-600/50 rounded cursor-pointer">
                          <input
                            type="checkbox"
                            checked={formData.asignaturas.includes(asignatura.id)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setFormData({
                                  ...formData,
                                  asignaturas: [...formData.asignaturas, asignatura.id]
                                });
                              } else {
                                setFormData({
                                  ...formData,
                                  asignaturas: formData.asignaturas.filter(id => id !== asignatura.id)
                                });
                              }
                            }}
                            className="mt-0.5 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                          />
                          <span className="text-sm text-gray-700 dark:text-gray-300">
                            {asignatura.nombre_asignatura}
                          </span>
                        </label>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Electivos - Solo para 3°-4° Media con plan seleccionado */}
              {electivosSugeridos.length > 0 && (
                <div className="mt-6">
                  <div className="flex justify-between items-center mb-2">
                    <label className="block text-sm font-medium text-purple-700 dark:text-purple-300">
                      🎯 Electivos del Plan
                      <span className="text-xs text-purple-500 dark:text-purple-400 ml-2">
                        ({formData.plan_diferenciado === 'CH' ? 'Científico-Humanista' :
                          formData.plan_diferenciado === 'TP' ? 'Técnico Profesional' :
                            formData.plan_diferenciado === 'ARTISTICO' ? 'Artístico' : ''})
                      </span>
                    </label>
                    <button
                      type="button"
                      onClick={() => {
                        const electivosIds = electivosSugeridos.map(a => a.id);
                        const otrasSeleccionadas = formData.asignaturas.filter(id => !electivosIds.includes(id));
                        if (formData.asignaturas.filter(id => electivosIds.includes(id)).length === electivosIds.length) {
                          setFormData({ ...formData, asignaturas: otrasSeleccionadas });
                        } else {
                          setFormData({ ...formData, asignaturas: [...new Set([...otrasSeleccionadas, ...electivosIds])] });
                        }
                      }}
                      className="px-3 py-1 text-xs bg-purple-100 hover:bg-purple-200 dark:bg-purple-900/30 dark:hover:bg-purple-900/50 text-purple-700 dark:text-purple-400 rounded-lg font-medium transition-colors"
                    >
                      {electivosSugeridos.every(a => formData.asignaturas.includes(a.id)) ? 'Deseleccionar electivos' : 'Seleccionar todos los electivos'}
                    </button>
                  </div>
                  <div className="border border-purple-300 dark:border-purple-600 rounded-lg p-4 max-h-60 overflow-y-auto bg-purple-50 dark:bg-purple-900/20">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {electivosSugeridos.map(asignatura => (
                        <label key={asignatura.id} className="flex items-start space-x-2 p-2 hover:bg-purple-100 dark:hover:bg-purple-800/30 rounded cursor-pointer">
                          <input
                            type="checkbox"
                            checked={formData.asignaturas.includes(asignatura.id)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setFormData({
                                  ...formData,
                                  asignaturas: [...formData.asignaturas, asignatura.id]
                                });
                              } else {
                                setFormData({
                                  ...formData,
                                  asignaturas: formData.asignaturas.filter(id => id !== asignatura.id)
                                });
                              }
                            }}
                            className="mt-0.5 rounded border-purple-300 text-purple-600 focus:ring-purple-500"
                          />
                          <span className="text-sm text-purple-700 dark:text-purple-300">
                            {asignatura.nombre_asignatura}
                          </span>
                        </label>
                      ))}
                    </div>
                  </div>
                  <p className="mt-2 text-xs text-purple-500 dark:text-purple-400">
                    Los alumnos de 3° y 4° medio pueden mezclarse en estos electivos.
                  </p>
                </div>
              )}

              {/* Resumen de selección */}
              {formData.nivel && (
                <p className="mt-4 text-sm text-gray-600 dark:text-gray-400">
                  Total: {formData.asignaturas.length} asignatura(s) seleccionada(s)
                  {electivosSugeridos.length > 0 && (
                    <span className="ml-2 text-purple-600 dark:text-purple-400">
                      ({formData.asignaturas.filter(id => electivosSugeridos.some(e => e.id === id)).length} electivo(s))
                    </span>
                  )}
                </p>
              )}

              <div className="flex gap-2 mt-6">
                <button type="submit" className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">
                  {editingCurso ? 'Guardar Cambios' : 'Crear Curso'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowForm(false);
                    setEditingCurso(null);
                    setFormData({
                      nombre_curso: '',
                      nivel: '',
                      paralelo: '',
                      anio_academico: '',
                      capacidad_maxima: 40,
                      asignaturas: [],
                      plan_diferenciado: ''
                    });
                    setElectivosSugeridos([]);
                  }}
                  className="flex-1 px-4 py-2 bg-gray-300 dark:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal Gestionar Docentes */}
      {showDocentesModal && cursoParaDocentes && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-3xl w-full max-h-[80vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                  Gestionar Docentes - {cursoParaDocentes.nombre_curso}
                </h3>
                <button
                  onClick={() => {
                    setShowDocentesModal(false);
                    setCursoParaDocentes(null);
                  }}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div className="space-y-4">
                {cursoParaDocentes.asignaturas_asignadas && cursoParaDocentes.asignaturas_asignadas.length > 0 ? (
                  cursoParaDocentes.asignaturas_asignadas.map((asig) => (
                    <div key={asig.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        {asig.asignatura_nombre}
                      </label>
                      <select
                        value={asig.docente || ''}
                        onChange={(e) => asignarDocente(asig.asignatura, e.target.value || null)}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                      >
                        <option value="">Sin asignar</option>
                        {docentes.map((docente) => (
                          <option key={docente.id} value={docente.id}>
                            {docente.usuario_nombre} - {docente.especialidad}
                          </option>
                        ))}
                      </select>
                      {asig.docente_nombre && (
                        <p className="mt-1 text-sm text-green-600 dark:text-green-400">
                          Asignado: {asig.docente_nombre}
                        </p>
                      )}
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                    No hay asignaturas asignadas a este curso.
                    <br />
                    Por favor, edite el curso para seleccionar asignaturas.
                  </div>
                )}
              </div>

              <div className="mt-6">
                <button
                  onClick={() => {
                    setShowDocentesModal(false);
                    setCursoParaDocentes(null);
                  }}
                  className="w-full px-4 py-2 bg-gray-300 dark:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500"
                >
                  Cerrar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GestionCursos;
