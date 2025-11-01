import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import axios from 'axios';

const PlanificacionForm = ({ planificacion, onSave }) => {
  const { token } = useAuth();
  const [formData, setFormData] = useState({
    titulo: '',
    tipo: 'CURSO',
    fecha_inicio: '',
    fecha_fin: '',
    objetivos: [],
    actividades: [],
    recursos: [],
  });

  useEffect(() => {
    if (planificacion) {
      setFormData({
        titulo: planificacion.titulo,
        tipo: planificacion.tipo,
        fecha_inicio: planificacion.fecha_inicio,
        fecha_fin: planificacion.fecha_fin,
        objetivos: planificacion.detalle ? planificacion.detalle.objetivos : [],
        actividades: planificacion.detalle ? planificacion.detalle.actividades : [],
        recursos: planificacion.detalle ? planificacion.detalle.recursos : [],
      });
    }
  }, [planificacion]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleArrayChange = (field, value) => {
    setFormData({ ...formData, [field]: value.split('\n') });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = {
        titulo: formData.titulo,
        tipo: formData.tipo,
        fecha_inicio: formData.fecha_inicio,
        fecha_fin: formData.fecha_fin,
      };
      let response;
      if (planificacion) {
        response = await axios.put(`/api/planificaciones/${planificacion.id}/`, data, {
          headers: { Authorization: `Bearer ${token}` },
        });
      } else {
        response = await axios.post('/api/planificaciones/', data, {
          headers: { Authorization: `Bearer ${token}` },
        });
      }
      // Save detalle
      const detalleData = {
        objetivos: formData.objetivos,
        actividades: formData.actividades,
        recursos: formData.recursos,
      };
      if (planificacion && planificacion.detalle) {
        await axios.put(`/api/planificaciones/${planificacion.id}/detalle/`, detalleData, {
          headers: { Authorization: `Bearer ${token}` },
        });
      } else {
        await axios.post(`/api/planificaciones/${response.data.id}/detalle/`, detalleData, {
          headers: { Authorization: `Bearer ${token}` },
        });
      }
      onSave();
    } catch (error) {
      console.error('Error saving planificacion', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        name="titulo"
        placeholder="Título"
        value={formData.titulo}
        onChange={handleChange}
        required
      />
      <select name="tipo" value={formData.tipo} onChange={handleChange}>
        <option value="CURSO">Curso</option>
        <option value="TALLER">Taller</option>
        <option value="SEMINARIO">Seminario</option>
      </select>
      <input
        type="date"
        name="fecha_inicio"
        value={formData.fecha_inicio}
        onChange={handleChange}
        required
      />
      <input
        type="date"
        name="fecha_fin"
        value={formData.fecha_fin}
        onChange={handleChange}
        required
      />
      <textarea
        placeholder="Objetivos (uno por línea)"
        value={formData.objetivos.join('\n')}
        onChange={(e) => handleArrayChange('objetivos', e.target.value)}
      />
      <textarea
        placeholder="Actividades (uno por línea)"
        value={formData.actividades.join('\n')}
        onChange={(e) => handleArrayChange('actividades', e.target.value)}
      />
      <textarea
        placeholder="Recursos (uno por línea)"
        value={formData.recursos.join('\n')}
        onChange={(e) => handleArrayChange('recursos', e.target.value)}
      />
      <button type="submit">{planificacion ? 'Actualizar' : 'Crear'} Planificación</button>
    </form>
  );
};

export default PlanificacionForm;