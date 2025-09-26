import axios from 'axios';

export const BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000').replace(/\/$/, '');

const apiClient = axios.create({
  baseURL: BASE_URL,
  withCredentials: false
});

export const setAuthToken = (token) => {
  if (token) {
    apiClient.defaults.headers.common.Authorization = `Bearer ${token}`;
  } else {
    delete apiClient.defaults.headers.common.Authorization;
  }
};

export const extractErrorMessage = (error) => {
  if (!error) return 'An unknown error occurred';
  if (error.response?.data) {
    const data = error.response.data;
    return data.error || data.message || JSON.stringify(data);
  }
  if (error.message) {
    return error.message;
  }
  return 'An unknown error occurred';
};

export default apiClient;
