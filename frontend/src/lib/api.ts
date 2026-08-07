import axios from 'axios';
import { useAuthStore } from '@/store/authStore';

export const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

// Attach the JWT to every outgoing request automatically
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});


api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status;
    const hadAuthHeader = Boolean(error.config?.headers?.Authorization);

    if (status === 401 && hadAuthHeader) {
      useAuthStore.getState().logout();
    }

    const errorData = error.response?.data;
    return Promise.reject(errorData || { error: { message: 'Network connection error' } });
  }
);