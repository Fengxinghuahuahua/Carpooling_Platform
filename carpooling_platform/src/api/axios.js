import axios from 'axios';
import { ElMessage } from 'element-plus';
import router from '@/router/index';

const service = axios.create({
  timeout: 10000,
});


service.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token'); 

    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    return config;
  },
  error => {
    console.log(error);
    return Promise.reject(error);
  }
);


service.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if (error.response && error.response.status === 401) {
      ElMessage.error('登录状态已过期，请重新登录');
      localStorage.removeItem('token');
      router.push('/login');
    }
    return Promise.reject(error);
  }
);

export default service;