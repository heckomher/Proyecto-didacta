import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import { AcademicProvider } from './contexts/AcademicContext';
import { useAuth } from './hooks/useAuth';
import Login from './components/Login';
import Register from './components/Register';
import GestionUsuarios from './components/GestionUsuarios';
import GestionCursos from './components/GestionCursos';
import GestionAsignaturas from './components/GestionAsignaturas';
import HistorialCursos from './components/HistorialCursos';
import DashboardDocente from './components/DashboardDocente';
import DashboardUTP from './components/DashboardUTP';
import CalendarView from './components/CalendarView';
import ConfiguracionAcademica from './components/ConfiguracionAcademica';
import PlanificacionList from './components/planificacion/PlanificacionList';
import NuevaPlanificacion from './components/NuevaPlanificacion';
import Navbar from './components/Navbar';
import './App.css';

const ProtectedRoute = ({ children }) => {
  const { token, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Cargando...</p>
        </div>
      </div>
    );
  }

  return token ? (
    <>
      <Navbar />
      {children}
    </>
  ) : <Navigate to="/login" />;
};

const Dashboard = () => {
  const { user } = useAuth();

  // Superusers and UTP users see the UTP dashboard
  if (user && (user.role === 'UTP' || user.is_superuser)) {
    return <DashboardUTP />;
  }
  return <DashboardDocente />;
};

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <AcademicProvider>
          <Router>
            <div className="App min-h-screen bg-gray-50 dark:bg-gray-900">
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/gestionar-usuarios" element={<ProtectedRoute><GestionUsuarios /></ProtectedRoute>} />
                <Route path="/gestionar-cursos" element={<ProtectedRoute><GestionCursos /></ProtectedRoute>} />
                <Route path="/gestionar-asignaturas" element={<ProtectedRoute><GestionAsignaturas /></ProtectedRoute>} />
                <Route path="/historial-cursos" element={<ProtectedRoute><HistorialCursos /></ProtectedRoute>} />
                <Route path="/calendar" element={<ProtectedRoute><CalendarView /></ProtectedRoute>} />
                <Route path="/configuracion-academica" element={<ProtectedRoute><ConfiguracionAcademica /></ProtectedRoute>} />

                {/* Rutas de planificación */}
                <Route path="/planificaciones" element={<ProtectedRoute><PlanificacionList /></ProtectedRoute>} />
                <Route path="/planificaciones/nueva" element={<ProtectedRoute><NuevaPlanificacion /></ProtectedRoute>} />
                <Route path="/planificaciones/editar/:tipo/:id" element={<ProtectedRoute><NuevaPlanificacion /></ProtectedRoute>} />
                <Route path="/planificaciones/anuales" element={<ProtectedRoute><PlanificacionList tipo="ANUAL" /></ProtectedRoute>} />
                <Route path="/planificaciones/unidades" element={<ProtectedRoute><PlanificacionList tipo="UNIDAD" /></ProtectedRoute>} />
                <Route path="/planificaciones/semanales" element={<ProtectedRoute><PlanificacionList tipo="SEMANAL" /></ProtectedRoute>} />

                <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
              </Routes>
            </div>
          </Router>
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#333',
                color: '#fff',
              },
              success: {
                style: {
                  background: '#10B981',
                },
                iconTheme: {
                  primary: '#fff',
                  secondary: '#10B981',
                },
              },
              error: {
                style: {
                  background: '#EF4444',
                },
                duration: 5000,
              },
            }}
          />
        </AcademicProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
