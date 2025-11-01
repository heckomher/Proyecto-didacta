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

  return (
    <div>
      <h2>Dashboard Docente</h2>
      <button onClick={() => setShowForm(true)}>Crear Planificación</button>
      {showForm && (
        <PlanificacionForm planificacion={selectedPlanificacion} onSave={handleSave} />
      )}
      <ul>
        {planificaciones.map((p) => (
          <li key={p.id}>
            {p.titulo} - {p.estado}
            {p.estado === 'BORRADOR' && (
              <>
                <button onClick={() => { setSelectedPlanificacion(p); setShowForm(true); }}>Editar</button>
                <button onClick={() => handleEnviarValidacion(p.id)}>Enviar a Validación</button>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DashboardDocente;