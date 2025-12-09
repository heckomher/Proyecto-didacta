import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const GestionCursos = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [cursos, setCursos] = useState([]);
  const [nivelesEducativos, setNivelesEducativos] = useState([]);
  const [asignaturas, setAsignaturas] = useState([]);
  const [asignaturasSugeridas, setAsignaturasSugeridas] = useState([]);
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
    asignaturas: []
  });

  const isUTP = user?.role === 'UTP';

  const getAuthHeaders = () => {
    const token = localStorage.getItem('token');
    return {
      headers: { 'Authorization': `Bearer ${token}` }
    };
  };

  useEffect(() => {
    cargarDatos();
  }, []);

  const cargarDatos = async () => {
    try {
      const [cursosRes, nivelesRes, asignaturasRes, aniosRes, docentesRes] = await Promise.all([
        axios.get('/cursos/', getAuthHeaders()),
        axios.get('/niveles-educativos/', getAuthHeaders()),
        axios.get('/asignaturas/', getAuthHeaders()),
        axios.get('/anios-academicos/', getAuthHeaders()),
        axios.get('/docentes/', getAuthHeaders())
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
      alert('Error al cargar datos: ' + (error.response?.data?.detail || error.message));
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
      
      const response = await axios.get(`/asignaturas/sugeridas-por-nivel/${encodeURIComponent(nivel.nombre)}/`, getAuthHeaders());
      setAsignaturasSugeridas(response.data);
    } catch (error) {
      console.error('Error cargando asignaturas sugeridas:', error);
      // Si falla, mostrar todas las asignaturas
      setAsignaturasSugeridas(asignaturas);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      if (editingCurso) {
        await axios.put(`/cursos/${editingCurso.id}/`, formData, getAuthHeaders());
        alert('Curso actualizado exitosamente');
      } else {
        await axios.post('/cursos/', formData, getAuthHeaders());
        alert('Curso creado exitosamente');
      }
      setShowForm(false);
      setEditingCurso(null);
      setFormData({
        nombre_curso: '',
        nivel: '',
        paralelo: '',
        anio_academico: '',
        capacidad_maxima: 40,
        asignaturas: []
      });
      cargarDatos();
    } catch (error) {
      console.error('Error guardando curso:', error);
      alert('Error al guardar curso: ' + (error.response?.data?.detail || error.message));
    }
  };

  const editarCurso = (curso) => {
    setEditingCurso(curso);
    setFormData({
      nombre_curso: curso.nombre_curso,
      nivel: curso.nivel,
      paralelo: curso.paralelo || '',
      anio_academico: curso.anio_academico,
      capacidad_maxima: curso.capacidad_maxima,
      asignaturas: curso.asignaturas || []
    });
    cargarAsignaturasSugeridas(curso.nivel);
    setShowForm(true);
  };

  const eliminarCurso = async (id) => {
    if (!confirm('¿Está seguro de eliminar este curso?')) return;
    
    try {
      await axios.delete(`/cursos/${id}/`, getAuthHeaders());
      alert('Curso eliminado');
      cargarDatos();
    } catch (error) {
      console.error('Error eliminando curso:', error);
      alert('Error al eliminar curso');
    }
  };

  const abrirGestionDocentes = (curso) => {
    setCursoParaDocentes(curso);
    setShowDocentesModal(true);
  };

  const asignarDocente = async (asignaturaId, docenteId) => {
    try {
      await axios.post(
        `/cursos/${cursoParaDocentes.id}/asignar-docente/`,
        { asignatura_id: asignaturaId, docente_id: docenteId },
        getAuthHeaders()
      );
      // Recargar datos del curso
      const cursoRes = await axios.get(`/cursos/${cursoParaDocentes.id}/`, getAuthHeaders());
      setCursoParaDocentes(cursoRes.data);
      cargarDatos();
    } catch (error) {
      console.error('Error asignando docente:', error);
      alert('Error al asignar docente: ' + (error.response?.data?.detail || error.message));
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

              {/* Asignaturas Sugeridas */}
              {formData.nivel && asignaturasSugeridas.length > 0 && (
                <div className="mt-6">
                  <div className="flex justify-between items-center mb-2">
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                      Asignaturas Sugeridas para este nivel
                      <span className="text-xs text-gray-500 dark:text-gray-400 ml-2">
                        (Seleccione las que aplicarán para este curso)
                      </span>
                    </label>
                    <button
                      type="button"
                      onClick={() => {
                        if (formData.asignaturas.length === asignaturasSugeridas.length) {
                          // Si todas están seleccionadas, deseleccionar todas
                          setFormData({ ...formData, asignaturas: [] });
                        } else {
                          // Seleccionar todas
                          setFormData({ ...formData, asignaturas: asignaturasSugeridas.map(a => a.id) });
                        }
                      }}
                      className="px-3 py-1 text-xs bg-primary-100 hover:bg-primary-200 dark:bg-primary-900/30 dark:hover:bg-primary-900/50 text-primary-700 dark:text-primary-400 rounded-lg font-medium transition-colors"
                    >
                      {formData.asignaturas.length === asignaturasSugeridas.length ? 'Deseleccionar todas' : 'Seleccionar todas'}
                    </button>
                  </div>
                  <div className="border border-gray-300 dark:border-gray-600 rounded-lg p-4 max-h-60 overflow-y-auto bg-gray-50 dark:bg-gray-700/50">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {asignaturasSugeridas.map(asignatura => (
                        <label key={asignatura.id} className="flex items-center space-x-2 p-2 hover:bg-gray-100 dark:hover:bg-gray-600/50 rounded cursor-pointer">
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
                            className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                          />
                          <span className="text-sm text-gray-700 dark:text-gray-300">
                            {asignatura.nombre_asignatura}
                          </span>
                        </label>
                      ))}
                    </div>
                  </div>
                  <p className="mt-2 text-xs text-gray-500 dark:text-gray-400">
                    {formData.asignaturas.length} asignatura(s) seleccionada(s)
                  </p>
                </div>
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
                      asignaturas: []
                    });
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
