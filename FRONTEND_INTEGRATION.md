# Frontend Integratsiya - Render Sleep Mode ga Moslashgan

## ⚠️ Render Free Plan Xususiyatlari

- **Sleep Mode:** 15 daqiqa inactivity dan keyin
- **Wake-up Time:** 30-60 sekund
- **Cold Start:** Birinchi request sekin

---

## 🔧 **Axios Configuration (Retry Logic)**

### **React/React Native uchun:**

```javascript
// api/client.js
import axios from 'axios';

const API_URL = 'https://madinabonu-backend.onrender.com';

// Axios instance yaratish
const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 90000, // 90 sekund - Render wake-up uchun
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - token qo'shish
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - retry logic
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Timeout yoki network error bo'lsa retry qilish
    if (
      (error.code === 'ECONNABORTED' ||
       error.message === 'Network Error' ||
       error.response?.status === 503) &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;
      originalRequest.timeout = 120000; // 2 daqiqa

      console.log('Render waking up... Retrying...');

      // 5 sekund kutib, qayta urinish
      await new Promise((resolve) => setTimeout(resolve, 5000));

      return apiClient(originalRequest);
    }

    // Token muddati tugagan bo'lsa
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });

        const { access_token } = response.data;
        localStorage.setItem('access_token', access_token);

        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        // Logout
        localStorage.clear();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
```

---

## 🚀 **Health Check Hook (React)**

```javascript
// hooks/useHealthCheck.js
import { useState, useEffect } from 'react';
import apiClient from '../api/client';

export const useHealthCheck = () => {
  const [isServerAwake, setIsServerAwake] = useState(false);
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await apiClient.get('/', { timeout: 90000 });
        if (response.data.status === 'ok') {
          setIsServerAwake(true);
        }
      } catch (error) {
        console.error('Health check failed:', error);
        // Retry after 5 seconds
        setTimeout(checkHealth, 5000);
      } finally {
        setIsChecking(false);
      }
    };

    checkHealth();
  }, []);

  return { isServerAwake, isChecking };
};
```

---

## 📱 **Login Component (with Loading State)**

```javascript
// components/Login.jsx
import React, { useState } from 'react';
import apiClient from '../api/client';
import { useHealthCheck } from '../hooks/useHealthCheck';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const { isServerAwake, isChecking } = useHealthCheck();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await apiClient.post('/auth/login', {
        username,
        password,
      });

      const { access_token, refresh_token } = response.data;

      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);

      // Redirect
      window.location.href = '/dashboard';
    } catch (err) {
      if (err.code === 'ECONNABORTED') {
        setError('Server uyg\'onmoqda, iltimos kutib turing...');
      } else {
        setError(err.response?.data?.detail || 'Login xatosi');
      }
    } finally {
      setLoading(false);
    }
  };

  if (isChecking) {
    return (
      <div className="loading-screen">
        <div className="spinner" />
        <p>Server tekshirilmoqda...</p>
      </div>
    );
  }

  return (
    <div className="login-container">
      <h2>Login</h2>

      {!isServerAwake && (
        <div className="alert alert-warning">
          Server uyg'onmoqda, iltimos 30-60 sekund kuting...
        </div>
      )}

      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        {error && <div className="alert alert-error">{error}</div>}

        <button type="submit" disabled={loading || !isServerAwake}>
          {loading ? 'Yuklanmoqda...' : 'Kirish'}
        </button>
      </form>
    </div>
  );
};

export default Login;
```

---

## 📲 **React Native (TrainingApp uchun)**

```javascript
// services/api.js
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_URL = 'https://madinabonu-backend.onrender.com';

const api = axios.create({
  baseURL: API_URL,
  timeout: 90000, // 90 sekund
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor with retry
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Render wake-up retry
    if (
      (error.code === 'ECONNABORTED' || !error.response) &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;
      originalRequest.timeout = 120000;

      console.log('🔄 Render waking up, retrying...');

      // 5 sekund kutish
      await new Promise((resolve) => setTimeout(resolve, 5000));

      return api(originalRequest);
    }

    // Token refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = await AsyncStorage.getItem('refresh_token');
        const response = await axios.post(`${API_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });

        const { access_token } = response.data;
        await AsyncStorage.setItem('auth_token', access_token);

        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Logout
        await AsyncStorage.clear();
        // Navigate to login
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
```

---

## 🔄 **Custom Hook - React Native**

```javascript
// hooks/useApi.js
import { useState, useCallback } from 'react';
import api from '../services/api';

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const request = useCallback(async (method, url, data = null) => {
    setLoading(true);
    setError(null);

    try {
      const response = await api({
        method,
        url,
        data,
      });

      setLoading(false);
      return response.data;
    } catch (err) {
      setLoading(false);

      if (err.code === 'ECONNABORTED') {
        setError('Server uyg\'onmoqda, iltimos kutib turing...');
      } else {
        setError(err.response?.data?.detail || 'Xatolik yuz berdi');
      }

      throw err;
    }
  }, []);

  return { request, loading, error };
};
```

---

## 🎯 **Usage Example**

```javascript
// screens/LoginScreen.js
import React, { useState } from 'react';
import { View, TextInput, Button, Text, ActivityIndicator } from 'react-native';
import { useApi } from '../hooks/useApi';

const LoginScreen = ({ navigation }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { request, loading, error } = useApi();

  const handleLogin = async () => {
    try {
      const data = await request('POST', '/auth/login', {
        username,
        password,
      });

      await AsyncStorage.setItem('auth_token', data.access_token);
      navigation.navigate('Home');
    } catch (err) {
      // Error allaqachon state da
    }
  };

  return (
    <View>
      <TextInput
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
      />
      <TextInput
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />

      {error && <Text style={{ color: 'red' }}>{error}</Text>}

      {loading ? (
        <ActivityIndicator size="large" />
      ) : (
        <Button title="Login" onPress={handleLogin} />
      )}
    </View>
  );
};

export default LoginScreen;
```

---

## ⏰ **Timeout Sozlamalari**

```javascript
const TIMEOUTS = {
  NORMAL: 30000,        // 30 sek - normal requests
  WAKE_UP: 90000,       // 90 sek - cold start
  RETRY: 120000,        // 2 min - retry
  UPLOAD: 300000,       // 5 min - file uploads
};
```

---

## 🔔 **User Notification**

```javascript
// utils/notifications.js
export const showWakeUpMessage = () => {
  return {
    title: 'Server uyg\'onmoqda',
    message: 'Iltimos 30-60 sekund kuting. Bu faqat birinchi requestda sodir bo\'ladi.',
    type: 'info',
  };
};
```

---

## 📊 **Summary**

| Sozlama | Qiymat | Sabab |
|---------|--------|-------|
| **timeout** | 90 sek | Render wake-up vaqti |
| **retry delay** | 5 sek | Server stabilizatsiya |
| **max retries** | 1 | Ortiqcha yuklama oldini olish |
| **retry timeout** | 120 sek | Ikkinchi urinish |

---

**Endi frontendingizda uzun timeout va retry logic ishlatishingiz mumkin! 🚀**