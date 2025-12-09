import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const GestionUsuarios = () => {
  const navigate = useNavigate();
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    nombre: '',
    apellido: '',
    password: '',
    password2: '',
    role: 'DOCENTE'
  });

  const getAuthHeaders = () => {
    const token = localStorage.getItem('token');
    return {
      headers: { 'Authorization': `Bearer ${token}` }
    };
  };

  useEffect(() => {
    cargarUsuarios();
  }, []);

  const cargarUsuarios = async () => {
    try {
      // Nota: Este endpoint necesitará ser creado en el backend
      const response = await axios.get('http://localhost/api/auth/users/', getAuthHeaders());
      setUsuarios(response.data);
    } catch (error) {
      console.error('Error cargando usuarios:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.password !== formData.password2) {
      alert('Las contraseñas no coinciden');
      return;
    }

    try {
      await axios.post('http://localhost/api/auth/register/', formData, getAuthHeaders());
      alert('Usuario creado exitosamente');
      setShowForm(false);
      setFormData({
        username: '',
        email: '',
        nombre: '',
        apellido: '',
        password: '',
        password2: '',
        role: 'DOCENTE'
      });
      cargarUsuarios();
    } catch (error) {
      console.error('Error creando usuario:', error);
      alert('Error al crear usuario: ' + (error.response?.data?.detail || error.message));
    }
  };

  const getRoleBadge = (role) => {
    const badges = {
      DOCENTE: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
      UTP: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300',
      EQUIPO_DIRECTIVO: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
    };
    return badges[role] || badges.DOCENTE;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Cargando...</div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Gestión de Usuarios</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">Administra los usuarios del sistema</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => navigate('/')}
            className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg font-medium transition-colors"
          >
            ← Volver al Dashboard
          </button>
          <button
            onClick={() => setShowForm(true)}
            className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-colors inline-flex items-center"
          >
            <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Nuevo Usuario
          </button>
        </div>
      </div>

      {/* Lista de usuarios */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead className="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Usuario</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Nombre</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Email</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Rol</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Estado</th>
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            {usuarios.map((usuario) => (
              <tr key={usuario.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  {usuario.username}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {usuario.nombre} {usuario.apellido}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {usuario.email}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium ${getRoleBadge(usuario.role)}`}>
                    {usuario.role}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium ${usuario.activo ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {usuario.activo ? 'Activo' : 'Inactivo'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal Formulario */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4 max-h-[90vh] overflow-y-auto">
            <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-gray-100">Crear Nuevo Usuario</h3>
            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Nombre de Usuario</label>
                <input
                  type="text"
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  required
                />
              </div>
              
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Nombre</label>
                <input
                  type="text"
                  value={formData.nombre}
                  onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Apellido</label>
                <input
                  type="text"
                  value={formData.apellido}
                  onChange={(e) => setFormData({ ...formData, apellido: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Email</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  required
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Rol</label>
                <select
                  value={formData.role}
                  onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                >
                  <option value="DOCENTE">Docente</option>
                  <option value="UTP">UTP</option>
                  <option value="EQUIPO_DIRECTIVO">Equipo Directivo</option>
                </select>
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Contraseña</label>
                <input
                  type="password"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  required
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Confirmar Contraseña</label>
                <input
                  type="password"
                  value={formData.password2}
                  onChange={(e) => setFormData({ ...formData, password2: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  required
                />
              </div>

              <div className="flex gap-2">
                <button type="submit" className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">
                  Crear Usuario
                </button>
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="flex-1 px-4 py-2 bg-gray-300 dark:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default GestionUsuarios;
