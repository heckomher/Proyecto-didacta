import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

axios.defaults.baseURL = import.meta.env.VITE_API_URL || '/api';

const AuthContext = createContext();

export { AuthContext };

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [refreshToken, setRefreshToken] = useState(localStorage.getItem('refresh'));
  const [loading, setLoading] = useState(true);

  // Load user data on mount if token exists
  useEffect(() => {
    const loadUser = async () => {
      const storedToken = localStorage.getItem('token');
      if (storedToken) {
        try {
          const userResponse = await axios.get('/auth/user/', {
            headers: { Authorization: `Bearer ${storedToken}` },
          });
          setUser(userResponse.data);
        } catch (error) {
          console.error('Failed to load user', error);
          // Token might be invalid, clear it
          localStorage.removeItem('token');
          localStorage.removeItem('refresh');
          setToken(null);
          setRefreshToken(null);
        }
      }
      setLoading(false);
    };
    loadUser();
  }, []);

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [token]);

  // Axios interceptors: attach token and handle 401 with refresh
  useEffect(() => {
    const reqId = axios.interceptors.request.use((config) => {
      const t = localStorage.getItem('token');
      if (t && !config.headers?.Authorization) {
        config.headers = { ...(config.headers || {}), Authorization: `Bearer ${t}` };
      }
      return config;
    });

    const resId = axios.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config || {};
        // If unauthorized and we have refresh, try to refresh once
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          const r = localStorage.getItem('refresh');
          if (r) {
            try {
              const refreshResp = await axios.post('/auth/refresh/', { refresh: r });
              const newAccess = refreshResp.data.access;
              setToken(newAccess);
              localStorage.setItem('token', newAccess);
              axios.defaults.headers.common['Authorization'] = `Bearer ${newAccess}`;
              originalRequest.headers = { ...(originalRequest.headers || {}), Authorization: `Bearer ${newAccess}` };
              return axios(originalRequest);
            } catch (refreshErr) {
              // refresh failed - logout
              await logout();
            }
          } else {
            await logout();
          }
        }
        return Promise.reject(error);
      }
    );

    return () => {
      axios.interceptors.request.eject(reqId);
      axios.interceptors.response.eject(resId);
    };
  }, []);

  const login = async (username, password) => {
    try {
      const response = await axios.post('/auth/login/', { username, password });
      const { access, refresh } = response.data;
      setToken(access);
      setRefreshToken(refresh);
      localStorage.setItem('token', access);
      localStorage.setItem('refresh', refresh);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      // Fetch user info to get role
      const userResponse = await axios.get('/auth/user/', {
        headers: { Authorization: `Bearer ${access}` },
      });
      setUser(userResponse.data);
      localStorage.setItem('role', userResponse.data.role);
      return true;
    } catch (error) {
      console.error('Login failed', error);
      return false;
    }
  };

  const logout = async () => {
    try {
      await axios.post('/auth/logout/');
    } catch (error) {
      console.error('Logout failed', error);
    }
    setToken(null);
    setRefreshToken(null);
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('refresh');
    delete axios.defaults.headers.common['Authorization'];
  };

  const register = async (userData) => {
    try {
      await axios.post('/auth/register/', userData);
      return true;
    } catch (error) {
      console.error('Register failed', error);
      return false;
    }
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
};