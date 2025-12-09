import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const GestionCursos = () => {
  const navigate = useNavigate();
  const [cursos, setCursos] = useState([]);
  const [nivelesEducativos, setNivelesEducativos] = useState([]);
  const [asignaturas, setAsignaturas] = useState([]);
  const [aniosAcademicos, setAniosAcademicos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    nombre_curso: '',
    nivel: '',
    paralelo: '',
    anio_academico: '',
    capacidad_maxima: 40
  });

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
      const [cursosRes, nivelesRes, asignaturasRes, aniosRes] = await Promise.all([
        axios.get('http://localhost/api/cursos/', getAuthHeaders()),
        axios.get('http://localhost/api/niveles-educativos/', getAuthHeaders()),
        axios.get('http://localhost/api/asignaturas/', getAuthHeaders()),
        axios.get('http://localhost/api/anios-academicos/', getAuthHeaders())
      ]);
      
      // Solo mostrar cursos NO archivados (años activos o en borrador)
      setCursos(cursosRes.data.filter(c => !c.archivado));
      setNivelesEducativos(nivelesRes.data);
      setAsignaturas(asignaturasRes.data);
      // Solo años activos o en borrador pueden tener cursos nuevos
      setAniosAcademicos(aniosRes.data.filter(a => a.estado === 'ACTIVO' || a.estado === 'BORRADOR'));
    } catch (error) {
      console.error('Error cargando datos:', error);
      alert('Error al cargar datos: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      await axios.post('http://localhost/api/cursos/', formData, getAuthHeaders());
      alert('Curso creado exitosamente');
      setShowForm(false);
      setFormData({
        nombre_curso: '',
        nivel: '',
        paralelo: '',
        anio_academico: '',
        capacidad_maxima: 40
      });
      cargarDatos();
    } catch (error) {
      console.error('Error creando curso:', error);
      alert('Error al crear curso: ' + (error.response?.data?.detail || error.message));
    }
  };

  const eliminarCurso = async (id) => {
    if (!confirm('¿Está seguro de eliminar este curso?')) return;
    
    try {
      await axios.delete(`http://localhost/api/cursos/${id}/`, getAuthHeaders());
      alert('Curso eliminado');
      cargarDatos();
    } catch (error) {
      console.error('Error eliminando curso:', error);
      alert('Error al eliminar curso');
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
          <button
            onClick={() => setShowForm(true)}
            className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-colors inline-flex items-center"
          >
            <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Nuevo Curso
          </button>
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
                  <button
                    onClick={() => eliminarCurso(curso.id)}
                    className="inline-flex items-center px-3 py-1.5 bg-red-100 hover:bg-red-200 dark:bg-red-900/30 dark:hover:bg-red-900/50 text-red-700 dark:text-red-400 rounded-lg font-medium transition-colors"
                  >
                    <svg className="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    Eliminar
                  </button>
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
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4 max-h-[90vh] overflow-y-auto">
            <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-gray-100">Crear Nuevo Curso</h3>
            <form onSubmit={handleSubmit}>
              <div className="mb-4">
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
              
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Nivel Educativo</label>
                <select
                  value={formData.nivel}
                  onChange={(e) => setFormData({ ...formData, nivel: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  required
                >
                  <option value="">Seleccione un nivel</option>
                  {nivelesEducativos.map(nivel => (
                    <option key={nivel.id} value={nivel.id}>{nivel.nombre}</option>
                  ))}
                </select>
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Paralelo (opcional)</label>
                <input
                  type="text"
                  value={formData.paralelo}
                  onChange={(e) => setFormData({ ...formData, paralelo: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  placeholder="Ej: A, B, C"
                />
              </div>

              <div className="mb-4">
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

              <div className="mb-4">
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

              <div className="flex gap-2">
                <button type="submit" className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">
                  Crear Curso
                </button>
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="flex-1 px-4 py-2 bg-gray-300 dark:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default GestionCursos;
