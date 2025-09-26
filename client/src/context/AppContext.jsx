import { createContext, useContext, useMemo, useState, useCallback, useEffect } from 'react';
import { setAuthToken } from '../services/apiClient.js';

const AppContext = createContext(null);

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within AppProvider');
  }
  return context;
};

let notificationId = 0;

export const AppProvider = ({ children }) => {
  const getStoredValue = (key, parseJson = false) => {
    if (typeof window === 'undefined') return null;
    const raw = window.localStorage.getItem(key);
    if (!raw) return null;
    if (parseJson) {
      try {
        return JSON.parse(raw);
      } catch (err) {
        return null;
      }
    }
    return raw;
  };

  const [token, setToken] = useState(() => getStoredValue('resumetric_token'));
  const [user, setUser] = useState(() => getStoredValue('resumetric_user', true));
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [notifications, setNotifications] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [reports, setReports] = useState([]);
  const [activeReport, setActiveReport] = useState(null);

  useEffect(() => {
    setAuthToken(token);
    if (typeof window === 'undefined') return;
    if (token) {
      window.localStorage.setItem('resumetric_token', token);
    } else {
      window.localStorage.removeItem('resumetric_token');
    }
  }, [token]);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    if (user) {
      window.localStorage.setItem('resumetric_user', JSON.stringify(user));
    } else {
      window.localStorage.removeItem('resumetric_user');
    }
  }, [user]);

  const addNotification = useCallback((message, type = 'success') => {
    notificationId += 1;
    const id = notificationId;
    setNotifications((prev) => [...prev, { id, message, type, open: true }]);
    return id;
  }, []);

  const closeNotification = useCallback((id) => {
    setNotifications((prev) => prev.map((notif) => (notif.id === id ? { ...notif, open: false } : notif)));
    setTimeout(() => {
      setNotifications((prev) => prev.filter((notif) => notif.id !== id));
    }, 250);
  }, []);

  const showLoader = useCallback(() => setIsLoading(true), []);
  const hideLoader = useCallback(() => setIsLoading(false), []);

  const saveSession = useCallback((authToken, userData) => {
    setAuthToken(authToken || null);
    setToken(authToken || null);
    setUser(userData || null);
  }, []);

  const clearSession = useCallback(() => {
    setAuthToken(null);
    setToken(null);
    setUser(null);
    setReports([]);
    setActiveReport(null);
    setCurrentPage('dashboard');
  }, []);

  const value = useMemo(() => ({
    token,
    setToken,
    user,
    setUser,
    currentPage,
    setCurrentPage,
    notifications,
    addNotification,
    closeNotification,
    isLoading,
    showLoader,
    hideLoader,
    reports,
    setReports,
    activeReport,
    setActiveReport,
    saveSession,
    clearSession
  }), [
    token,
    user,
    currentPage,
    notifications,
    addNotification,
    closeNotification,
    isLoading,
    showLoader,
    hideLoader,
    reports,
    activeReport,
    saveSession,
    clearSession
  ]);

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};
