import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../hooks/useAuth';
import axios from 'axios';

const DashboardUTP = () => {
  const { token } = useAuth();
  const [planificaciones, setPlanificaciones] = useState([]);

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

  const handleValidar = async (id, accion, comentarios) => {
    try {
      await axios.post(`/api/planificaciones/${id}/validar/`, { accion, comentarios }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchPlanificaciones();
    } catch (error) {
      console.error('Error validando', error);
    }
  };

  return (
    <div>
      <h2>Dashboard UTP</h2>
      <h3>Planificaciones Pendientes</h3>
      <ul>
        {planificaciones.filter(p => p.estado === 'PENDIENTE').map((p) => (
          <li key={p.id}>
            {p.titulo} - {p.autor}
            <button onClick={() => handleValidar(p.id, 'aprobar')}>Aprobar</button>
            <button onClick={() => handleValidar(p.id, 'rechazar')}>Rechazar</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DashboardUTP;