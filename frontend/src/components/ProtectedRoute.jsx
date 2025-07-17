'use client';
import { useContext, useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { AuthContext } from './AuthContext';
import { toast } from 'react-toastify';

// Define route access configurations
const ROUTE_ACCESS = {
  '/admindashboard': {
    roles: ['SUPER_ADMIN', 'ADMIN'],
    permissions: ['manage_users']
  },
  '/managerdashboard': {
    roles: ['SUPER_ADMIN', 'ADMIN', 'MANAGER'],
    permissions: ['manage_employees']
  },
  '/employeepage': {
    roles: ['SUPER_ADMIN', 'ADMIN', 'MANAGER'],
    permissions: ['manage_employees']
  },
  '/addemployeepage': {
    roles: ['SUPER_ADMIN', 'ADMIN'],
    permissions: ['manage_employees']
  },
  '/updateemployeepage': {
    roles: ['SUPER_ADMIN', 'ADMIN'],
    permissions: ['manage_employees']
  }
  // Add more route configurations as needed
};

const ProtectedRoute = ({ children }) => {
  const router = useRouter();
  const pathname = usePathname();
  const { isAuthenticated, isLoading, hasRole, hasPermission, role } = useContext(AuthContext);

  useEffect(() => {
    const checkAccess = () => {
      // Public routes that don't need authentication
      const publicRoutes = ['/', '/login', '/signup', '/forgetpassword', '/publiccontact'];
      if (publicRoutes.includes(pathname)) {
        return true;
      }

      // Check if user is authenticated
      if (!isAuthenticated) {
        toast.error('Please login to access this page');
        router.push('/login');
        return false;
      }

      // Get route access configuration
      const routeConfig = ROUTE_ACCESS[pathname];
      if (!routeConfig) {
        // If no specific configuration, allow access to authenticated users
        return true;
      }

      // Check role access
      const hasValidRole = routeConfig.roles?.some(requiredRole => hasRole(requiredRole));
      if (!hasValidRole) {
        toast.error('You do not have permission to access this page');
        router.push(role === 'MANAGER' ? '/managerdashboard' : '/');
        return false;
      }

      // Check permissions
      const hasValidPermission = routeConfig.permissions?.some(permission => hasPermission(permission));
      if (!hasValidPermission) {
        toast.error('You do not have the required permissions');
        router.push(role === 'MANAGER' ? '/managerdashboard' : '/');
        return false;
      }

      return true;
    };

    if (!isLoading) {
      checkAccess();
    }
  }, [pathname, isAuthenticated, isLoading, hasRole, hasPermission, role, router]);

  // Show loading state
  if (isLoading) {
    return <div>Loading...</div>;
  }

  // Render children if all checks pass
  return children;
};

export default ProtectedRoute;