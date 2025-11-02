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
  return token ? children : <Navigate to="/login" />;
};

const Dashboard = () => {
  const { user } = useAuth();
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
          <div className="App min-h-screen bg-academic-light dark:bg-academic-dark">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/calendar" element={<ProtectedRoute><Navbar /><CalendarView /></ProtectedRoute>} />
              <Route path="/" element={<ProtectedRoute><Navbar /><Dashboard /></ProtectedRoute>} />
            </Routes>
          </div>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
