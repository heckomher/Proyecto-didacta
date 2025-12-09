import { useState, useEffect } from 'react';
import axios from 'axios';
import { useTheme } from '../contexts/ThemeContext';
import { useNavigate } from 'react-router-dom';

const ConfiguracionAcademica = () => {
  const { theme } = useTheme();
  const navigate = useNavigate();
  const [aniosAcademicos, setAniosAcademicos] = useState([]);
  const [anioActivo, setAnioActivo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showNuevoAnio, setShowNuevoAnio] = useState(false);
  const [showPeriodoForm, setShowPeriodoForm] = useState(false);
  const [showFeriadoForm, setShowFeriadoForm] = useState(false);
  const [showVacacionForm, setShowVacacionForm] = useState(false);
  const [showConfirmarCierre, setShowConfirmarCierre] = useState(false);
  const [anioACerrar, setAnioACerrar] = useState(null);
  const [passwordCierre, setPasswordCierre] = useState('');
  const [errorPassword, setErrorPassword] = useState('');

  const [nuevoAnio, setNuevoAnio] = useState({
    nombre: new Date().getFullYear().toString(),
    fecha_inicio: '',
    fecha_fin: '',
    tipo_periodo: 'SEMESTRE'
  });

  const [nuevoPeriodo, setNuevoPeriodo] = useState({
    nombre: '',
    numero: 1,
    fecha_inicio: '',
    fecha_fin: '',
    anio_academico: null
  });

  const [nuevoFeriado, setNuevoFeriado] = useState({
    nombre: '',
    fecha: '',
    tipo: 'FERIADO',
    anio_academico: null
  });

  const [nuevaVacacion, setNuevaVacacion] = useState({
    nombre: '',
    fecha_inicio: '',
    fecha_fin: '',
    tipo: 'INVIERNO',
    anio_academico: null
  });

  // Helper para obtener headers con token
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
      const config = getAuthHeaders();

      const [aniosRes, activoRes] = await Promise.all([
        axios.get('/api/anios-academicos/', config),
        axios.get('/api/anios-academicos/activo/', config).catch(() => ({ data: null }))
      ]);
      setAniosAcademicos(aniosRes.data);
      setAnioActivo(activoRes.data);
    } catch (error) {
      console.error('Error cargando datos:', error);
      if (error.response?.status === 404) {
        setAnioActivo(null);
      }
    } finally {
      setLoading(false);
    }
  };

  const crearAnioAcademico = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/anios-academicos/', {
        ...nuevoAnio,
        estado: 'BORRADOR'
      }, getAuthHeaders());
      setShowNuevoAnio(false);
      setNuevoAnio({
        nombre: new Date().getFullYear().toString(),
        fecha_inicio: '',
        fecha_fin: '',
        tipo_periodo: 'SEMESTRE'
      });
      cargarDatos();
      alert('Año académico creado en borrador. Actívelo para poder usarlo.');
    } catch (error) {
      console.error('Error creando año académico:', error);
      alert('Error al crear año académico: ' + (error.response?.data?.detail || error.message));
    }
  };

  const crearPeriodo = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/periodos-academicos/', nuevoPeriodo, getAuthHeaders());
      setShowPeriodoForm(false);
      setNuevoPeriodo({
        nombre: '',
        numero: 1,
        fecha_inicio: '',
        fecha_fin: '',
        anio_academico: null
      });
      cargarDatos();
    } catch (error) {
      console.error('Error creando periodo:', error);
      alert('Error al crear periodo: ' + (error.response?.data?.detail || error.message));
    }
  };

  const crearFeriado = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/feriados/', nuevoFeriado, getAuthHeaders());
      setShowFeriadoForm(false);
      setNuevoFeriado({
        nombre: '',
        fecha: '',
        tipo: 'FERIADO',
        anio_academico: null
      });
      cargarDatos();
    } catch (error) {
      console.error('Error creando feriado:', error);
      alert('Error al crear feriado: ' + (error.response?.data?.detail || error.message));
    }
  };

  const crearVacacion = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/vacaciones/', nuevaVacacion, getAuthHeaders());
      setShowVacacionForm(false);
      setNuevaVacacion({
        nombre: '',
        fecha_inicio: '',
        fecha_fin: '',
        tipo: 'INVIERNO',
        anio_academico: null
      });
      cargarDatos();
    } catch (error) {
      console.error('Error creando vacación:', error);
      alert('Error al crear vacación: ' + (error.response?.data?.detail || error.message));
    }
  };

  const eliminarItem = async (tipo, id) => {
    if (!confirm('¿Está seguro de eliminar este elemento?')) return;

    try {
      const endpoints = {
        periodo: 'periodos-academicos',
        feriado: 'feriados',
        vacacion: 'vacaciones'
      };
      await axios.delete(`/api/${endpoints[tipo]}/${id}/`, getAuthHeaders());
      cargarDatos();
    } catch (error) {
      console.error('Error eliminando:', error);
      const mensaje = error.response?.data?.detail || error.response?.data?.[0] || error.message;
      alert('Error al eliminar: ' + mensaje);
    }
  };

  const activarAnioAcademico = async (id) => {
    if (!confirm('¿Está seguro de activar este año académico? Se desactivará el año activo actual (si existe).')) {
      return;
    }
    try {
      await axios.post(`/api/anios-academicos/${id}/activar/`, {}, getAuthHeaders());
      cargarDatos();
      alert('Año académico activado exitosamente.');
    } catch (error) {
      console.error('Error activando año:', error);
      alert('Error al activar año académico: ' + (error.response?.data?.detail || error.message));
    }
  };

  const cerrarAnioAcademico = async (id) => {
    if (!confirm('¿Está seguro de cerrar este año académico? Una vez cerrado no se podrá modificar.')) return;

    // Abrir modal de confirmación con contraseña
    setAnioACerrar(id);
    setShowConfirmarCierre(true);
    setPasswordCierre('');
    setErrorPassword('');
  };

  const confirmarCierreConPassword = async (e) => {
    e.preventDefault();
    setErrorPassword('');

    try {
      // Verificar contraseña del usuario actual
      const { data: user } = await axios.get('/api/auth/user/');

      // Intentar login para validar la contraseña
      try {
        await axios.post('/api/auth/login/', {
          username: user.username,
          password: passwordCierre
        });
      } catch (error) {
        setErrorPassword('Contraseña incorrecta');
        return;
      }

      // Si la contraseña es correcta, cerrar el año
      await axios.post(`/api/anios-academicos/${anioACerrar}/cerrar/`);
      setShowConfirmarCierre(false);
      setPasswordCierre('');
      setAnioACerrar(null);
      cargarDatos();
      alert('Año académico cerrado exitosamente. Ahora es de solo lectura.');
    } catch (error) {
      console.error('Error cerrando año:', error);
      const mensaje = error.response?.data?.detail || error.message;
      alert('Error al cerrar año académico: ' + mensaje);
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
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-primary-800 dark:text-primary-200">
          Configuración Académica
        </h1>
        <button
          onClick={() => navigate('/')}
          className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg font-medium transition-colors inline-flex items-center"
        >
          <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Volver al Dashboard
        </button>
      </div>

      {/* Año Académico Activo */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-200">
            Año Académico Activo
          </h2>
          <button
            onClick={() => setShowNuevoAnio(true)}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition"
          >
            Crear Nuevo Año
          </button>
        </div>

        {anioActivo ? (
          <div className="border border-primary-200 dark:border-primary-700 rounded-lg p-4 bg-primary-50 dark:bg-primary-900/20">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-lg font-semibold text-primary-800 dark:text-primary-200">
                  {anioActivo.nombre}
                  {anioActivo.cerrado && (
                    <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-500 text-white">
                      🔒 Cerrado
                    </span>
                  )}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                  <span className="font-medium">Inicio:</span> {anioActivo.fecha_inicio} |
                  <span className="font-medium ml-2">Fin:</span> {anioActivo.fecha_fin}
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  <span className="font-medium">Tipo:</span> {anioActivo.tipo_periodo}
                </p>
              </div>
              {!anioActivo.cerrado && (
                <button
                  onClick={() => cerrarAnioAcademico(anioActivo.id)}
                  className="px-3 py-2 bg-gray-600 hover:bg-gray-700 text-white text-sm rounded-lg transition inline-flex items-center"
                  title="Cerrar año académico (solo lectura)"
                >
                  <svg className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                  Cerrar Año
                </button>
              )}
            </div>

            {anioActivo.cerrado && (
              <div className="mb-4 p-3 bg-yellow-100 dark:bg-yellow-900/30 border border-yellow-300 dark:border-yellow-700 rounded-lg">
                <p className="text-sm text-yellow-800 dark:text-yellow-200">
                  ⚠️ Este año académico está cerrado. No se pueden realizar modificaciones. Los datos se mantienen para consulta histórica.
                </p>
              </div>
            )}

            {/* Periodos */}
            <div className="mt-4">
              <div className="flex justify-between items-center mb-2">
                <h4 className="font-semibold text-gray-700 dark:text-gray-300">Periodos</h4>
                {!anioActivo.cerrado && (
                  <button
                    onClick={() => {
                      setNuevoPeriodo({ ...nuevoPeriodo, anio_academico: anioActivo.id });
                      setShowPeriodoForm(true);
                    }}
                    className="text-sm px-3 py-1 bg-secondary-600 text-white rounded hover:bg-secondary-700"
                  >
                    + Agregar Periodo
                  </button>
                )}
              </div>
              {anioActivo.periodos?.length > 0 ? (
                <div className="space-y-2">
                  {anioActivo.periodos.map((periodo) => (
                    <div key={periodo.id} className="flex justify-between items-center bg-white dark:bg-gray-700 p-3 rounded">
                      <div>
                        <span className="font-medium text-gray-900 dark:text-gray-100">{periodo.nombre}</span>
                        <span className="text-sm text-gray-600 dark:text-gray-400 ml-2">
                          ({periodo.fecha_inicio} - {periodo.fecha_fin})
                        </span>
                      </div>
                      {!anioActivo.cerrado && (
                        <button
                          onClick={() => eliminarItem('periodo', periodo.id)}
                          className="inline-flex items-center px-2.5 py-1 bg-red-100 hover:bg-red-200 dark:bg-red-900/30 dark:hover:bg-red-900/50 text-red-700 dark:text-red-400 rounded text-xs font-medium transition-colors"
                        >
                          <svg className="h-3.5 w-3.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                          Eliminar
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-500 dark:text-gray-400 italic">No hay periodos definidos</p>
              )}
            </div>

            {/* Feriados */}
            <div className="mt-4">
              <div className="flex justify-between items-center mb-2">
                <h4 className="font-semibold text-gray-700 dark:text-gray-300">Feriados</h4>
                {!anioActivo.cerrado && (
                  <button
                    onClick={() => {
                      setNuevoFeriado({ ...nuevoFeriado, anio_academico: anioActivo.id });
                      setShowFeriadoForm(true);
                    }}
                    className="text-sm px-3 py-1 bg-secondary-600 text-white rounded hover:bg-secondary-700"
                  >
                    + Agregar Feriado
                  </button>
                )}
              </div>
              {anioActivo.feriados?.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {anioActivo.feriados.map((feriado) => (
                    <div key={feriado.id} className="flex justify-between items-center bg-white dark:bg-gray-700 p-2 rounded text-sm">
                      <div>
                        <span className="font-medium text-gray-900 dark:text-gray-100">{feriado.nombre}</span>
                        <span className="text-gray-600 dark:text-gray-400 ml-2">({feriado.fecha})</span>
                      </div>
                      {!anioActivo.cerrado && (
                        <button
                          onClick={() => eliminarItem('feriado', feriado.id)}
                          className="inline-flex items-center px-2.5 py-1 bg-red-100 hover:bg-red-200 dark:bg-red-900/30 dark:hover:bg-red-900/50 text-red-700 dark:text-red-400 rounded text-xs font-medium transition-colors"
                        >
                          <svg className="h-3.5 w-3.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                          Eliminar
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-500 dark:text-gray-400 italic">No hay feriados definidos</p>
              )}
            </div>

            {/* Vacaciones */}
            <div className="mt-4">
              <div className="flex justify-between items-center mb-2">
                <h4 className="font-semibold text-gray-700 dark:text-gray-300">Vacaciones</h4>
                {!anioActivo.cerrado && (
                  <button
                    onClick={() => {
                      setNuevaVacacion({ ...nuevaVacacion, anio_academico: anioActivo.id });
                      setShowVacacionForm(true);
                    }}
                    className="text-sm px-3 py-1 bg-secondary-600 text-white rounded hover:bg-secondary-700"
                  >
                    + Agregar Vacaciones
                  </button>
                )}
              </div>
              {anioActivo.vacaciones?.length > 0 ? (
                <div className="space-y-2">
                  {anioActivo.vacaciones.map((vacacion) => (
                    <div key={vacacion.id} className="flex justify-between items-center bg-white dark:bg-gray-700 p-3 rounded">
                      <div>
                        <span className="font-medium text-gray-900 dark:text-gray-100">{vacacion.nombre}</span>
                        <span className="text-sm text-gray-600 dark:text-gray-400 ml-2">
                          ({vacacion.fecha_inicio} - {vacacion.fecha_fin})
                        </span>
                      </div>
                      {!anioActivo.cerrado && (
                        <button
                          onClick={() => eliminarItem('vacacion', vacacion.id)}
                          className="inline-flex items-center px-2.5 py-1 bg-red-100 hover:bg-red-200 dark:bg-red-900/30 dark:hover:bg-red-900/50 text-red-700 dark:text-red-400 rounded text-xs font-medium transition-colors"
                        >
                          <svg className="h-3.5 w-3.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                          Eliminar
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-500 dark:text-gray-400 italic">No hay vacaciones definidas</p>
              )}
            </div>
          </div>
        ) : (
          <p className="text-gray-500 italic">No hay año académico activo. Cree uno nuevo.</p>
        )}
      </div>

      {/* Años Académicos en Borrador */}
      {aniosAcademicos && aniosAcademicos.filter(a => a.estado === 'BORRADOR').length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-4">
            Años Académicos en Borrador
          </h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
            Configure los periodos, feriados y vacaciones, luego active el año para poder usarlo en el sistema.
          </p>
          <div className="space-y-4">
            {aniosAcademicos.filter(a => a.estado === 'BORRADOR').map((anio) => (
              <div key={anio.id} className="border border-blue-300 dark:border-blue-600 rounded-lg p-4 bg-blue-50 dark:bg-blue-900/20">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-800 dark:text-gray-200 flex items-center gap-2">
                      {anio.nombre}
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-500 text-white">
                        📝 Borrador
                      </span>
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                      {anio.fecha_inicio} - {anio.fecha_fin} | {anio.tipo_periodo}
                    </p>
                  </div>
                  <button
                    onClick={() => activarAnioAcademico(anio.id)}
                    className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm rounded-lg transition inline-flex items-center gap-2"
                  >
                    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Activar
                  </button>
                </div>

                {/* Periodos del año en borrador */}
                <div className="mt-3 bg-white dark:bg-gray-700 rounded p-3">
                  <div className="flex justify-between items-center mb-2">
                    <h4 className="font-medium text-gray-700 dark:text-gray-300 text-sm">Periodos</h4>
                    <button
                      onClick={() => {
                        setNuevoPeriodo({ ...nuevoPeriodo, anio_academico: anio.id });
                        setShowPeriodoForm(true);
                      }}
                      className="text-xs px-2 py-1 bg-secondary-600 text-white rounded hover:bg-secondary-700"
                    >
                      + Agregar
                    </button>
                  </div>
                  {anio.periodos?.length > 0 ? (
                    <div className="space-y-1">
                      {anio.periodos.map((periodo) => (
                        <div key={periodo.id} className="flex justify-between items-center text-sm">
                          <span className="text-gray-800 dark:text-gray-200">{periodo.nombre} ({periodo.fecha_inicio} - {periodo.fecha_fin})</span>
                            <button
                            onClick={() => eliminarItem('periodo', periodo.id)}
                            className="inline-flex items-center px-2 py-0.5 bg-red-100 hover:bg-red-200 dark:bg-red-900/30 dark:hover:bg-red-900/50 text-red-700 dark:text-red-400 rounded text-xs font-medium transition-colors"
                            >
                              <svg className="h-3 w-3 mr-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                              </svg>
                              Eliminar
                            </button>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs text-gray-500 dark:text-gray-400 italic">Sin periodos</p>
                  )}
                </div>

                {/* Feriados del año en borrador */}
                <div className="mt-2 bg-white dark:bg-gray-700 rounded p-3">
                  <div className="flex justify-between items-center mb-2">
                    <h4 className="font-medium text-gray-700 dark:text-gray-300 text-sm">Feriados</h4>
                    <button
                      onClick={() => {
                        setNuevoFeriado({ ...nuevoFeriado, anio_academico: anio.id });
                        setShowFeriadoForm(true);
                      }}
                      className="text-xs px-2 py-1 bg-secondary-600 text-white rounded hover:bg-secondary-700"
                    >
                      + Agregar
                    </button>
                  </div>
                  {anio.feriados?.length > 0 ? (
                    <div className="grid grid-cols-2 gap-1">
                      {anio.feriados.map((feriado) => (
                        <div key={feriado.id} className="flex justify-between items-center text-xs">
                          <span className="text-gray-800 dark:text-gray-200">{feriado.nombre} ({feriado.fecha})</span>
                          <button
                            onClick={() => eliminarItem('feriado', feriado.id)}
                            className="text-red-600 hover:text-red-800 text-xs"
                          >
                            ×
                          </button>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs text-gray-500 dark:text-gray-400 italic">Sin feriados</p>
                  )}
                </div>

                {/* Vacaciones del año en borrador */}
                <div className="mt-2 bg-white dark:bg-gray-700 rounded p-3">
                  <div className="flex justify-between items-center mb-2">
                    <h4 className="font-medium text-gray-700 dark:text-gray-300 text-sm">Vacaciones</h4>
                    <button
                      onClick={() => {
                        setNuevaVacacion({ ...nuevaVacacion, anio_academico: anio.id });
                        setShowVacacionForm(true);
                      }}
                      className="text-xs px-2 py-1 bg-secondary-600 text-white rounded hover:bg-secondary-700"
                    >
                      + Agregar
                    </button>
                  </div>
                  {anio.vacaciones?.length > 0 ? (
                    <div className="space-y-1">
                      {anio.vacaciones.map((vacacion) => (
                        <div key={vacacion.id} className="flex justify-between items-center text-sm">
                          <span className="text-gray-800 dark:text-gray-200">{vacacion.nombre} ({vacacion.fecha_inicio} - {vacacion.fecha_fin})</span>
                            <button
                            onClick={() => eliminarItem('vacacion', vacacion.id)}
                            className="inline-flex items-center px-2 py-0.5 bg-red-100 hover:bg-red-200 dark:bg-red-900/30 dark:hover:bg-red-900/50 text-red-700 dark:text-red-400 rounded text-xs font-medium transition-colors"
                            >
                              <svg className="h-3 w-3 mr-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                              </svg>
                              Eliminar
                            </button>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs text-gray-500 dark:text-gray-400 italic">Sin vacaciones</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Historial de Años Académicos Cerrados */}
      {aniosAcademicos.filter(a => a.cerrado).length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-4">
            Historial de Años Académicos (Solo Lectura)
          </h2>
          <div className="space-y-3">
            {aniosAcademicos.filter(a => a.cerrado).map((anio) => (
              <div key={anio.id} className="border border-gray-300 dark:border-gray-600 rounded-lg p-4 bg-gray-50 dark:bg-gray-700/50">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-gray-800 dark:text-gray-200 flex items-center gap-2">
                      {anio.nombre}
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-500 text-white">
                        🔒 Cerrado
                      </span>
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                      {anio.fecha_inicio} - {anio.fecha_fin} | {anio.tipo_periodo}
                    </p>
                    <div className="mt-2 text-sm">
                      <span className="text-gray-600 dark:text-gray-400">
                        Periodos: {anio.periodos?.length || 0} |
                        Feriados: {anio.feriados?.length || 0} |
                        Vacaciones: {anio.vacaciones?.length || 0}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Modal Nuevo Año */}
      {showNuevoAnio && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-gray-100">Crear Año Académico</h3>
            <form onSubmit={crearAnioAcademico}>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Nombre (Año)</label>
                <input
                  type="text"
                  value={nuevoAnio.nombre}
                  onChange={(e) => setNuevoAnio({ ...nuevoAnio, nombre: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Fecha Inicio</label>
                <input
                  type="date"
                  value={nuevoAnio.fecha_inicio}
                  onChange={(e) => setNuevoAnio({ ...nuevoAnio, fecha_inicio: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Fecha Fin</label>
                <input
                  type="date"
                  value={nuevoAnio.fecha_fin}
                  onChange={(e) => setNuevoAnio({ ...nuevoAnio, fecha_fin: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Tipo de Periodo</label>
                <select
                  value={nuevoAnio.tipo_periodo}
                  onChange={(e) => setNuevoAnio({ ...nuevoAnio, tipo_periodo: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                >
                  <option value="SEMESTRE">Semestre</option>
                  <option value="TRIMESTRE">Trimestre</option>
                  <option value="ANUAL">Anual</option>
                </select>
              </div>
              <div className="flex gap-2">
                <button type="submit" className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">
                  Crear
                </button>
                <button
                  type="button"
                  onClick={() => setShowNuevoAnio(false)}
                  className="flex-1 px-4 py-2 bg-gray-300 dark:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal Nuevo Periodo */}
      {showPeriodoForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-gray-100">Agregar Periodo</h3>
            <form onSubmit={crearPeriodo}>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Nombre</label>
                <input
                  type="text"
                  value={nuevoPeriodo.nombre}
                  onChange={(e) => setNuevoPeriodo({ ...nuevoPeriodo, nombre: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  required
                  placeholder="Ej: Primer Semestre"
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Número</label>
                <input
                  type="number"
                  value={nuevoPeriodo.numero}
                  onChange={(e) => setNuevoPeriodo({ ...nuevoPeriodo, numero: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  required
                  min="1"
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Fecha Inicio</label>
                <input
                  type="date"
                  value={nuevoPeriodo.fecha_inicio}
                  onChange={(e) => setNuevoPeriodo({ ...nuevoPeriodo, fecha_inicio: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Fecha Fin</label>
                <input
                  type="date"
                  value={nuevoPeriodo.fecha_fin}
                  onChange={(e) => setNuevoPeriodo({ ...nuevoPeriodo, fecha_fin: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  required
                />
              </div>
              <div className="flex gap-2">
                <button type="submit" className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">
                  Agregar
                </button>
                <button
                  type="button"
                  onClick={() => setShowPeriodoForm(false)}
                  className="flex-1 px-4 py-2 bg-gray-300 dark:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal Nuevo Feriado */}
      {showFeriadoForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-gray-100">Agregar Feriado</h3>
            <form onSubmit={crearFeriado}>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Nombre</label>
                <input
                  type="text"
                  value={nuevoFeriado.nombre}
                  onChange={(e) => setNuevoFeriado({ ...nuevoFeriado, nombre: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Fecha</label>
                <input
                  type="date"
                  value={nuevoFeriado.fecha}
                  onChange={(e) => setNuevoFeriado({ ...nuevoFeriado, fecha: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Tipo</label>
                <select
                  value={nuevoFeriado.tipo}
                  onChange={(e) => setNuevoFeriado({ ...nuevoFeriado, tipo: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                >
                  <option value="FERIADO">Feriado Nacional</option>
                  <option value="INSTITUCIONAL">Día Institucional</option>
                  <option value="RECESO">Receso Académico</option>
                </select>
              </div>
              <div className="flex gap-2">
                <button type="submit" className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">
                  Agregar
                </button>
                <button
                  type="button"
                  onClick={() => setShowFeriadoForm(false)}
                  className="flex-1 px-4 py-2 bg-gray-300 dark:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal Nueva Vacación */}
      {showVacacionForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-gray-100">Agregar Vacaciones</h3>
            <form onSubmit={crearVacacion}>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Nombre</label>
                <input
                  type="text"
                  value={nuevaVacacion.nombre}
                  onChange={(e) => setNuevaVacacion({ ...nuevaVacacion, nombre: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Fecha Inicio</label>
                <input
                  type="date"
                  value={nuevaVacacion.fecha_inicio}
                  onChange={(e) => setNuevaVacacion({ ...nuevaVacacion, fecha_inicio: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Fecha Fin</label>
                <input
                  type="date"
                  value={nuevaVacacion.fecha_fin}
                  onChange={(e) => setNuevaVacacion({ ...nuevaVacacion, fecha_fin: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Tipo</label>
                <select
                  value={nuevaVacacion.tipo}
                  onChange={(e) => setNuevaVacacion({ ...nuevaVacacion, tipo: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                >
                  <option value="INVIERNO">Invierno</option>
                  <option value="VERANO">Verano</option>
                  <option value="RECESO">Receso</option>
                </select>
              </div>
              <div className="flex gap-2">
                <button type="submit" className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">
                  Agregar
                </button>
                <button
                  type="button"
                  onClick={() => setShowVacacionForm(false)}
                  className="flex-1 px-4 py-2 bg-gray-300 dark:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal Confirmar Cierre con Contraseña */}
      {showConfirmarCierre && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4 border-2 border-red-500">
            <div className="flex items-center gap-3 mb-4">
              <div className="flex-shrink-0 w-12 h-12 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center">
                <svg className="h-6 w-6 text-red-600 dark:text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div>
                <h3 className="text-xl font-semibold text-red-600 dark:text-red-400">⚠️ Acción Irreversible</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Confirme con su contraseña</p>
              </div>
            </div>

            <div className="mb-4 p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-300 dark:border-yellow-700 rounded-lg">
              <p className="text-sm text-yellow-800 dark:text-yellow-200 font-medium mb-2">
                ⚠️ Está a punto de cerrar el año académico permanentemente.
              </p>
              <ul className="text-sm text-yellow-700 dark:text-yellow-300 space-y-1 ml-4 list-disc">
                <li>No podrá agregar, modificar o eliminar periodos</li>
                <li>No podrá agregar, modificar o eliminar feriados</li>
                <li>No podrá agregar, modificar o eliminar vacaciones</li>
                <li>El año quedará como registro histórico de solo lectura</li>
                <li><strong>Esta acción NO se puede revertir</strong></li>
              </ul>
            </div>

            <form onSubmit={confirmarCierreConPassword}>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                  Ingrese su contraseña para confirmar:
                </label>
                <input
                  type="password"
                  value={passwordCierre}
                  onChange={(e) => {
                    setPasswordCierre(e.target.value);
                    setErrorPassword('');
                  }}
                  className="w-full px-3 py-2 border rounded-lg dark:bg-gray-700 focus:ring-2 focus:ring-red-500 focus:border-red-500"
                  placeholder="Ingrese su contraseña"
                  required
                  autoFocus
                />
                {errorPassword && (
                  <p className="mt-2 text-sm text-red-600 dark:text-red-400 flex items-center gap-1">
                    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {errorPassword}
                  </p>
                )}
              </div>

              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => {
                    setShowConfirmarCierre(false);
                    setPasswordCierre('');
                    setAnioACerrar(null);
                    setErrorPassword('');
                  }}
                  className="flex-1 px-4 py-2 bg-gray-300 dark:bg-gray-600 rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500 font-medium"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-medium inline-flex items-center justify-center gap-2"
                >
                  <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                  Cerrar Año Definitivamente
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ConfiguracionAcademica;
