import apiClient from './apiClient.js';

export const registerUser = async (payload) => {
  const { data } = await apiClient.post('/api/auth/register', payload);
  return data;
};

export const loginUser = async (payload) => {
  const { data } = await apiClient.post('/api/auth/login', payload);
  return data;
};

export const fetchProfile = async () => {
  const { data } = await apiClient.get('/api/auth/profile');
  return data;
};

export const updateProfile = async (payload) => {
  const { data } = await apiClient.put('/api/auth/profile', payload);
  return data;
};

export const verifyToken = async () => {
  const { data } = await apiClient.post('/api/auth/verify-token');
  return data;
};
