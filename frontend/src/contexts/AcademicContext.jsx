import React, { createContext, useContext, useState, useEffect } from 'react';
import { utilService, anioAcademicoService } from '../services/api';

const AcademicContext = createContext();

export const useAcademic = () => {
  const context = useContext(AcademicContext);
  if (!context) {
    throw new Error('useAcademic must be used within an AcademicProvider');
  }
  return context;
};

export const AcademicProvider = ({ children }) => {
  const [anioActivo, setAnioActivo] = useState(null);
  const [configuracionValida, setConfiguracionValida] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Verificar configuración académica al cargar
  useEffect(() => {
    const verificarConfiguracion = async () => {
      try {
        setLoading(true);
        setError(null);

        // Verificar configuración académica
        const config = await utilService.verificarConfiguracionAcademica();
        setConfiguracionValida(config.configurado);

        if (config.configurado && config.anio_academico) {
          setAnioActivo(config.anio_academico);
        } else {
          // Intentar obtener año activo directamente
          try {
            const activo = await anioAcademicoService.getActivo();
            setAnioActivo(activo);
            setConfiguracionValida(true);
          } catch (err) {
            if (err.response?.status !== 404) {
              console.error('Error al obtener año activo:', err);
            }
            setAnioActivo(null);
            setConfiguracionValida(false);
          }
        }
      } catch (err) {
        console.error('Error al verificar configuración:', err);
        setError(err.message);
        setConfiguracionValida(false);
      } finally {
        setLoading(false);
      }
    };

    verificarConfiguracion();
  }, []);

  // Función para refrescar la configuración
  const refreshConfiguration = async () => {
    try {
      setLoading(true);
      const config = await utilService.verificarConfiguracionAcademica();
      setConfiguracionValida(config.configurado);
      
      if (config.configurado && config.anio_academico) {
        setAnioActivo(config.anio_academico);
      }
      
      return config;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Función para activar un año académico
  const activarAnio = async (anioId) => {
    try {
      const anioActivado = await anioAcademicoService.activar(anioId);
      setAnioActivo(anioActivado);
      setConfiguracionValida(true);
      return anioActivado;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  // Función para cerrar un año académico
  const cerrarAnio = async (anioId, password) => {
    try {
      const anioCerrado = await anioAcademicoService.cerrar(anioId, password);
      // Si cerramos el año activo, necesitamos actualizar el estado
      if (anioActivo && anioActivo.id === anioId) {
        setAnioActivo(prev => ({ ...prev, estado: 'CERRADO' }));
      }
      return anioCerrado;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  // Validar si se puede crear planificaciones
  const canCreatePlanificaciones = () => {
    return configuracionValida && anioActivo && anioActivo.estado === 'ACTIVO';
  };

  // Obtener mensaje de estado de configuración
  const getConfigurationMessage = () => {
    if (loading) return 'Verificando configuración...';
    if (error) return `Error en configuración: ${error}`;
    if (!configuracionValida) return 'No hay configuración académica válida';
    if (!anioActivo) return 'No hay año académico activo';
    if (anioActivo.estado !== 'ACTIVO') return `Año académico en estado: ${anioActivo.estado}`;
    return 'Configuración válida';
  };

  const value = {
    // Estado
    anioActivo,
    configuracionValida,
    loading,
    error,
    
    // Funciones
    refreshConfiguration,
    activarAnio,
    cerrarAnio,
    canCreatePlanificaciones,
    getConfigurationMessage,
    
    // Utilidades
    setError,
  };

  return (
    <AcademicContext.Provider value={value}>
      {children}
    </AcademicContext.Provider>
  );
};