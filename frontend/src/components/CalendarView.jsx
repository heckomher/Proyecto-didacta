import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../hooks/useAuth';
import axios from 'axios';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';

const CalendarView = () => {
  const { token } = useAuth();
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [anioActivo, setAnioActivo] = useState(null);

  const fetchAnioActivo = useCallback(async () => {
    try {
      const response = await axios.get('/api/anios-academicos/activo/');
      setAnioActivo(response.data);
    } catch (error) {
      console.error('Error fetching año activo', error);
    }
  }, []);

  const fetchEvents = useCallback(async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/eventos/', {
        headers: { Authorization: `Bearer ${token}` },
      });
      const eventData = response.data.map(e => ({
        title: e.titulo,
        start: e.fecha_inicio,
        end: e.fecha_fin,
        color: getEventColor(e.tipo),
        extendedProps: { tipo: 'evento' }
      }));
      setEvents(eventData);
    } catch (error) {
      console.error('Error fetching events', error);
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    fetchAnioActivo();
    fetchEvents();
  }, [fetchAnioActivo, fetchEvents]);

  const getEventColor = (tipo) => {
    const colors = {
      CURSO: '#2563eb', // primary-600
      TALLER: '#7c3aed', // secondary-600
      SEMINARIO: '#059669', // green-600
      periodo: '#6366f1', // indigo-500
      feriado: '#dc2626', // red-600
      vacaciones: '#f59e0b', // amber-500
    };
    return colors[tipo] || '#6b7280'; // gray-500
  };

  // Combinar eventos del año académico con eventos regulares
  const allEvents = React.useMemo(() => {
    const academicEvents = [];

    if (anioActivo) {
      // Agregar periodos académicos
      anioActivo.periodos?.forEach(periodo => {
        academicEvents.push({
          title: `📚 ${periodo.nombre}`,
          start: periodo.fecha_inicio,
          end: periodo.fecha_fin,
          color: getEventColor('periodo'),
          display: 'background',
          extendedProps: { tipo: 'periodo' }
        });
      });

      // Agregar feriados
      anioActivo.feriados?.forEach(feriado => {
        academicEvents.push({
          title: `🎉 ${feriado.nombre}`,
          start: feriado.fecha,
          allDay: true,
          color: getEventColor('feriado'),
          extendedProps: { tipo: 'feriado' }
        });
      });

      // Agregar vacaciones
      anioActivo.vacaciones?.forEach(vacacion => {
        academicEvents.push({
          title: `🏖️ ${vacacion.nombre}`,
          start: vacacion.fecha_inicio,
          end: vacacion.fecha_fin,
          color: getEventColor('vacaciones'),
          display: 'background',
          extendedProps: { tipo: 'vacaciones' }
        });
      });
    }

    return [...events, ...academicEvents];
  }, [events, anioActivo]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white font-serif">Calendario Académico</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">Vista de todas las planificaciones y eventos</p>
      </div>

      {/* Legend */}
      <div className="card p-4 mb-6">
        <div className="flex flex-wrap items-center gap-6 text-sm">
          <span className="font-medium text-gray-700 dark:text-gray-300">Leyenda:</span>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-primary-600"></div>
            <span className="text-gray-600 dark:text-gray-400">Curso</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-secondary-600"></div>
            <span className="text-gray-600 dark:text-gray-400">Taller</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-green-600"></div>
            <span className="text-gray-600 dark:text-gray-400">Seminario</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-indigo-500"></div>
            <span className="text-gray-600 dark:text-gray-400">📚 Periodo Académico</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-red-600"></div>
            <span className="text-gray-600 dark:text-gray-400">🎉 Feriado</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-amber-500"></div>
            <span className="text-gray-600 dark:text-gray-400">🏖️ Vacaciones</span>
          </div>
        </div>
      </div>

      {/* Calendar */}
      <div className="card p-6">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <svg className="animate-spin h-8 w-8 text-primary-600" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
        ) : (
          <div className="calendar-wrapper">
            <FullCalendar
              plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
              initialView="dayGridMonth"
              events={allEvents}
              headerToolbar={{
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay'
              }}
              height="auto"
              locale="es"
              buttonText={{
                today: 'Hoy',
                month: 'Mes',
                week: 'Semana',
                day: 'Día'
              }}
              eventTimeFormat={{
                hour: '2-digit',
                minute: '2-digit',
                meridiem: false
              }}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default CalendarView;