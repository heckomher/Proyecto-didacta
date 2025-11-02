import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import { useAuth } from './hooks/useAuth';
import Login from './components/Login';
import Register from './components/Register';
import DashboardDocente from './components/DashboardDocente';
import DashboardUTP from './components/DashboardUTP';
import CalendarView from './components/CalendarView';
import Navbar from './components/Navbar';
import './App.css';

const ProtectedRoute = ({ children }) => {
  const { token } = useAuth();
  return token ? (
    <>
      <Navbar />
      {children}
    </>
  ) : <Navigate to="/login" />;
};

const Dashboard = () => {
  const { user } = useAuth();
  
  // Redirect superusers to Django admin
  if (user && user.is_superuser) {
    window.location.href = 'http://localhost:8000/admin/';
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Redirigiendo al panel de administración...</p>
        </div>
      </div>
    );
  }
  
  if (user && user.role === 'UTP') {
    return <DashboardUTP />;
  }
  return <DashboardDocente />;
};

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <div className="App min-h-screen bg-gray-50 dark:bg-gray-900">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/calendar" element={<ProtectedRoute><CalendarView /></ProtectedRoute>} />
              <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
            </Routes>
          </div>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
