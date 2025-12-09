import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import axios from 'axios';

const DashboardUTP = () => {
  const { token } = useAuth();
  const navigate = useNavigate();
  const [planificaciones, setPlanificaciones] = useState([]);
  const [comentarios, setComentarios] = useState({});
  const [tieneAnioActivo, setTieneAnioActivo] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    verificarAnioAcademico();
  }, []);

  const verificarAnioAcademico = async () => {
    try {
      const response = await axios.get('http://localhost/api/verificar-anio-academico/');
      setTieneAnioActivo(response.data.tiene_anio_activo);
      if (!response.data.tiene_anio_activo) {
        // Redirigir a configuración académica si no hay año activo
        setTimeout(() => {
          navigate('/configuracion-academica');
        }, 3000);
      }
    } catch (error) {
      console.error('Error verificando año académico:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchPlanificaciones = useCallback(async () => {
    if (!tieneAnioActivo) return;
    
    try {
      const response = await axios.get('/api/planificaciones/', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setPlanificaciones(response.data);
    } catch (error) {
      console.error('Error fetching planificaciones', error);
    }
  }, [token, tieneAnioActivo]);

  useEffect(() => {
    if (tieneAnioActivo !== null) {
      fetchPlanificaciones();
    }
  }, [fetchPlanificaciones, tieneAnioActivo]);

  const handleValidar = async (id, accion) => {
    try {
      await axios.post(`/api/planificaciones/${id}/validar/`, { 
        accion, 
        comentarios: comentarios[id] || '' 
      }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchPlanificaciones();
      setComentarios(prev => ({ ...prev, [id]: '' }));
    } catch (error) {
      console.error('Error validando', error);
    }
  };

  const pendientes = planificaciones.filter(p => p.estado === 'PENDIENTE');
  const aprobadas = planificaciones.filter(p => p.estado === 'APROBADA');
  const rechazadas = planificaciones.filter(p => p.estado === 'RECHAZADA');

  const getStatusBadge = (estado) => {
    const badges = {
      BORRADOR: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
      PENDIENTE: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
      APROBADA: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
      RECHAZADA: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300',
    };
    return badges[estado] || badges.BORRADOR;
  };

  const PlanificacionCard = ({ p, showActions = false }) => (
    <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-5 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{p.titulo}</h3>
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusBadge(p.estado)}`}>
              {p.estado}
            </span>
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400 mb-2">
            <span className="font-medium">Autor:</span> {p.autor}
            {p.anio_academico_nombre && (
              <span className="ml-3">
                <span className="font-medium">Año:</span> {p.anio_academico_nombre}
              </span>
            )}
          </div>
          <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
            <span className="flex items-center">
              <svg className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              {new Date(p.fecha_inicio).toLocaleDateString()} - {new Date(p.fecha_fin).toLocaleDateString()}
            </span>
            <span className="flex items-center">
              <svg className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
              {p.tipo}
            </span>
          </div>
        </div>
      </div>
      
      {showActions && (
        <div className="mt-4 space-y-3">
          <textarea
            placeholder="Comentarios de validación (opcional)"
            value={comentarios[p.id] || ''}
            onChange={(e) => setComentarios(prev => ({ ...prev, [p.id]: e.target.value }))}
            className="input text-sm"
            rows="2"
          />
          <div className="flex gap-2">
            <button
              onClick={() => handleValidar(p.id, 'aprobar')}
              className="flex-1 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors inline-flex items-center justify-center"
            >
              <svg className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Aprobar
            </button>
            <button
              onClick={() => handleValidar(p.id, 'rechazar')}
              className="flex-1 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors inline-flex items-center justify-center"
            >
              <svg className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
              Rechazar
            </button>
          </div>
        </div>
      )}
    </div>
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Verificando configuración...</p>
        </div>
      </div>
    );
  }

  if (tieneAnioActivo === false) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border-2 border-yellow-400 dark:border-yellow-600 rounded-lg p-8 text-center">
          <div className="flex justify-center mb-4">
            <svg className="h-16 w-16 text-yellow-600 dark:text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-yellow-800 dark:text-yellow-200 mb-3">
            ⚠️ Configuración Requerida
          </h2>
          <p className="text-yellow-700 dark:text-yellow-300 mb-6 text-lg">
            No hay un año académico activo configurado. Debe crear y activar un año académico antes de gestionar planificaciones.
          </p>
          <p className="text-yellow-600 dark:text-yellow-400 mb-6">
            Será redirigido a la configuración académica en unos segundos...
          </p>
          <button
            onClick={() => navigate('/configuracion-academica')}
            className="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium inline-flex items-center gap-2"
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Ir a Configuración Académica
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white font-serif">Dashboard UTP</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">Gestión y validación de planificaciones académicas</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => navigate('/gestionar-usuarios')}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors inline-flex items-center"
          >
            <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            Gestionar Usuarios
          </button>
          <button
            onClick={() => navigate('/gestionar-cursos')}
            className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors inline-flex items-center"
          >
            <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            Gestionar Cursos
          </button>
          <button
            onClick={() => navigate('/historial-cursos')}
            className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium transition-colors inline-flex items-center"
          >
            <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
            </svg>
            Historial de Cursos
          </button>
          <button
            onClick={() => navigate('/configuracion-academica')}
            className="px-4 py-2 bg-secondary-600 hover:bg-secondary-700 text-white rounded-lg font-medium transition-colors inline-flex items-center"
          >
            <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Configuración Académica
          </button>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="card p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-yellow-100 dark:bg-yellow-900 rounded-lg p-3">
              <svg className="h-6 w-6 text-yellow-600 dark:text-yellow-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Pendientes</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{pendientes.length}</p>
            </div>
          </div>
        </div>
        <div className="card p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-green-100 dark:bg-green-900 rounded-lg p-3">
              <svg className="h-6 w-6 text-green-600 dark:text-green-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Aprobadas</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{aprobadas.length}</p>
            </div>
          </div>
        </div>
        <div className="card p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-red-100 dark:bg-red-900 rounded-lg p-3">
              <svg className="h-6 w-6 text-red-600 dark:text-red-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Rechazadas</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{rechazadas.length}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Pending Validations */}
      <div className="card p-6 mb-8">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
          <svg className="h-5 w-5 mr-2 text-yellow-600 dark:text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Planificaciones Pendientes de Validación
        </h2>
        
        {pendientes.length === 0 ? (
          <div className="text-center py-12">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">No hay planificaciones pendientes de validación</p>
          </div>
        ) : (
          <div className="space-y-4">
            {pendientes.map((p) => <PlanificacionCard key={p.id} p={p} showActions={true} />)}
          </div>
        )}
      </div>

      {/* Approved and Rejected in tabs */}
      <div className="card p-6">
        <div className="grid grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-semibold text-green-600 dark:text-green-400 mb-4 flex items-center">
              <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Aprobadas ({aprobadas.length})
            </h3>
            <div className="space-y-3">
              {aprobadas.length === 0 ? (
                <p className="text-sm text-gray-500 dark:text-gray-400">No hay planificaciones aprobadas</p>
              ) : (
                aprobadas.map(p => <PlanificacionCard key={p.id} p={p} />)
              )}
            </div>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-red-600 dark:text-red-400 mb-4 flex items-center">
              <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Rechazadas ({rechazadas.length})
            </h3>
            <div className="space-y-3">
              {rechazadas.length === 0 ? (
                <p className="text-sm text-gray-500 dark:text-gray-400">No hay planificaciones rechazadas</p>
              ) : (
                rechazadas.map(p => <PlanificacionCard key={p.id} p={p} />)
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardUTP;