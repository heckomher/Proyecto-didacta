import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../hooks/useAuth';
import axios from 'axios';
import PlanificacionForm from './PlanificacionForm';

const DashboardDocente = () => {
  const { token } = useAuth();
  const [planificaciones, setPlanificaciones] = useState([]);
  const [selectedPlanificacion, setSelectedPlanificacion] = useState(null);
  const [showForm, setShowForm] = useState(false);

  const fetchPlanificaciones = useCallback(async () => {
    try {
      const response = await axios.get('/api/planificaciones/', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setPlanificaciones(response.data);
    } catch (error) {
      console.error('Error fetching planificaciones', error);
    }
  }, [token]);

  useEffect(() => {
    fetchPlanificaciones();
  }, [fetchPlanificaciones]);

  const handleEnviarValidacion = async (id) => {
    try {
      await axios.post(`/api/planificaciones/${id}/enviar/`, {}, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchPlanificaciones();
    } catch (error) {
      console.error('Error enviando a validación', error);
    }
  };

  const handleSave = () => {
    setShowForm(false);
    setSelectedPlanificacion(null);
    fetchPlanificaciones();
  };

  const getStatusBadge = (estado) => {
    const badges = {
      BORRADOR: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
      PENDIENTE: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
      APROBADA: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
      RECHAZADA: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300',
    };
    return badges[estado] || badges.BORRADOR;
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white font-serif">Dashboard Docente</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">Gestione sus planificaciones académicas</p>
      </div>

      <div className="mb-6">
        <button
          onClick={() => setShowForm(true)}
          className="btn-primary inline-flex items-center"
        >
          <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Nueva Planificación
        </button>
      </div>

      {showForm && (
        <PlanificacionForm 
          planificacion={selectedPlanificacion} 
          onSave={handleSave}
          onCancel={() => {
            setShowForm(false);
            setSelectedPlanificacion(null);
          }}
        />
      )}

      <div className="grid gap-6">
        <div className="card p-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Mis Planificaciones</h2>
          
          {planificaciones.length === 0 ? (
            <div className="text-center py-12">
              <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">No hay planificaciones aún</p>
              <button onClick={() => setShowForm(true)} className="mt-4 text-primary-600 dark:text-primary-400 hover:underline">
                Crear su primera planificación
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {planificaciones.map((p) => (
                <div key={p.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{p.titulo}</h3>
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusBadge(p.estado)}`}>
                          {p.estado}
                        </span>
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
                    <div className="flex gap-2">
                      {p.estado === 'BORRADOR' && (
                        <>
                          <button
                            onClick={() => { setSelectedPlanificacion(p); setShowForm(true); }}
                            className="btn-secondary text-sm"
                          >
                            Editar
                          </button>
                          <button
                            onClick={() => handleEnviarValidacion(p.id)}
                            className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                          >
                            Enviar a Validación
                          </button>
                        </>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DashboardDocente;