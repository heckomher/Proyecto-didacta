import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { authService } from '../services/api';

const GestionUsuarios = () => {
  const navigate = useNavigate();
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editingUser, setEditingUser] = useState(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [userToDelete, setUserToDelete] = useState(null);

  const [formData, setFormData] = useState({
    username: '',
    email: '',
    nombre: '',
    apellido: '',
    password: '',
    password2: '',
    role: 'DOCENTE'
  });

  const [editFormData, setEditFormData] = useState({
    email: '',
    nombre: '',
    apellido: '',
    role: '',
    activo: true
  });

  useEffect(() => {
    cargarUsuarios();
  }, []);

  const cargarUsuarios = async () => {
    try {
      const data = await authService.getUsers();
      setUsuarios(data);
    } catch (error) {
      console.error('Error cargando usuarios:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.password2) {
      toast.error('Las contraseñas no coinciden');
      return;
    }

    if (formData.password.length < 8) {
      toast.error('Contraseña débil: Debe tener al menos 8 caracteres');
      return;
    }

    if (/^\d+$/.test(formData.password)) {
      toast.error('Contraseña débil: No puede contener solo números');
      return;
    }

    try {
      await authService.register(formData);
      toast.success('Usuario creado exitosamente');
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
      if (error.response?.data?.password) {
        const passwordErrors = error.response.data.password;
        if (Array.isArray(passwordErrors)) {
          toast.error('Contraseña no válida: ' + passwordErrors.join(', '));
        } else {
          toast.error('Contraseña no válida: ' + passwordErrors);
        }
      } else {
        toast.error('Error al crear usuario: ' + (error.response?.data?.detail || error.message));
      }
    }
  };

  const handleEditClick = (usuario) => {
    setEditingUser(usuario);
    setEditFormData({
      email: usuario.email || '',
      nombre: usuario.nombre || '',
      apellido: usuario.apellido || '',
      role: usuario.role || 'DOCENTE',
      activo: usuario.activo
    });
    setShowEditModal(true);
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    try {
      await authService.updateUser(editingUser.id, editFormData);
      toast.success('Usuario actualizado exitosamente');
      setShowEditModal(false);
      setEditingUser(null);
      cargarUsuarios();
    } catch (error) {
      console.error('Error actualizando usuario:', error);
      toast.error('Error al actualizar usuario: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleToggleActive = async (usuario) => {
    try {
      const result = await authService.toggleUserActive(usuario.id);
      toast.success(result.message);
      cargarUsuarios();
    } catch (error) {
      console.error('Error cambiando estado:', error);
      toast.error('Error: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleDeleteClick = (usuario) => {
    setUserToDelete(usuario);
    setShowDeleteConfirm(true);
  };

  const handleDeleteConfirm = async () => {
    try {
      const result = await authService.deleteUser(userToDelete.id);
      toast.success(result.message);
      setShowDeleteConfirm(false);
      setUserToDelete(null);
      cargarUsuarios();
    } catch (error) {
      console.error('Error eliminando usuario:', error);
      toast.error('Error: ' + (error.response?.data?.detail || error.message));
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

  // Verificar si un usuario es admin
  const isAdmin = (user) => {
    return ['UTP', 'EQUIPO_DIRECTIVO'].includes(user.role) || user.is_superuser;
  };

  // Contar admins activos excluyendo un usuario específico
  const countOtherActiveAdmins = (excludeId) => {
    return usuarios.filter(
      u => u.activo && isAdmin(u) && u.id !== excludeId
    ).length;
  };

  // Verificar si un usuario es el último admin activo
  const isLastActiveAdmin = (user) => {
    if (!isAdmin(user) || !user.activo) return false;
    return countOtherActiveAdmins(user.id) === 0;
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
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            {usuarios.map((usuario) => (
              <tr
                key={usuario.id}
                className="hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition-colors"
                onClick={() => handleEditClick(usuario)}
              >
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
                <td className="px-6 py-4 whitespace-nowrap text-sm" onClick={(e) => e.stopPropagation()}>
                  <div className="flex gap-2">
                    {usuario.activo && isLastActiveAdmin(usuario) ? (
                      <span
                        className="px-3 py-1 bg-gray-200 text-gray-500 rounded text-xs font-medium cursor-not-allowed"
                        title="Último administrador activo"
                      >
                        Protegido
                      </span>
                    ) : (
                      <button
                        onClick={() => handleToggleActive(usuario)}
                        className={`px-3 py-1 rounded text-xs font-medium transition-colors ${usuario.activo
                          ? 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200'
                          : 'bg-green-100 text-green-800 hover:bg-green-200'
                          }`}
                      >
                        {usuario.activo ? 'Desactivar' : 'Activar'}
                      </button>
                    )}
                    {isLastActiveAdmin(usuario) ? (
                      <span
                        className="px-3 py-1 bg-gray-200 text-gray-500 rounded text-xs font-medium cursor-not-allowed"
                        title="No se puede eliminar al último administrador"
                      >
                        Eliminar
                      </span>
                    ) : (
                      <button
                        onClick={() => handleDeleteClick(usuario)}
                        className="px-3 py-1 bg-red-100 text-red-800 hover:bg-red-200 rounded text-xs font-medium transition-colors"
                      >
                        Eliminar
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal Crear Usuario */}
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
                <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
                  Mínimo 8 caracteres. Debe incluir letras y números.
                </p>
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

      {/* Modal Editar Usuario */}
      {showEditModal && editingUser && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4 max-h-[90vh] overflow-y-auto">
            <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-gray-100">Editar Usuario</h3>
            <form onSubmit={handleEditSubmit}>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Nombre de Usuario</label>
                <input
                  type="text"
                  value={editingUser.username}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-100 dark:bg-gray-600 dark:text-gray-100 cursor-not-allowed"
                  disabled
                />
                <p className="mt-1 text-xs text-gray-500">El nombre de usuario no se puede cambiar</p>
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Nombre</label>
                <input
                  type="text"
                  value={editFormData.nombre}
                  onChange={(e) => setEditFormData({ ...editFormData, nombre: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Apellido</label>
                <input
                  type="text"
                  value={editFormData.apellido}
                  onChange={(e) => setEditFormData({ ...editFormData, apellido: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Email</label>
                <input
                  type="email"
                  value={editFormData.email}
                  onChange={(e) => setEditFormData({ ...editFormData, email: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                  required
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Rol</label>
                <select
                  value={editFormData.role}
                  onChange={(e) => setEditFormData({ ...editFormData, role: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                >
                  <option value="DOCENTE">Docente</option>
                  <option value="UTP">UTP</option>
                  <option value="EQUIPO_DIRECTIVO">Equipo Directivo</option>
                </select>
              </div>

              <div className="flex gap-2">
                <button type="submit" className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">
                  Guardar Cambios
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowEditModal(false);
                    setEditingUser(null);
                  }}
                  className="flex-1 px-4 py-2 bg-gray-300 dark:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal Confirmar Eliminación */}
      {showDeleteConfirm && userToDelete && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-sm w-full mx-4">
            <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-gray-100">Confirmar Eliminación</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              ¿Está seguro que desea eliminar al usuario <strong>{userToDelete.username}</strong>? Esta acción no se puede deshacer.
            </p>
            <div className="flex gap-2">
              <button
                onClick={handleDeleteConfirm}
                className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
              >
                Eliminar
              </button>
              <button
                onClick={() => {
                  setShowDeleteConfirm(false);
                  setUserToDelete(null);
                }}
                className="flex-1 px-4 py-2 bg-gray-300 dark:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500"
              >
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GestionUsuarios;

