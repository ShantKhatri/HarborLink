import axios from 'axios';

const baseURL = '/api';
const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;