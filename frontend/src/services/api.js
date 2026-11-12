import axios from 'axios';

// Create an Axios instance with base URL pointing to Express backend
const API = axios.create({
  baseURL: 'http://localhost:5001/api'
});

// Request interceptor to automatically attach JWT token to every request
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle common errors like expired token
API.interceptors.response.use(
  (response) => response,
  (error) => {
    // If token expired or unauthorized, clear storage and redirect to login
    if (error.response && error.response.status === 401) {
      if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default API;
