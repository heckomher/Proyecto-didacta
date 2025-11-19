# Frontend Optimizado para API Didacta

Esta documentación describe cómo el frontend ha sido optimizado para usar los nuevos endpoints del backend de manera eficiente.

## 🚀 Características Principales

### 1. Servicios API Unificados (`src/services/api.js`)
- **Cliente HTTP configurado**: Interceptors automáticos para tokens JWT
- **Servicios base**: Clase BaseService para operaciones CRUD estándar
- **Servicios específicos**: Para cada endpoint del backend
- **Manejo de errores**: Refresh automático de tokens y manejo de errores

### 2. Hooks Personalizados (`src/hooks/useApi.js`)
- **useCrud**: Hook genérico para operaciones CRUD
- **Hooks específicos**: Para cada entidad (useDocentes, useCursos, etc.)
- **usePlanificacionForm**: Hook especializado para formularios de planificación
- **Estado de carga**: Loading y error states integrados

### 3. Contexto Académico (`src/contexts/AcademicContext.jsx`)
- **Estado global**: Año académico activo y configuración
- **Validaciones**: Verificación automática de configuración
- **Funciones utilitarias**: Para activar/cerrar años académicos

### 4. Componentes Reutilizables (`src/components/common/`)
- **UI Components**: Botones, formularios, tablas, modales
- **Estados de carga**: Spinners y mensajes de error/éxito
- **Formularios**: Campos con validación integrada

### 5. Componentes Específicos

#### Planificaciones
- `PlanificacionForm.jsx`: Formulario inteligente con validaciones
- `PlanificacionList.jsx`: Lista con acciones (crear, editar, validar)

#### Configuración
- `ConfiguracionAcademicaOptimizada.jsx`: Gestión completa de configuración

## 📡 Endpoints Disponibles

### Autenticación
```javascript
import { authService } from '@/services/api';

// Login
const { access, refresh } = await authService.login(username, password);

// Usuario actual
const user = await authService.getCurrentUser();
```

### Configuración Académica
```javascript
import { anioAcademicoService } from '@/services/api';

// Obtener año activo
const anioActivo = await anioAcademicoService.getActivo();

// Activar año académico
await anioAcademicoService.activar(id);

// Cerrar año académico
await anioAcademicoService.cerrar(id, password);
```

### Gestión de Usuarios
```javascript
import { docenteService, equipoDirectivoService } from '@/services/api';

// Obtener docentes
const docentes = await docenteService.getAll();

// Crear docente
const nuevoDocente = await docenteService.create({
  usuario: userId,
  rut: '12345678-9',
  especialidad: 'Matemáticas'
});
```

### Estructura Académica
```javascript
import { cursoService, asignaturaService } from '@/services/api';

// Obtener cursos por nivel
const cursos = await cursoService.getAll({ nivel: nivelId });

// Crear asignatura
const asignatura = await asignaturaService.create({
  nombre_asignatura: 'Matemáticas Aplicadas',
  descripcion: 'Curso de matemáticas...'
});
```

### Planificaciones
```javascript
import { planificacionService } from '@/services/api';

// Crear planificación
const planificacion = await planificacionService.create({
  titulo: 'Planificación Anual 2025',
  tipo: 'ANUAL',
  docente: docenteId,
  curso: cursoId,
  asignatura: asignaturaId,
  // ... otros campos
});

// Enviar a validación
await planificacionService.enviarAValidacion(planificacionId);

// Validar planificación
await planificacionService.validar(planificacionId, 'aprobar', 'Comentarios...');
```

## 🎯 Uso de Hooks

### Hook Básico para CRUD
```javascript
import { useCrud } from '@/hooks/useApi';
import { cursoService } from '@/services/api';

function CursosComponent() {
  const {
    data: cursos,
    loading,
    error,
    create,
    update,
    remove
  } = useCrud(cursoService);

  const handleCreate = async (cursoData) => {
    try {
      await create(cursoData);
      // Datos se actualizan automáticamente
    } catch (err) {
      console.error('Error:', err);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div>
      {cursos.map(curso => (
        <div key={curso.id}>{curso.nombre_curso}</div>
      ))}
    </div>
  );
}
```

