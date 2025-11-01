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

  const fetchEvents = useCallback(async () => {
    try {
      const response = await axios.get('/api/eventos/', {
        headers: { Authorization: `Bearer ${token}` },
      });
      const eventData = response.data.map(e => ({
        title: e.titulo,
        start: e.fecha_inicio,
        end: e.fecha_fin,
      }));
      setEvents(eventData);
    } catch (error) {
      console.error('Error fetching events', error);
    }
  }, [token]);

  useEffect(() => {
    fetchEvents();
  }, [fetchEvents]);

  return (
    <div>
      <h2>Calendario</h2>
      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        initialView="dayGridMonth"
        events={events}
      />
    </div>
  );
};

export default CalendarView;