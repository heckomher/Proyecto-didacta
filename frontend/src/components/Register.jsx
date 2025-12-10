import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useNavigate, Link } from 'react-router-dom';
import { authService } from '../services/api';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    role: 'DOCENTE',
    password: '',
    password2: '',
  });
  const [error, setError] = useState('');
  const [passwordErrors, setPasswordErrors] = useState([]);
  const [usernameStatus, setUsernameStatus] = useState({
    checking: false,
    available: null,
    message: ''
  });

  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    setError('');

    if (name === 'password') {
      validatePassword(value);
    }
  };

  const validatePassword = (password) => {
    const errors = [];
    if (password.length < 8) {
      errors.push('Debe tener al menos 8 caracteres');
    }
    if (/^\d+$/.test(password)) {
      errors.push('No puede ser solo numérica');
    }
    // Simple check for "common" passwords could ideally be better, but we rely on length mainly here locally
    setPasswordErrors(errors);
  };

  const checkUsername = async () => {
    if (!formData.username) return;

    setUsernameStatus({ checking: true, available: null, message: '' });
    try {
      const response = await authService.checkUsername(formData.username);
      if (response.exists) {
        setUsernameStatus({
          checking: false,
          available: false,
          message: 'El nombre de usuario ya está ocupado'
        });
      } else {
        setUsernameStatus({
          checking: false,
          available: true,
          message: 'Nombre de usuario disponible'
        });
      }
    } catch (err) {
      console.error(err);
      setUsernameStatus({
        checking: false,
        available: null,
        message: 'Error al verificar usuario'
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    validatePassword(formData.password);
    if (passwordErrors.length > 0 || formData.password !== formData.password2) {
      setError('Por favor corrige los errores de contraseña');
      return;
    }

    if (usernameStatus.available === false) {
      setError('El nombre de usuario no está disponible');
      return;
    }

    const success = await register(formData);
    if (success) {
      navigate('/login');
    } else {
      // Intentar mejorar el mensaje de error si es posible
      setError('Error al registrar usuario. Revisa los datos e intenta de nuevo.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-gray-900 dark:to-gray-800 px-4 py-12">
      <div className="max-w-2xl w-full">
        <div className="card p-8">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-600 rounded-full mb-4">
              <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
              </svg>
            </div>
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white font-serif">Crear Cuenta</h2>
            <p className="mt-2 text-gray-600 dark:text-gray-400">Sistema de Gestión Académica Didacta</p>
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
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Nombre
                </label>
                <input
                  type="text"
                  name="first_name"
                  placeholder="Juan"
                  value={formData.first_name}
                  onChange={handleChange}
                  className="input"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Apellido
                </label>
                <input
                  type="text"
                  name="last_name"
                  placeholder="Pérez"
                  value={formData.last_name}
                  onChange={handleChange}
                  className="input"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Nombre de Usuario
              </label>
              <div className="relative">
                <input
                  type="text"
                  name="username"
                  placeholder="jperez"
                  value={formData.username}
                  onChange={handleChange}
                  onBlur={checkUsername}
                  className={`input ${usernameStatus.available === true
                      ? 'border-green-500 focus:border-green-500 focus:ring-green-500'
                      : usernameStatus.available === false
                        ? 'border-red-500 focus:border-red-500 focus:ring-red-500'
                        : ''
                    }`}
                  required
                />
                {usernameStatus.checking && (
                  <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
                  </div>
                )}
              </div>
              {usernameStatus.message && (
                <p className={`mt-1 text-sm ${usernameStatus.available === true ? 'text-green-600' : 'text-red-600'
                  }`}>
                  {usernameStatus.message}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Correo Electrónico
              </label>
              <input
                type="email"
                name="email"
                placeholder="jperez@inacap.cl"
                value={formData.email}
                onChange={handleChange}
                className="input"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Rol
              </label>
              <select
                name="role"
                value={formData.role}
                onChange={handleChange}
                className="input"
              >
                <option value="DOCENTE">Docente</option>
                <option value="UTP">UTP (Unidad Técnico Pedagógica)</option>
              </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Contraseña
                </label>
                <input
                  type="password"
                  name="password"
                  placeholder="••••••••"
                  value={formData.password}
                  onChange={handleChange}
                  className="input"
                  required
                />
                {passwordErrors.length > 0 && (
                  <ul className="mt-1 text-xs text-red-600 list-disc list-inside">
                    {passwordErrors.map((err, idx) => (
                      <li key={idx}>{err}</li>
                    ))}
                  </ul>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Confirmar Contraseña
                </label>
                <input
                  type="password"
                  name="password2"
                  placeholder="••••••••"
                  value={formData.password2}
                  onChange={handleChange}
                  className="input"
                  required
                />
                {formData.password2 && formData.password !== formData.password2 && (
                  <p className="mt-1 text-xs text-red-600">Las contraseñas no coinciden</p>
                )}
              </div>
            </div>

            <div className="pt-4">
              <button
                type="submit"
                className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={usernameStatus.available === false || passwordErrors.length > 0 || (formData.password2 && formData.password !== formData.password2)}
              >
                Crear Cuenta
              </button>
            </div>
          </form>

          {/* Footer */}
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              ¿Ya tienes una cuenta?{' '}
              <Link to="/login" className="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400 dark:hover:text-primary-300">
                Inicia sesión aquí
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;