import React, { useState } from 'react';
import { Table, Button, Modal, LoadingSpinner, ErrorMessage } from '../common';
import { usePlanificaciones } from '../../hooks/useApi';
import PlanificacionForm from './PlanificacionForm';

const PlanificacionList = ({ tipo = null, className = '' }) => {
  const {
    planificaciones,
    loading,
    error,
    fetchData,
    enviarAValidacion,
    validarPlanificacion,
    create,
    update,
  } = usePlanificaciones();

  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingPlanificacion, setEditingPlanificacion] = useState(null);
  const [validationModal, setValidationModal] = useState({ show: false, planificacion: null });
  const [validationComments, setValidationComments] = useState('');
  const [actionLoading, setActionLoading] = useState(false);

  // Filtrar planificaciones por tipo si se especifica
  const filteredPlanificaciones = tipo 
    ? planificaciones.filter(p => p.tipo === tipo)
    : planificaciones;

  // Definir columnas de la tabla
  const columns = [
    {
      key: 'titulo',
      title: 'Título',
      render: (value, row) => (
        <div>
          <p className="font-medium text-gray-900">{value}</p>
          <p className="text-sm text-gray-500">{row.tipo}</p>
        </div>
      ),
    },
    {
      key: 'docente_nombre',
      title: 'Docente',
    },
    {
      key: 'curso_nombre',
      title: 'Curso',
    },
    {
      key: 'asignatura_nombre',
      title: 'Asignatura',
    },
    {
      key: 'fecha_inicio',
      title: 'Fecha Inicio',
      render: (value) => new Date(value).toLocaleDateString(),
    },
    {
      key: 'fecha_fin',
      title: 'Fecha Fin',
      render: (value) => new Date(value).toLocaleDateString(),
    },
    {
      key: 'estado',
      title: 'Estado',
      render: (value) => {
        const colors = {
          BORRADOR: 'bg-gray-100 text-gray-800',
          PENDIENTE: 'bg-yellow-100 text-yellow-800',
          APROBADA: 'bg-green-100 text-green-800',
          RECHAZADA: 'bg-red-100 text-red-800',
        };
        return (
          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${colors[value]}`}>
            {value}
          </span>
        );
      },
    },
    {
      key: 'acciones',
      title: 'Acciones',
      render: (_, row) => (
        <div className="flex space-x-2">
          <Button
            size="sm"
            variant="outline"
            onClick={(e) => {
              e.stopPropagation();
              setEditingPlanificacion(row);
            }}
          >
            Editar
          </Button>
          
          {row.estado === 'BORRADOR' && (
            <Button
              size="sm"
              variant="secondary"
              onClick={(e) => {
                e.stopPropagation();
                handleEnviarValidacion(row.id);
              }}
            >
              Enviar
            </Button>
          )}
          
          {row.estado === 'PENDIENTE' && (
            <Button
              size="sm"
              variant="success"
              onClick={(e) => {
                e.stopPropagation();
                setValidationModal({ show: true, planificacion: row });
              }}
            >
              Validar
            </Button>
          )}
        </div>
      ),
    },
  ];

  const handleEnviarValidacion = async (id) => {
    try {
      setActionLoading(true);
      await enviarAValidacion(id);
    } catch (err) {
      console.error('Error al enviar a validación:', err);
    } finally {
      setActionLoading(false);
    }
  };

  const handleValidarPlanificacion = async (accion) => {
    try {
      setActionLoading(true);
      await validarPlanificacion(
        validationModal.planificacion.id, 
        accion, 
        validationComments
      );
      setValidationModal({ show: false, planificacion: null });
      setValidationComments('');
    } catch (err) {
      console.error('Error al validar planificación:', err);
    } finally {
      setActionLoading(false);
    }
  };

  const handleCreatePlanificacion = async (formData) => {
    await create(formData);
    setShowCreateModal(false);
  };

  const handleUpdatePlanificacion = async (formData) => {
    await update(editingPlanificacion.id, formData);
    setEditingPlanificacion(null);
  };

  if (error) {
    return (
      <ErrorMessage 
        message={error} 
        onRetry={fetchData}
        className={className}
      />
    );
  }

  return (
    <div className={className}>
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-xl font-semibold text-gray-900">
            Planificaciones{tipo && ` ${tipo.charAt(0) + tipo.slice(1).toLowerCase()}es`}
          </h2>
          <p className="text-sm text-gray-600">
            {filteredPlanificaciones.length} planificaciones encontradas
          </p>
        </div>
        
        <Button
          onClick={() => setShowCreateModal(true)}
          disabled={actionLoading}
        >
          Nueva Planificación
        </Button>
      </div>

      {/* Tabla */}
      <Table
        columns={columns}
        data={filteredPlanificaciones}
        loading={loading}
        onRowClick={(row) => {
          // Abrir detalle de planificación
          console.log('Ver detalle de:', row);
        }}
      />

      {/* Modal de creación */}
      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title="Nueva Planificación"
        size="xl"
      >
        <PlanificacionForm
          tipo={tipo || 'ANUAL'}
          onSubmit={handleCreatePlanificacion}
          onCancel={() => setShowCreateModal(false)}
        />
      </Modal>

      {/* Modal de edición */}
      <Modal
        isOpen={!!editingPlanificacion}
        onClose={() => setEditingPlanificacion(null)}
        title="Editar Planificación"
        size="xl"
      >
        {editingPlanificacion && (
          <PlanificacionForm
            tipo={editingPlanificacion.tipo}
            initialData={editingPlanificacion}
            onSubmit={handleUpdatePlanificacion}
            onCancel={() => setEditingPlanificacion(null)}
          />
        )}
      </Modal>

      {/* Modal de validación */}
      <Modal
        isOpen={validationModal.show}
        onClose={() => {
          setValidationModal({ show: false, planificacion: null });
          setValidationComments('');
        }}
        title="Validar Planificación"
        size="md"
      >
        {validationModal.planificacion && (
          <div className="space-y-4">
            <div className="bg-gray-50 p-4 rounded-md">
              <h4 className="font-medium text-gray-900">
                {validationModal.planificacion.titulo}
              </h4>
              <p className="text-sm text-gray-600">
                Docente: {validationModal.planificacion.docente_nombre}
              </p>
              <p className="text-sm text-gray-600">
                Curso: {validationModal.planificacion.curso_nombre}
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Comentarios (opcional)
              </label>
              <textarea
                value={validationComments}
                onChange={(e) => setValidationComments(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={3}
                placeholder="Ingresa comentarios sobre la validación..."
              />
            </div>

            <div className="flex justify-end space-x-3">
              <Button
                variant="danger"
                onClick={() => handleValidarPlanificacion('rechazar')}
                loading={actionLoading}
              >
                Rechazar
              </Button>
              
              <Button
                variant="success"
                onClick={() => handleValidarPlanificacion('aprobar')}
                loading={actionLoading}
              >
                Aprobar
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default PlanificacionList;