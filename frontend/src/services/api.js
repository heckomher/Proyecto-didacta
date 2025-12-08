import axios from 'axios';
import { useState } from 'react';

// Configuración base de axios
const API_BASE_URL = (import.meta.env.VITE_API_URL || '') + '/api';

// Crear instancia de axios con configuración base
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token automáticamente
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para manejar errores de autenticación
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expirado, intentar refresh
      const refreshToken = localStorage.getItem('refresh');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
            refresh: refreshToken,
          });
          const newToken = response.data.access;
          localStorage.setItem('token', newToken);
          // Reintentar petición original
          error.config.headers.Authorization = `Bearer ${newToken}`;
          return apiClient.request(error.config);
        } catch (refreshError) {
          // Refresh falló, limpiar tokens y redirigir a login
          localStorage.removeItem('token');
          localStorage.removeItem('refresh');
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

// Servicio base para CRUD operations
class BaseService {
  constructor(endpoint) {
    this.endpoint = endpoint;
  }

  async getAll(params = {}) {
    const response = await apiClient.get(this.endpoint, { params });
    return response.data;
  }

  async getById(id) {
    const response = await apiClient.get(`${this.endpoint}${id}/`);
    return response.data;
  }

  async create(data) {
    const response = await apiClient.post(this.endpoint, data);
    return response.data;
  }

  async update(id, data) {
    const response = await apiClient.put(`${this.endpoint}${id}/`, data);
    return response.data;
  }

  async partialUpdate(id, data) {
    const response = await apiClient.patch(`${this.endpoint}${id}/`, data);
    return response.data;
  }

  async delete(id) {
    await apiClient.delete(`${this.endpoint}${id}/`);
  }
}

// Servicios específicos para cada endpoint
export const authService = {
  async login(username, password) {
    const response = await apiClient.post('/auth/login/', { username, password });
    return response.data;
  },

  async register(userData) {
    const response = await apiClient.post('/auth/register/', userData);
    return response.data;
  },

  async logout() {
    await apiClient.post('/auth/logout/');
  },

  async getCurrentUser() {
    const response = await apiClient.get('/auth/user/');
    return response.data;
  },

  async refreshToken(refreshToken) {
    const response = await apiClient.post('/auth/refresh/', { refresh: refreshToken });
    return response.data;
  },
};

// Servicios para configuración académica
export const anioAcademicoService = {
  ...new BaseService('/anios-academicos/'),

  async getActivo() {
    const response = await apiClient.get('/anios-academicos/activo/');
    return response.data;
  },

  async getBorradores() {
    const response = await apiClient.get('/anios-academicos/borradores/');
    return response.data;
  },

  async activar(id) {
    const response = await apiClient.post(`/anios-academicos/${id}/activar/`);
    return response.data;
  },

  async cerrar(id, password) {
    const response = await apiClient.post(`/anios-academicos/${id}/cerrar/`, { password });
    return response.data;
  },
};

export const periodoAcademicoService = new BaseService('/periodos-academicos/');
export const feriadoService = new BaseService('/feriados/');
export const vacacionesService = new BaseService('/vacaciones/');

// Servicios para usuarios y roles
export const rolService = new BaseService('/roles/');
export const docenteService = new BaseService('/docentes/');
export const equipoDirectivoService = new BaseService('/equipo-directivo/');

// Servicios para estructura académica
export const nivelEducativoService = new BaseService('/niveles-educativos/');
export const asignaturaService = new BaseService('/asignaturas/');
export const cursoService = new BaseService('/cursos/');
export const objetivoAprendizajeService = new BaseService('/objetivos-aprendizaje/');
export const recursoPedagogicoService = new BaseService('/recursos-pedagogicos/');

// Servicios para planificaciones
export const planificacionService = {
  ...new BaseService('/planificaciones/'),

  async enviarAValidacion(id) {
    const response = await apiClient.post(`/planificaciones/${id}/enviar/`);
    return response.data;
  },

  async validar(id, accion, comentarios = '') {
    const response = await apiClient.post(`/planificaciones/${id}/validar/`, {
      accion,
      comentarios,
    });
    return response.data;
  },

  async getDetalle(id) {
    const response = await apiClient.get(`/planificaciones/${id}/detalle/`);
    return response.data;
  },

  async updateDetalle(id, data) {
    const response = await apiClient.put(`/planificaciones/${id}/detalle/`, data);
    return response.data;
  },
};

// Servicios para tipos específicos de planificación
export const planificacionAnualService = new BaseService('/planificaciones-anuales/');
export const planificacionUnidadService = new BaseService('/planificaciones-unidad/');
export const planificacionSemanalService = new BaseService('/planificaciones-semanales/');

// Servicios para eventos y calendario
export const eventoService = new BaseService('/eventos/');
export const calendarioService = new BaseService('/calendario/');

// Servicios utilitarios
export const utilService = {
  async verificarAnioAcademico() {
    const response = await apiClient.get('/verificar-anio-academico/');
    return response.data;
  },

  async verificarConfiguracionAcademica() {
    const response = await apiClient.get('/verificar-configuracion-academica/');
    return response.data;
  },
};

// Hook personalizado para manejar llamadas a la API con estado de carga
export const useApiCall = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = async (apiCall) => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiCall();
      return result;
    } catch (err) {
      setError(err.response?.data?.message || err.message || 'Error desconocido');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { loading, error, execute };
};

export default apiClient;