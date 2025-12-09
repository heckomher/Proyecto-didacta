import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import axios from 'axios';

const PlanificacionForm = ({ planificacion, onSave, onCancel }) => {
  const { token } = useAuth();
  const [formData, setFormData] = useState({
    titulo: '',
    tipo: 'ANUAL',
    fecha_inicio: '',
    fecha_fin: '',
    objetivos: [],
    actividades: [],
    recursos: [],
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

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
    setError('');
  };

  const handleArrayChange = (field, value) => {
    setFormData({ ...formData, [field]: value.split('\n').filter(item => item.trim()) });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    
    try {
      const data = {
        titulo: formData.titulo,
        tipo: formData.tipo,
        fecha_inicio: formData.fecha_inicio,
        fecha_fin: formData.fecha_fin,
      };
      
      let response;
      if (planificacion) {
        response = await axios.put(`/planificaciones/${planificacion.id}/`, data, {
          headers: { Authorization: `Bearer ${token}` },
        });
      } else {
        response = await axios.post('/planificaciones/', data, {
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
      } else if (response.data.id) {
        // Para crear un nuevo detalle, usar PUT en lugar de POST
        await axios.put(`/api/planificaciones/${response.data.id}/detalle/`, detalleData, {
          headers: { Authorization: `Bearer ${token}` },
        });
      }
      
      onSave();
    } catch (error) {
      console.error('Error saving planificacion', error);
      setError('Error al guardar la planificación. Por favor, intenta de nuevo.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="card max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white font-serif">
              {planificacion ? 'Editar Planificación' : 'Nueva Planificación'}
            </h2>
            <button
              onClick={onCancel}
              className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
              <div className="flex items-center">
                <svg className="h-5 w-5 text-red-400 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p className="text-sm text-red-800 dark:text-red-200">{error}</p>
              </div>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Basic Information */}
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Título de la Planificación
                </label>
                <input
                  type="text"
                  name="titulo"
                  placeholder="ej. Programación Avanzada 2024"
                  value={formData.titulo}
                  onChange={handleChange}
                  className="input"
                  required
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Tipo
                  </label>
                  <select 
                    name="tipo" 
                    value={formData.tipo} 
                    onChange={handleChange}
                    className="input"
                  >
                    <option value="CURSO">Curso</option>
                    <option value="TALLER">Taller</option>
                    <option value="SEMINARIO">Seminario</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Fecha Inicio
                  </label>
                  <input
                    type="date"
                    name="fecha_inicio"
                    value={formData.fecha_inicio}
                    onChange={handleChange}
                    className="input"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Fecha Fin
                  </label>
                  <input
                    type="date"
                    name="fecha_fin"
                    value={formData.fecha_fin}
                    onChange={handleChange}
                    className="input"
                    required
                  />
                </div>
              </div>
            </div>

            {/* Detailed Information */}
            <div className="border-t border-gray-200 dark:border-gray-700 pt-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Objetivos de Aprendizaje
                  <span className="text-xs text-gray-500 dark:text-gray-400 ml-2">(uno por línea)</span>
                </label>
                <textarea
                  placeholder="Ejemplo:&#10;Comprender los principios de programación orientada a objetos&#10;Desarrollar aplicaciones utilizando patrones de diseño"
                  value={formData.objetivos.join('\n')}
                  onChange={(e) => handleArrayChange('objetivos', e.target.value)}
                  className="input font-mono text-sm"
                  rows="4"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Actividades Planificadas
                  <span className="text-xs text-gray-500 dark:text-gray-400 ml-2">(una por línea)</span>
                </label>
                <textarea
                  placeholder="Ejemplo:&#10;Clase teórica sobre encapsulamiento&#10;Práctica de laboratorio - Implementación de clases&#10;Evaluación formativa"
                  value={formData.actividades.join('\n')}
                  onChange={(e) => handleArrayChange('actividades', e.target.value)}
                  className="input font-mono text-sm"
                  rows="5"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Recursos Necesarios
                  <span className="text-xs text-gray-500 dark:text-gray-400 ml-2">(uno por línea)</span>
                </label>
                <textarea
                  placeholder="Ejemplo:&#10;Sala de computación con 30 equipos&#10;Proyector y pizarra digital&#10;Licencias de software de desarrollo"
                  value={formData.recursos.join('\n')}
                  onChange={(e) => handleArrayChange('recursos', e.target.value)}
                  className="input font-mono text-sm"
                  rows="4"
                />
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center justify-end gap-3 pt-6 border-t border-gray-200 dark:border-gray-700">
              <button
                type="button"
                onClick={onCancel}
                className="btn-secondary"
                disabled={saving}
              >
                Cancelar
              </button>
              <button
                type="submit"
                className="btn-primary inline-flex items-center"
                disabled={saving}
              >
                {saving ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Guardando...
                  </>
                ) : (
                  <>
                    <svg className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    {planificacion ? 'Actualizar' : 'Crear'} Planificación
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default PlanificacionForm;