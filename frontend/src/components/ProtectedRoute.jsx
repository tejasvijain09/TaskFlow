import React from 'react';
import { Navigate } from 'react-router-dom';

// Protect routes: ensures only logged-in users (or admins) can access
const ProtectedRoute = ({ children, adminOnly = false }) => {
  const token = localStorage.getItem('token');
  const userString = localStorage.getItem('user');

  // If no token or user data, redirect to login page
  if (!token || !userString) {
    return <Navigate to="/login" replace />;
  }

  const user = JSON.parse(userString);

  // If route is restricted to Admin only and current user is not Admin
  if (adminOnly && user.role !== 'Admin') {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

export default ProtectedRoute;
