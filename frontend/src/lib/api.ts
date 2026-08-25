import axios from 'axios';
import { useAuthStore } from '@/store/authStore';

export const API_ORIGIN = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const getImageUrl = (path: string): string => {
  if (path.startsWith('http')) return path;
  return `${API_ORIGIN}${path}`;
};

export const api = axios.create({
  baseURL: `${API_ORIGIN}/api`,
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