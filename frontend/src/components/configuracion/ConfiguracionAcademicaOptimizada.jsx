import React, { useState } from 'react';
import {
  Card,
  Button,
  Table,
  Modal,
  FormField,
  ErrorMessage,
  SuccessMessage,
  LoadingSpinner,
} from '../common';
import {
  useAniosAcademicos,
  useCrud,
} from '../../hooks/useApi';
import {
  periodoAcademicoService,
  feriadoService,
  vacacionesService,
} from '../../services/api';

const ConfiguracionAcademicaOptimizada = () => {
  const {
    data: aniosAcademicos,
    loading: aniosLoading,
    error: aniosError,
    anioActivo,
    activarAnio,
    cerrarAnio,
    create: createAnio,
    update: updateAnio,
    remove: removeAnio,
  } = useAniosAcademicos();

  const {
    data: periodos,
    loading: periodosLoading,
    create: createPeriodo,
    remove: removePeriodo,
    fetchData: fetchPeriodos,
  } = useCrud(periodoAcademicoService);

  const {
    data: feriados,
    loading: feriadosLoading,
    create: createFeriado,
    remove: removeFeriado,
    fetchData: fetchFeriados,
  } = useCrud(feriadoService);

  const [activeTab, setActiveTab] = useState('anios');
  const [showModal, setShowModal] = useState({ type: '', show: false, data: null });
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // Configuración de pestañas
  const tabs = [
    { id: 'anios', label: 'Años Académicos', icon: '📅' },
    { id: 'periodos', label: 'Períodos', icon: '📊' },
    { id: 'feriados', label: 'Feriados', icon: '🎉' },
  ];

  // Columnas para años académicos
  const aniosColumns = [
    {
      key: 'nombre',
      title: 'Año',
      render: (value, row) => (
        <div className="flex items-center">
          <span className="font-medium">{value}</span>
          {row.id === anioActivo?.id && (
            <span className="ml-2 inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
              Activo
            </span>
          )}
        </div>
      ),
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
          ACTIVO: 'bg-green-100 text-green-800',
          CERRADO: 'bg-red-100 text-red-800',
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
          {row.estado === 'BORRADOR' && (
            <Button
              size="sm"
              variant="success"
              onClick={() => handleActivarAnio(row.id)}
            >
              Activar
            </Button>
          )}
          
          {row.estado === 'ACTIVO' && (
            <Button
              size="sm"
              variant="danger"
              onClick={() => setShowModal({ 
                type: 'cerrar', 
                show: true, 
                data: row 
              })}
            >
              Cerrar
            </Button>
          )}
          
          {row.estado !== 'CERRADO' && (
            <Button
              size="sm"
              variant="outline"
              onClick={() => setShowModal({ 
                type: 'editAnio', 
                show: true, 
                data: row 
              })}
            >
              Editar
            </Button>
          )}
        </div>
      ),
    },
  ];

  const handleActivarAnio = async (id) => {
    try {
      setLoading(true);
      await activarAnio(id);
      setSuccess('Año académico activado correctamente');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitForm = async () => {
    try {
      setLoading(true);
      setError(null);

      switch (showModal.type) {
        case 'newAnio':
          await createAnio(formData);
          setSuccess('Año académico creado correctamente');
          break;
        case 'editAnio':
          await updateAnio(showModal.data.id, formData);
          setSuccess('Año académico actualizado correctamente');
          break;
        case 'cerrar':
          await cerrarAnio(showModal.data.id, formData.password);
          setSuccess('Año académico cerrado correctamente');
          break;
        case 'newPeriodo':
          await createPeriodo(formData);
          await fetchPeriodos();
          setSuccess('Período creado correctamente');
          break;
        case 'newFeriado':
          await createFeriado(formData);
          await fetchFeriados();
          setSuccess('Feriado creado correctamente');
          break;
      }

      setShowModal({ type: '', show: false, data: null });
      setFormData({});
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const renderModalContent = () => {
    switch (showModal.type) {
      case 'newAnio':
      case 'editAnio':
        return (
          <div className="space-y-4">
            <FormField
              label="Nombre del Año"
              value={formData.nombre || ''}
              onChange={(value) => setFormData({ ...formData, nombre: value })}
              placeholder="2025"
              required
            />
            
            <div className="grid grid-cols-2 gap-4">
              <FormField
                label="Fecha de Inicio"
                type="date"
                value={formData.fecha_inicio || ''}
                onChange={(value) => setFormData({ ...formData, fecha_inicio: value })}
                required
              />
              
              <FormField
                label="Fecha de Fin"
                type="date"
                value={formData.fecha_fin || ''}
                onChange={(value) => setFormData({ ...formData, fecha_fin: value })}
                required
              />
            </div>
            
            <FormField
              label="Tipo de Período"
              type="select"
              value={formData.tipo_periodo || 'SEMESTRE'}
              onChange={(value) => setFormData({ ...formData, tipo_periodo: value })}
              options={[
                { value: 'SEMESTRE', label: 'Semestral' },
                { value: 'TRIMESTRE', label: 'Trimestral' },
                { value: 'ANUAL', label: 'Anual' },
              ]}
            />
          </div>
        );

      case 'cerrar':
        return (
          <div className="space-y-4">
            <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
              <p className="text-yellow-800">
                <strong>¿Está seguro que desea cerrar el año académico "{showModal.data?.nombre}"?</strong>
              </p>
              <p className="text-sm text-yellow-700 mt-2">
                Esta acción no se puede deshacer. El año académico quedará en modo de solo lectura.
              </p>
            </div>
            
            <FormField
              label="Confirme su contraseña"
              type="password"
              value={formData.password || ''}
              onChange={(value) => setFormData({ ...formData, password: value })}
              placeholder="Ingrese su contraseña"
              required
            />
          </div>
        );

      default:
        return null;
    }
  };

  const getModalTitle = () => {
    switch (showModal.type) {
      case 'newAnio': return 'Nuevo Año Académico';
      case 'editAnio': return 'Editar Año Académico';
      case 'cerrar': return 'Cerrar Año Académico';
      case 'newPeriodo': return 'Nuevo Período';
      case 'newFeriado': return 'Nuevo Feriado';
      default: return '';
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">
          Configuración Académica
        </h1>
        <p className="text-gray-600">
          Gestiona años académicos, períodos y feriados del sistema
        </p>
      </div>

      {error && <ErrorMessage message={error} onRetry={() => setError(null)} className="mb-6" />}
      {success && <SuccessMessage message={success} onClose={() => setSuccess(null)} className="mb-6" />}

      {/* Estado del año académico activo */}
      {anioActivo && (
        <Card className="mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-medium text-gray-900">
                Año Académico Activo: {anioActivo.nombre}
              </h3>
              <p className="text-sm text-gray-600">
                {new Date(anioActivo.fecha_inicio).toLocaleDateString()} - {new Date(anioActivo.fecha_fin).toLocaleDateString()}
              </p>
            </div>
            <div className="text-green-600">
              ✓ Configuración válida
            </div>
          </div>
        </Card>
      )}

      {/* Pestañas */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`
                flex items-center py-2 px-1 border-b-2 font-medium text-sm
                ${activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }
              `}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Contenido de pestañas */}
      {activeTab === 'anios' && (
        <Card
          title="Años Académicos"
          actions={[
            <Button
              key="new"
              onClick={() => setShowModal({ type: 'newAnio', show: true, data: null })}
            >
              Nuevo Año
            </Button>
          ]}
        >
          <Table
            columns={aniosColumns}
            data={aniosAcademicos}
            loading={aniosLoading}
          />
        </Card>
      )}

      {/* Modal */}
      <Modal
        isOpen={showModal.show}
        onClose={() => {
          setShowModal({ type: '', show: false, data: null });
          setFormData({});
        }}
        title={getModalTitle()}
        size="md"
      >
        <div className="space-y-6">
          {renderModalContent()}
          
          <div className="flex justify-end space-x-3">
            <Button
              variant="outline"
              onClick={() => {
                setShowModal({ type: '', show: false, data: null });
                setFormData({});
              }}
            >
              Cancelar
            </Button>
            
            <Button
              onClick={handleSubmitForm}
              loading={loading}
              variant={showModal.type === 'cerrar' ? 'danger' : 'primary'}
            >
              {showModal.type === 'cerrar' ? 'Cerrar Año' : 'Guardar'}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default ConfiguracionAcademicaOptimizada;