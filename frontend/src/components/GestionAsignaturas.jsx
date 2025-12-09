import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../hooks/useAuth';

const GestionAsignaturas = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [asignaturas, setAsignaturas] = useState([]);
  const [docentes, setDocentes] = useState([]);
  const [cursos, setCursos] = useState([]);
  const [filtroNivel, setFiltroNivel] = useState('');
  const [nivelesEducativos, setNivelesEducativos] = useState([]);
  const [showAsignarModal, setShowAsignarModal] = useState(false);
  const [asignaturaSeleccionada, setAsignaturaSeleccionada] = useState(null);
  const [cursoAsignaturas, setCursoAsignaturas] = useState([]);

  const isUTP = user?.role === 'UTP';

  const getAuthHeaders = () => ({
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  });

  useEffect(() => {
    cargarDatos();
  }, []);

  const cargarDatos = async () => {
    try {
      const [asignaturasRes, docentesRes, cursosRes, nivelesRes] = await Promise.all([
        axios.get('/asignaturas/', getAuthHeaders()),
        axios.get('/docentes/', getAuthHeaders()),
        axios.get('/cursos/', getAuthHeaders()),
        axios.get('/niveles-educativos/', getAuthHeaders())
      ]);
      
      console.log('Asignaturas cargadas:', asignaturasRes.data.length);
      console.log('Docentes cargados:', docentesRes.data.length);
      console.log('Cursos cargados:', cursosRes.data.length);
      
      setAsignaturas(asignaturasRes.data);
      setDocentes(docentesRes.data);
      setCursos(cursosRes.data.filter(c => !c.archivado));
      setNivelesEducativos(nivelesRes.data);
    } catch (error) {
      console.error('Error cargando datos:', error);
      alert('Error al cargar datos: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const abrirModalAsignar = async (asignatura) => {
    setAsignaturaSeleccionada(asignatura);
    
    // Obtener todos los CursoAsignatura que tienen esta asignatura
    const cursosConAsignatura = [];
    for (const curso of cursos) {
      if (curso.asignaturas_asignadas) {
        const cursoAsig = curso.asignaturas_asignadas.find(ca => ca.asignatura === asignatura.id);
        if (cursoAsig) {
          cursosConAsignatura.push({
            ...cursoAsig,
            curso_nombre: curso.nombre_curso + (curso.paralelo ? ' ' + curso.paralelo : ''),
            curso_id: curso.id
          });
        }
      }
    }
    
    setCursoAsignaturas(cursosConAsignatura);
    setShowAsignarModal(true);
  };

  const asignarDocente = async (cursoAsignaturaId, cursoId, docenteId) => {
    try {
      await axios.post(
        `/cursos/${cursoId}/asignar-docente/`,
        { 
          asignatura_id: asignaturaSeleccionada.id, 
          docente_id: docenteId 
        },
        getAuthHeaders()
      );
      
      // Recargar datos
      await cargarDatos();
      
      // Actualizar la lista local
      setCursoAsignaturas(prev => prev.map(ca => 
        ca.id === cursoAsignaturaId 
          ? { ...ca, docente: docenteId, docente_nombre: docentes.find(d => d.id === docenteId)?.usuario_nombre }
          : ca
      ));
      
    } catch (error) {
      console.error('Error asignando docente:', error);
      alert('Error al asignar docente: ' + (error.response?.data?.detail || error.message));
    }
  };

  const asignaturasFilteradas = filtroNivel 
    ? asignaturas.filter(a => a.nivel_educativo === parseInt(filtroNivel))
    : asignaturas;

  console.log('Estado actual:', {
    totalAsignaturas: asignaturas.length,
    filtradas: asignaturasFilteradas.length,
    filtroNivel,
    loading,
    isUTP
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Cargando...</div>
      </div>
    );
  }

  if (!isUTP) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
          <p className="text-yellow-800 dark:text-yellow-200">
            Solo usuarios UTP pueden gestionar asignaciones de docentes.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Gestión de Asignaturas y Docentes
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Asigna docentes a las asignaturas en cada curso
        </p>
      </div>

      {/* Filtro por nivel */}
      <div className="mb-6 bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
        <div className="flex justify-between items-center mb-2">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Filtrar por Nivel Educativo
          </label>
          <span className="text-sm text-gray-500 dark:text-gray-400">
            {asignaturasFilteradas.length} de {asignaturas.length} asignaturas
          </span>
        </div>
        <select
          value={filtroNivel}
          onChange={(e) => setFiltroNivel(e.target.value)}
          className="w-full md:w-96 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
        >
          <option value="">Todos los niveles</option>
          {nivelesEducativos.map(nivel => (
            <option key={nivel.id} value={nivel.id}>{nivel.nombre}</option>
          ))}
        </select>
      </div>

      {/* Lista de asignaturas */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead className="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Asignatura
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Nivel Educativo
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Cursos Asignados
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Acciones
              </th>
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            {asignaturasFilteradas.map((asignatura) => {
              const cursosConAsignatura = cursos.filter(c => 
                c.asignaturas_asignadas?.some(ca => ca.asignatura === asignatura.id)
              );
              
              return (
                <tr key={asignatura.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                    {asignatura.nombre_asignatura}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {asignatura.nivel_educativo_nombre}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {cursosConAsignatura.length} curso(s)
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    {cursosConAsignatura.length > 0 ? (
                      <button
                        onClick={() => abrirModalAsignar(asignatura)}
                        className="inline-flex items-center px-3 py-1.5 bg-green-100 hover:bg-green-200 dark:bg-green-900/30 dark:hover:bg-green-900/50 text-green-700 dark:text-green-400 rounded-lg font-medium transition-colors"
                      >
                        <svg className="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                        </svg>
                        Asignar Docentes
                      </button>
                    ) : (
                      <span className="text-sm text-gray-400 dark:text-gray-500">
                        Sin cursos
                      </span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {asignaturasFilteradas.length === 0 && (
          <div className="text-center py-12 text-gray-500 dark:text-gray-400">
            No hay asignaturas disponibles
          </div>
        )}
      </div>

      {/* Modal Asignar Docentes */}
      {showAsignarModal && asignaturaSeleccionada && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-3xl w-full max-h-[80vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                  Asignar Docentes - {asignaturaSeleccionada.nombre_asignatura}
                </h3>
                <button
                  onClick={() => {
                    setShowAsignarModal(false);
                    setAsignaturaSeleccionada(null);
                  }}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div className="space-y-4">
                {cursoAsignaturas.length > 0 ? (
                  cursoAsignaturas.map((ca) => (
                    <div key={ca.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        {ca.curso_nombre}
                      </label>
                      <select
                        value={ca.docente || ''}
                        onChange={(e) => asignarDocente(ca.id, ca.curso_id, e.target.value || null)}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                      >
                        <option value="">Sin asignar</option>
                        {docentes.map((docente) => (
                          <option key={docente.id} value={docente.id}>
                            {docente.usuario_nombre} - {docente.especialidad}
                          </option>
                        ))}
                      </select>
                      {ca.docente_nombre && (
                        <p className="mt-1 text-sm text-green-600 dark:text-green-400">
                          ✓ Asignado: {ca.docente_nombre}
                        </p>
                      )}
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                    Esta asignatura no está asignada a ningún curso aún.
                  </div>
                )}
              </div>

              <div className="mt-6">
                <button
                  onClick={() => {
                    setShowAsignarModal(false);
                    setAsignaturaSeleccionada(null);
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

export default GestionAsignaturas;
