'use client';
import React, { createContext, useState, useEffect, useCallback } from 'react';
import AxiosInstance from "@/components/AxiosInstance";
import { useRouter } from 'next/navigation';
import { toast } from 'react-toastify';

export const AuthContext = createContext();

// Define available roles and their hierarchy
const ROLE_HIERARCHY = {
  SUPER_ADMIN: ['ADMIN', 'MANAGER', 'USER'],
  ADMIN: ['MANAGER', 'USER'],
  MANAGER: ['USER'],
  USER: []
};

// Define permission sets for each role
const ROLE_PERMISSIONS = {
  SUPER_ADMIN: ['all'],
  ADMIN: [
    'manage_users',
    'manage_employees',
    'manage_products',
    'manage_categories',
    'view_reports',
    'manage_settings'
  ],
  MANAGER: [
    'manage_employees',
    'manage_products',
    'view_reports'
  ],
  USER: [
    'view_products',
    'view_categories'
  ]
};

export const AuthProvider = ({ children }) => {
  const router = useRouter();
  const [token, setToken] = useState(null);
  const [refreshToken, setRefreshToken] = useState(null);
  const [user, setUser] = useState(null);
  const [role, setRole] = useState(null);
  const [permissions, setPermissions] = useState({});
  const [isLoading, setIsLoading] = useState(true);

  // Load auth state from localStorage
  useEffect(() => {
    const loadAuthState = () => {
      try {
        const storedToken = localStorage.getItem('token');
        const storedRefreshToken = localStorage.getItem('refreshToken');
        const storedUser = localStorage.getItem('user');
        const storedRole = localStorage.getItem('role');
        const storedPermissions = localStorage.getItem('permissions');

        if (storedToken) setToken(JSON.parse(storedToken));
        if (storedRefreshToken) setRefreshToken(JSON.parse(storedRefreshToken));
        if (storedUser) setUser(JSON.parse(storedUser));
        if (storedRole) setRole(JSON.parse(storedRole));
        if (storedPermissions) setPermissions(JSON.parse(storedPermissions));
      } catch (error) {
        console.error('Error loading auth state:', error);
        // Clear potentially corrupted data
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('user');
        localStorage.removeItem('role');
        localStorage.removeItem('permissions');
      } finally {
        setIsLoading(false);
      }
    };

    loadAuthState();
  }, []);

  // Check if user has permission
  const hasPermission = useCallback((requiredPermission) => {
    if (!role || !permissions) return false;
    
    // Super admin has all permissions
    if (role === 'SUPER_ADMIN') return true;
    
    // Check if user has the specific permission
    if (Array.isArray(permissions)) {
      return permissions.includes(requiredPermission);
    }
    
    return false;
  }, [role, permissions]);

  // Check if user has role
  const hasRole = useCallback((requiredRole) => {
    if (!role) return false;
    
    // Check if user has the exact role
    if (role === requiredRole) return true;
    
    // Check if user's role is higher in hierarchy
    const higherRoles = ROLE_HIERARCHY[role] || [];
    return higherRoles.includes(requiredRole);
  }, [role]);

  // Login function
  const login = useCallback(async (credentials) => {
    try {
      const response = await AxiosInstance.post('/user/login', credentials);
      const { token: newToken, refresh_token, user: userData, role: userRole, permissions: userPermissions } = response.data.data;

      // Store in localStorage
      localStorage.setItem('token', JSON.stringify(newToken));
      localStorage.setItem('refreshToken', JSON.stringify(refresh_token));
      localStorage.setItem('user', JSON.stringify(userData));
      localStorage.setItem('role', JSON.stringify(userRole));
      localStorage.setItem('permissions', JSON.stringify(userPermissions));

      // Update state
      setToken(newToken);
      setRefreshToken(refresh_token);
      setUser(userData);
      setRole(userRole);
      setPermissions(userPermissions);

      // Show success message
      toast.success('Login successful!');

      // Redirect based on role
      switch(userRole) {
        case 'SUPER_ADMIN':
        case 'ADMIN':
          router.push('/admindashboard');
          break;
        case 'MANAGER':
          router.push('/managerdashboard');
          break;
        default:
          router.push('/');
      }
    } catch (error) {
      console.error('Login error:', error);
      toast.error(error.response?.data?.message || 'Login failed');
      throw error;
    }
  }, [router]);

  // Logout function
  const logout = useCallback(async () => {
    try {
      if (token) {
        await AxiosInstance.post('/user/logout');
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear localStorage
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('user');
      localStorage.removeItem('role');
      localStorage.removeItem('permissions');

      // Reset state
      setToken(null);
      setRefreshToken(null);
      setUser(null);
      setRole(null);
      setPermissions({});

      // Show success message
      toast.success('Logged out successfully');

      // Redirect to home
      router.push('/');
    }
  }, [token, router]);

  // Register function
  const register = useCallback(async (userData) => {
    try {
      const response = await AxiosInstance.post('/user/register', userData);
      toast.success('Registration successful! Please login.');
      return response.data;
    } catch (error) {
      console.error('Registration error:', error);
      toast.error(error.response?.data?.message || 'Registration failed');
      throw error;
    }
  }, []);

  // Context value
  const value = {
    token,
    user,
    role,
    permissions,
    isLoading,
    isAuthenticated: !!token,
    login,
    logout,
    register,
    hasPermission,
    hasRole,
  };

  // Loading state
  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