### Hook Específico para Planificaciones
```javascript
import { usePlanificaciones } from '@/hooks/useApi';

function PlanificacionesComponent() {
  const {
    planificaciones,
    loading,
    enviarAValidacion,
    validarPlanificacion
  } = usePlanificaciones();

  const handleEnviar = async (id) => {
    await enviarAValidacion(id);
    // Estado se actualiza automáticamente
  };

  return (
    <div>
      {planificaciones.map(plan => (
        <div key={plan.id}>
          {plan.titulo}
          <button onClick={() => handleEnviar(plan.id)}>
            Enviar a Validación
          </button>
        </div>
      ))}
    </div>
  );
}
```

### Hook para Formularios
```javascript
import { usePlanificacionForm } from '@/hooks/useApi';

function FormularioComponent() {
  const {
    formData,
    updateField,
    validateForm,
    docentes,
    cursos,
    asignaturas
  } = usePlanificacionForm('ANUAL');

  const handleSubmit = (e) => {
    e.preventDefault();
    const { isValid, errors } = validateForm();
    
    if (isValid) {
      // Procesar formulario
    } else {
      // Mostrar errores
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <FormField
        label="Título"
        value={formData.titulo}
        onChange={(value) => updateField('titulo', value)}
      />
      
      <FormField
        label="Docente"
        type="select"
        value={formData.docente}
        onChange={(value) => updateField('docente', value)}
        options={docentes.map(d => ({
          value: d.id,
          label: d.usuario_info.nombre
        }))}
      />
    </form>
  );
}
```

## 🔧 Contexto Académico

```javascript
import { useAcademic } from '@/contexts/AcademicContext';

function ComponenteConValidacion() {
  const {
    anioActivo,
    configuracionValida,
    canCreatePlanificaciones,
    getConfigurationMessage
  } = useAcademic();

  if (!canCreatePlanificaciones()) {
    return (
      <div className="alert alert-warning">
        {getConfigurationMessage()}
      </div>
    );
  }

  return (
    <div>
      <p>Año activo: {anioActivo.nombre}</p>
      {/* Contenido del componente */}
    </div>
  );
}
```

## 📱 Componentes de UI

### Formularios
```javascript
import { FormField, Button } from '@/components/common';

<FormField
  label="Título"
  value={titulo}
  onChange={setTitulo}
  required
  error={errors.titulo}
/>

<Button
  variant="primary"
  loading={loading}
  onClick={handleSubmit}
>
  Guardar
</Button>
```

### Tablas
```javascript
import { Table } from '@/components/common';

const columns = [
  { key: 'nombre', title: 'Nombre' },
  { key: 'fecha', title: 'Fecha', render: (value) => new Date(value).toLocaleDateString() },
  { key: 'acciones', title: 'Acciones', render: (_, row) => <Button>Editar</Button> }
];

<Table
  columns={columns}
  data={datos}
  loading={loading}
  onRowClick={handleRowClick}
/>
```

### Modales
```javascript
import { Modal } from '@/components/common';

<Modal
  isOpen={showModal}
  onClose={() => setShowModal(false)}
  title="Título del Modal"
  size="lg"
>
  <div>Contenido del modal</div>
</Modal>
```

## 🛠️ Configuración y Estado

### Provider Setup en App.jsx
```javascript
<ThemeProvider>
  <AuthProvider>
    <AcademicProvider>
      <Router>
        {/* Rutas */}
      </Router>
    </AcademicProvider>
  </AuthProvider>
</ThemeProvider>
```

### Rutas Disponibles
- `/planificaciones` - Lista general de planificaciones
- `/planificaciones/anuales` - Planificaciones anuales
- `/planificaciones/unidades` - Planificaciones de unidad
- `/planificaciones/semanales` - Planificaciones semanales
- `/configuracion-academica` - Configuración del sistema

## 🚀 Optimizaciones Implementadas

1. **Caching inteligente**: Los hooks mantienen datos en memoria
2. **Lazy loading**: Los datos se cargan solo cuando se necesitan
3. **Actualizaciones optimistas**: UI se actualiza inmediatamente
4. **Manejo de errores**: Reintentos automáticos y fallbacks
5. **Validación client-side**: Validaciones antes de enviar al servidor
6. **Estado global**: Contextos para datos compartidos
7. **Componentes reutilizables**: Menos código duplicado
8. **TypeScript support**: Tipos para mejor desarrollo (próximamente)

## 📚 Próximos Pasos

1. Implementar TypeScript para mejor type safety
2. Añadir tests unitarios para hooks y componentes
3. Implementar Service Workers para offline support
4. Añadir notificaciones push para validaciones
5. Optimizar bundle size con lazy loading de rutas
6. Implementar temas personalizables
7. Añadir drag & drop para reordenar elementos