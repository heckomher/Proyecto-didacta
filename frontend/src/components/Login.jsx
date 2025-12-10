import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import toast from 'react-hot-toast';
import logoClaro from '../assets/images/logo-didacta-claro-sin-fondo.png';
import logoOscuro from '../assets/images/logo-didacta-oscuro-sin-fondo.png';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await login(username, password);
    if (result.success) {
      navigate('/');
    } else {
      toast.error(result.error);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-gray-900 dark:to-gray-800 px-4">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            {/* Logo para tema claro */}
            <img src={logoClaro} alt="Didacta" className="h-32 dark:hidden" />
            {/* Logo para tema oscuro */}
            <img src={logoOscuro} alt="Didacta" className="h-32 hidden dark:block" />
          </div>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">Sistema de Gestión Académica</p>
        </div>

        <div className="card p-8">
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">Iniciar Sesión</h3>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Usuario
              </label>
              <input
                id="username"
                type="text"
                placeholder="Ingrese su usuario"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="input"
                required
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Contraseña
              </label>
              <input
                id="password"
                type="password"
                placeholder="Ingrese su contraseña"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input"
                required
              />
            </div>

            <button type="submit" className="btn-primary w-full">
              Iniciar Sesión
            </button>
          </form>
        </div>

        <p className="mt-6 text-center text-sm text-gray-600 dark:text-gray-400">
          ¿Necesita ayuda? Contacte al administrador del sistema
        </p>
      </div>
    </div>
  );
};

export default Login;