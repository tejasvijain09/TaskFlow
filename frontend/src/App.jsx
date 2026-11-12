import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import io from 'socket.io-client';

// Page components
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Tasks from './pages/Tasks';
import Admin from './pages/Admin';

// Route guard component
import ProtectedRoute from './components/ProtectedRoute';

function AppContent() {
  // Real-time notification toast state
  const [notification, setNotification] = useState(null);
  const location = useLocation();

  /**
   * Socket.IO Real-Time Flow:
   * 1. Check if user is logged in (user in localStorage).
   * 2. Re-evaluated whenever location.pathname changes (e.g. after logging in).
   * 3. Connect client socket to backend at http://localhost:5001.
   * 4. Emit 'join' event passing user._id so backend adds socket to a private room.
   * 5. Listen for 'taskStatusUpdated' event emitted when task status changes in database.
   * 6. Render floating notification toast auto-dismissed after 5 seconds.
   */
  useEffect(() => {
    const userString = localStorage.getItem('user');
    if (!userString) return;

    const user = JSON.parse(userString);
    const socket = io('http://localhost:5001');

    socket.on('connect', () => {
      // Join user's personal room
      socket.emit('join', user._id);
    });

    // Listen for real-time task status updates
    socket.on('taskStatusUpdated', (data) => {
      setNotification({
        title: data.title,
        message: data.message || `Status updated to ${data.newStatus}`
      });

      // Automatically hide notification after 5 seconds
      setTimeout(() => {
        setNotification(null);
      }, 5000);
    });

    return () => {
      socket.disconnect();
    };
  }, [location.pathname]);

  return (
    <>
      {/* Real-time Socket.IO notification banner */}
      {notification && (
        <div className="realtime-toast">
          <div className="toast-icon">🔔</div>
          <div className="toast-content">
            <h4>Real-time Task Update</h4>
            <p>{notification.message}</p>
          </div>
          <button
            className="toast-close"
            onClick={() => setNotification(null)}
          >
            ✕
          </button>
        </div>
      )}

      <Routes>
        {/* Public authentication routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected user routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/tasks"
          element={
            <ProtectedRoute>
              <Tasks />
            </ProtectedRoute>
          }
        />

        {/* Protected administrator route */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute adminOnly={true}>
              <Admin />
            </ProtectedRoute>
          }
        />

        {/* Default route redirect */}
        <Route
          path="*"
          element={
            localStorage.getItem('token') ? (
              <Navigate to="/dashboard" replace />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
      </Routes>
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;
