import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';

const Sidebar = () => {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <NavLink to="/dashboard" className="brand-logo">
          <span>⚡ TaskFlow</span>
          <span className="brand-badge">MERN</span>
        </NavLink>
      </div>

      <nav className="sidebar-nav">
        <NavLink
          to="/dashboard"
          className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}
        >
          <span>📊</span>
          <span>Dashboard</span>
        </NavLink>

        <NavLink
          to="/tasks"
          className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}
        >
          <span>📋</span>
          <span>My Tasks</span>
        </NavLink>

        {/* Admin only link */}
        {user.role === 'Admin' && (
          <NavLink
            to="/admin"
            className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}
          >
            <span>🛡️</span>
            <span>Admin Panel</span>
          </NavLink>
        )}
      </nav>

      <div className="sidebar-footer">
        <div className="user-snippet">
          <span className="user-name">{user.name || 'User'}</span>
          <span className={`user-role-badge ${user.role === 'Admin' ? 'role-admin' : 'role-user'}`}>
            {user.role || 'User'}
          </span>
        </div>
        <button onClick={handleLogout} className="btn btn-secondary btn-sm" style={{ width: '100%' }}>
          🚪 Logout
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
