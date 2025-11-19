import { useState, useEffect } from 'react';
import {
  anioAcademicoService,
  docenteService,
  cursoService,
  asignaturaService,
  nivelEducativoService,
  objetivoAprendizajeService,
  recursoPedagogicoService,
  planificacionService,
  planificacionAnualService,
  planificacionUnidadService,
  planificacionSemanalService,
} from '../services/api';

// Hook genérico para CRUD operations
export const useCrud = (service, initialLoad = true) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async (params = {}) => {
    try {
      setLoading(true);
      setError(null);
      const result = await service.getAll(params);
      setData(Array.isArray(result) ? result : result.results || []);
      return result;
    } catch (err) {
      setError(err.response?.data?.message || err.message || 'Error al cargar datos');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const create = async (itemData) => {
    try {
      setLoading(true);
      setError(null);
      const newItem = await service.create(itemData);
      setData(prev => [...prev, newItem]);
      return newItem;
    } catch (err) {
      setError(err.response?.data?.message || err.message || 'Error al crear');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const update = async (id, itemData) => {
    try {
      setLoading(true);
      setError(null);
      const updatedItem = await service.update(id, itemData);
      setData(prev => prev.map(item => item.id === id ? updatedItem : item));
      return updatedItem;
    } catch (err) {
      setError(err.response?.data?.message || err.message || 'Error al actualizar');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const remove = async (id) => {
    try {
      setLoading(true);
      setError(null);
      await service.delete(id);
      setData(prev => prev.filter(item => item.id !== id));
    } catch (err) {
      setError(err.response?.data?.message || err.message || 'Error al eliminar');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getById = async (id) => {
    try {
      setLoading(true);
      setError(null);
      const item = await service.getById(id);
      return item;
    } catch (err) {
      setError(err.response?.data?.message || err.message || 'Error al cargar item');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (initialLoad) {
      fetchData();
    }
  }, [initialLoad]);

  return {
    data,
    loading,
    error,
    fetchData,
    create,
    update,
    remove,
    getById,
    setData,
    setError,
  };
};

// Hook específico para años académicos
export const useAniosAcademicos = () => {
  const crud = useCrud(anioAcademicoService);
  const [anioActivo, setAnioActivo] = useState(null);

  const getAnioActivo = async () => {
    try {
      const activo = await anioAcademicoService.getActivo();
      setAnioActivo(activo);
      return activo;
    } catch (err) {
      if (err.response?.status !== 404) {
        throw err;
      }
      setAnioActivo(null);
    }
  };

  const activarAnio = async (id) => {
    try {
      const result = await anioAcademicoService.activar(id);
      await crud.fetchData(); // Recargar datos
      await getAnioActivo(); // Actualizar año activo
      return result;
    } catch (err) {
      throw err;
    }
  };

  const cerrarAnio = async (id, password) => {
    try {
      const result = await anioAcademicoService.cerrar(id, password);
      await crud.fetchData(); // Recargar datos
      return result;
    } catch (err) {
      throw err;
    }
  };

  useEffect(() => {
    getAnioActivo();
  }, []);

  return {
    ...crud,
    anioActivo,
    getAnioActivo,
    activarAnio,
    cerrarAnio,
  };
};

// Hook específico para docentes
export const useDocentes = () => {
  const crud = useCrud(docenteService);
  
  return {
    ...crud,
    docentes: crud.data,
  };
};

// Hook específico para cursos
export const useCursos = (nivelId = null) => {
  const crud = useCrud(cursoService, false);
  
  const fetchCursos = async () => {
    const params = nivelId ? { nivel: nivelId } : {};
    return await crud.fetchData(params);
  };

  useEffect(() => {
    fetchCursos();
  }, [nivelId]);

  return {
    ...crud,
    cursos: crud.data,
    fetchCursos,
  };
};

// Hook específico para asignaturas
export const useAsignaturas = () => {
  const crud = useCrud(asignaturaService);
  
  return {
    ...crud,
    asignaturas: crud.data,
  };
};

// Hook específico para niveles educativos
export const useNivelesEducativos = () => {
  const crud = useCrud(nivelEducativoService);
  
  return {
    ...crud,
    niveles: crud.data,
  };
};

// Hook específico para objetivos de aprendizaje
export const useObjetivosAprendizaje = (cursoId = null, nivelId = null) => {
  const crud = useCrud(objetivoAprendizajeService, false);
  
  const fetchObjetivos = async () => {
    const params = {};
    if (cursoId) params.curso = cursoId;
    if (nivelId) params.nivel_educativo = nivelId;
    return await crud.fetchData(params);
  };

  useEffect(() => {
    fetchObjetivos();
  }, [cursoId, nivelId]);

  return {
    ...crud,
    objetivos: crud.data,
    fetchObjetivos,
  };
};

// Hook específico para recursos pedagógicos
export const useRecursosPedagogicos = (tipo = null) => {
  const crud = useCrud(recursoPedagogicoService, false);
  
  const fetchRecursos = async () => {
    const params = tipo ? { tipo } : {};
    return await crud.fetchData(params);
  };

  useEffect(() => {
    fetchRecursos();
  }, [tipo]);

  return {
    ...crud,
    recursos: crud.data,
    fetchRecursos,
  };
};

// Hook específico para planificaciones
export const usePlanificaciones = () => {
  const crud = useCrud(planificacionService);
  
  const enviarAValidacion = async (id) => {
    try {
      await planificacionService.enviarAValidacion(id);
      await crud.fetchData(); // Recargar para ver cambio de estado
    } catch (err) {
      throw err;
    }
  };

  const validarPlanificacion = async (id, accion, comentarios = '') => {
    try {
      await planificacionService.validar(id, accion, comentarios);
      await crud.fetchData(); // Recargar para ver cambio de estado
    } catch (err) {
      throw err;
    }
  };

  const getDetalle = async (id) => {
    return await planificacionService.getDetalle(id);
  };

  const updateDetalle = async (id, data) => {
    return await planificacionService.updateDetalle(id, data);
  };

  return {
    ...crud,
    planificaciones: crud.data,
    enviarAValidacion,
    validarPlanificacion,
    getDetalle,
    updateDetalle,
  };
};

// Hook específico para planificaciones anuales
export const usePlanificacionesAnuales = () => {
  const crud = useCrud(planificacionAnualService);
  
  return {
    ...crud,
    planificacionesAnuales: crud.data,
  };
};

// Hook específico para planificaciones de unidad
export const usePlanificacionesUnidad = () => {
  const crud = useCrud(planificacionUnidadService);
  
  return {
    ...crud,
    planificacionesUnidad: crud.data,
  };
};

// Hook específico para planificaciones semanales
export const usePlanificacionesSemanales = () => {
  const crud = useCrud(planificacionSemanalService);
  
  return {
    ...crud,
    planificacionesSemanales: crud.data,
  };
};

// Hook para formularios de planificación
export const usePlanificacionForm = (tipo = 'ANUAL') => {
  const { anioActivo } = useAniosAcademicos();
  const { docentes } = useDocentes();
  const { cursos } = useCursos();
  const { asignaturas } = useAsignaturas();
  const { objetivos } = useObjetivosAprendizaje();
  const { recursos } = useRecursosPedagogicos();

  const [formData, setFormData] = useState({
    titulo: '',
    descripcion: '',
    tipo: tipo,
    fecha_inicio: '',
    fecha_fin: '',
    docente: '',
    curso: '',
    asignatura: '',
    objetivos_aprendizaje: [],
    recursos_pedagogicos: [],
  });

  // Auto-asignar año académico activo
  useEffect(() => {
    if (anioActivo) {
      setFormData(prev => ({
        ...prev,
        anio_academico: anioActivo.id,
      }));
    }
  }, [anioActivo]);

  const updateField = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const validateForm = () => {
    const errors = {};
    
    if (!formData.titulo) errors.titulo = 'El título es requerido';
    if (!formData.fecha_inicio) errors.fecha_inicio = 'La fecha de inicio es requerida';
    if (!formData.fecha_fin) errors.fecha_fin = 'La fecha de fin es requerida';
    if (!formData.docente) errors.docente = 'El docente es requerido';
    if (!formData.curso) errors.curso = 'El curso es requerido';
    if (!formData.asignatura) errors.asignatura = 'La asignatura es requerida';
    
    return {
      isValid: Object.keys(errors).length === 0,
      errors,
    };
  };

  return {
    formData,
    setFormData,
    updateField,
    validateForm,
    // Datos de selección
    anioActivo,
    docentes,
    cursos,
    asignaturas,
    objetivos,
    recursos,
  };
};