import React, { useState, useEffect } from 'react';
import { FormField, Button, ErrorMessage, SuccessMessage, LoadingSpinner } from '../common';
import { usePlanificacionForm } from '../../hooks/useApi';
import { useAcademic } from '../../contexts/AcademicContext';

const PlanificacionForm = ({ 
  tipo = 'ANUAL', 
  initialData = null, 
  onSubmit, 
  onCancel,
  className = '' 
}) => {
  const { canCreatePlanificaciones, getConfigurationMessage } = useAcademic();
  const {
    formData,
    setFormData,
    updateField,
    validateForm,
    anioActivo,
    docentes,
    cursos,
    asignaturas,
    objetivos,
    recursos,
  } = usePlanificacionForm(tipo);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [validationErrors, setValidationErrors] = useState({});

  // Cargar datos iniciales si se está editando
  useEffect(() => {
    if (initialData) {
      setFormData({
        ...formData,
        ...initialData,
        // Asegurar que los arrays se manejen correctamente
        objetivos_aprendizaje: initialData.objetivos_aprendizaje || [],
        recursos_pedagogicos: initialData.recursos_pedagogicos || [],
      });
    }
  }, [initialData]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    setValidationErrors({});

    // Validar configuración académica
    if (!canCreatePlanificaciones()) {
      setError(getConfigurationMessage());
      return;
    }

    // Validar formulario
    const validation = validateForm();
    if (!validation.isValid) {
      setValidationErrors(validation.errors);
      return;
    }

    try {
      setLoading(true);
      await onSubmit(formData);
      setSuccess(initialData ? 'Planificación actualizada correctamente' : 'Planificación creada correctamente');
      
      if (!initialData) {
        // Limpiar formulario después de crear
        setFormData({
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
      }
    } catch (err) {
      setError(err.response?.data?.message || err.message || 'Error al guardar la planificación');
      
      // Manejar errores de validación del backend
      if (err.response?.data && typeof err.response.data === 'object') {
        setValidationErrors(err.response.data);
      }
    } finally {
      setLoading(false);
    }
  };

  // Convertir arrays para los selects
  const docentesOptions = docentes.map(d => ({
    value: d.id,
    label: d.usuario_info ? `${d.usuario_info.nombre} ${d.usuario_info.apellido}`.trim() || d.usuario_info.username : d.rut,
  }));

  const cursosOptions = cursos.map(c => ({
    value: c.id,
    label: `${c.nivel_nombre} - ${c.nombre_curso}`,
  }));

  const asignaturasOptions = asignaturas.map(a => ({
    value: a.id,
    label: a.nombre_asignatura,
  }));

  const objetivosOptions = objetivos.map(o => ({
    value: o.id,
    label: o.descripcion.substring(0, 50) + (o.descripcion.length > 50 ? '...' : ''),
  }));

  const recursosOptions = recursos.map(r => ({
    value: r.id,
    label: `${r.tipo} - ${r.nombre}`,
  }));

  if (!anioActivo) {
    return (
      <div className={`bg-yellow-50 border border-yellow-200 rounded-md p-4 ${className}`}>
        <p className="text-yellow-800">
          No hay año académico activo configurado. No se pueden crear planificaciones.
        </p>
      </div>
    );
  }

  return (
    <div className={className}>
      <form onSubmit={handleSubmit} className="space-y-6">
        {error && <ErrorMessage message={error} />}
        {success && <SuccessMessage message={success} />}

        {/* Información del año académico */}
        <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
          <h4 className="text-sm font-medium text-blue-800 mb-2">Año Académico</h4>
          <p className="text-sm text-blue-700">
            {anioActivo.nombre} ({anioActivo.fecha_inicio} - {anioActivo.fecha_fin})
          </p>
        </div>

        {/* Información básica */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <FormField
            label="Título"
            value={formData.titulo}
            onChange={(value) => updateField('titulo', value)}
            error={validationErrors.titulo}
            required
            placeholder="Ingresa el título de la planificación"
          />

          <FormField
            label="Tipo"
            type="select"
            value={formData.tipo}
            onChange={(value) => updateField('tipo', value)}
            options={[
              { value: 'ANUAL', label: 'Planificación Anual' },
              { value: 'UNIDAD', label: 'Planificación de Unidad' },
              { value: 'SEMANAL', label: 'Planificación Semanal' },
            ]}
            disabled={!!initialData} // No cambiar tipo al editar
            required
          />
        </div>

        <FormField
          label="Descripción"
          type="textarea"
          value={formData.descripcion}
          onChange={(value) => updateField('descripcion', value)}
          error={validationErrors.descripcion}
          placeholder="Describe la planificación..."
        />

        {/* Fechas */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <FormField
            label="Fecha de Inicio"
            type="date"
            value={formData.fecha_inicio}
            onChange={(value) => updateField('fecha_inicio', value)}
            error={validationErrors.fecha_inicio}
            required
          />

          <FormField
            label="Fecha de Fin"
            type="date"
            value={formData.fecha_fin}
            onChange={(value) => updateField('fecha_fin', value)}
            error={validationErrors.fecha_fin}
            required
          />
        </div>

        {/* Asignaciones */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <FormField
            label="Docente"
            type="select"
            value={formData.docente}
            onChange={(value) => updateField('docente', value)}
            options={docentesOptions}
            error={validationErrors.docente}
            required
          />

          <FormField
            label="Curso"
            type="select"
            value={formData.curso}
            onChange={(value) => updateField('curso', value)}
            options={cursosOptions}
            error={validationErrors.curso}
            required
          />

          <FormField
            label="Asignatura"
            type="select"
            value={formData.asignatura}
            onChange={(value) => updateField('asignatura', value)}
            options={asignaturasOptions}
            error={validationErrors.asignatura}
            required
          />
        </div>

        {/* Objetivos y Recursos */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <FormField
            label="Objetivos de Aprendizaje"
            type="multiselect"
            value={formData.objetivos_aprendizaje}
            onChange={(value) => updateField('objetivos_aprendizaje', value)}
            options={objetivosOptions}
            error={validationErrors.objetivos_aprendizaje}
          />

          <FormField
            label="Recursos Pedagógicos"
            type="multiselect"
            value={formData.recursos_pedagogicos}
            onChange={(value) => updateField('recursos_pedagogicos', value)}
            options={recursosOptions}
            error={validationErrors.recursos_pedagogicos}
          />
        </div>

        {/* Campos específicos por tipo */}
        {tipo === 'ANUAL' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <FormField
              label="Meses Académicos"
              type="number"
              value={formData.meses_academicos || 12}
              onChange={(value) => updateField('meses_academicos', parseInt(value))}
              min="1"
              max="12"
            />

            <FormField
              label="Períodos de Evaluación"
              type="number"
              value={formData.periodos_evaluacion || 4}
              onChange={(value) => updateField('periodos_evaluacion', parseInt(value))}
              min="1"
              max="8"
            />
          </div>
        )}

        {tipo === 'UNIDAD' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <FormField
              label="Número de Unidad"
              type="number"
              value={formData.numero_unidad || 1}
              onChange={(value) => updateField('numero_unidad', parseInt(value))}
              min="1"
              required
            />

            <FormField
              label="Semanas de Duración"
              type="number"
              value={formData.semanas_duracion || 4}
              onChange={(value) => updateField('semanas_duracion', parseInt(value))}
              min="1"
              max="20"
            />
          </div>
        )}

        {tipo === 'SEMANAL' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <FormField
              label="Número de Semana"
              type="number"
              value={formData.numero_semana || 1}
              onChange={(value) => updateField('numero_semana', parseInt(value))}
              min="1"
              required
            />

            <FormField
              label="Horas Académicas"
              type="number"
              value={formData.horas_academicas || 45}
              onChange={(value) => updateField('horas_academicas', parseInt(value))}
              min="1"
              max="100"
            />
          </div>
        )}

        {/* Botones */}
        <div className="flex justify-end space-x-4">
          {onCancel && (
            <Button
              variant="outline"
              onClick={onCancel}
              disabled={loading}
            >
              Cancelar
            </Button>
          )}
          
          <Button
            type="submit"
            loading={loading}
            disabled={!canCreatePlanificaciones() || loading}
          >
            {initialData ? 'Actualizar' : 'Crear'} Planificación
          </Button>
        </div>
      </form>
    </div>
  );
};

export default PlanificacionForm;