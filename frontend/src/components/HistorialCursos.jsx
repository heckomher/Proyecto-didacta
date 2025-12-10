import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import apiClient from '../services/api';

const HistorialCursos = () => {
  const navigate = useNavigate();
  const [aniosCerrados, setAniosCerrados] = useState([]);
  const [anioSeleccionado, setAnioSeleccionado] = useState(null);
  const [cursosArchivados, setCursosArchivados] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    cargarAniosCerrados();
  }, []);

  const cargarAniosCerrados = async () => {
    try {
      const response = await apiClient.get('/anios-academicos/');
      const cerrados = response.data.filter(a => a.estado === 'CERRADO');
      setAniosCerrados(cerrados);

      if (cerrados.length > 0) {
        setAnioSeleccionado(cerrados[0].id);
        cargarCursosArchivados(cerrados[0].id);
      } else {
        setLoading(false);
      }
    } catch (error) {
      console.error('Error cargando años cerrados:', error);
      toast.error('Error al cargar historial: ' + (error.response?.data?.detail || error.message));
      setLoading(false);
    }
  };

  const cargarCursosArchivados = async (anioId) => {
    try {
      setLoading(true);
      const response = await apiClient.get(`/cursos/?anio_academico=${anioId}`);
      setCursosArchivados(response.data.filter(c => c.archivado));
    } catch (error) {
      console.error('Error cargando cursos archivados:', error);
      toast.error('Error al cargar cursos');
    } finally {
      setLoading(false);
    }
  };

  const handleAnioChange = (anioId) => {
    setAnioSeleccionado(anioId);
    cargarCursosArchivados(anioId);
  };

  if (loading && aniosCerrados.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Cargando historial...</div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Historial de Cursos</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">Consulta los cursos de años académicos cerrados (solo lectura)</p>
        </div>
        <button
          onClick={() => navigate('/')}
          className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg font-medium transition-colors"
        >
          ← Volver al Dashboard
        </button>
      </div>

      {aniosCerrados.length === 0 ? (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-8 text-center">
          <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
          <h3 className="mt-2 text-lg font-medium text-gray-900 dark:text-white">No hay años académicos cerrados</h3>
          <p className="mt-1 text-gray-500 dark:text-gray-400">
            Los cursos aparecerán aquí cuando se cierre un año académico.
          </p>
        </div>
      ) : (
        <>
          {/* Selector de año */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
            <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
              Selecciona un Año Académico Cerrado:
            </label>
            <select
              value={anioSeleccionado || ''}
              onChange={(e) => handleAnioChange(parseInt(e.target.value))}
              className="w-full max-w-md px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
            >
              {aniosCerrados.map(anio => (
                <option key={anio.id} value={anio.id}>
                  {anio.nombre} ({anio.fecha_inicio} - {anio.fecha_fin})
                </option>
              ))}
            </select>
          </div>

          {/* Tabla de cursos archivados */}
          {loading ? (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
              <p className="mt-4 text-gray-600 dark:text-gray-400">Cargando cursos...</p>
            </div>
          ) : (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
              <div className="px-6 py-4 bg-yellow-50 dark:bg-yellow-900/20 border-b border-yellow-200 dark:border-yellow-800">
                <div className="flex items-center">
                  <svg className="h-5 w-5 text-yellow-600 dark:text-yellow-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                  <span className="text-sm font-medium text-yellow-800 dark:text-yellow-200">
                    Estos cursos están archivados y solo pueden consultarse. No se pueden modificar.
                  </span>
                </div>
              </div>

              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Curso</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Nivel</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Capacidad</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Estado</th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {cursosArchivados.map((curso) => (
                    <tr key={curso.id} className="opacity-75">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                        {curso.nombre_curso} {curso.paralelo}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                        {curso.nivel_nombre}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                        {curso.capacidad_maxima} estudiantes
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300">
                          <svg className="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
                          </svg>
                          Archivado
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {cursosArchivados.length === 0 && (
                <div className="text-center py-12 text-gray-500 dark:text-gray-400">
                  No hay cursos archivados para este año académico.
                </div>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default HistorialCursos;
