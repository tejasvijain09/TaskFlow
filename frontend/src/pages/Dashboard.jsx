import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Navbar from '../components/Navbar';
import API from '../services/api';

const Dashboard = () => {
  // State for statistics and recent tasks
  const [stats, setStats] = useState({
    totalTasks: 0,
    pendingTasks: 0,
    inProgressTasks: 0,
    completedTasks: 0,
    overdueTasks: 0,
    recentTasks: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Fetch statistics from backend API
  const fetchDashboardStats = async () => {
    try {
      setLoading(true);
      setError('');
      const res = await API.get('/dashboard/stats');
      setStats(res.data);
    } catch (err) {
      console.error('Failed to fetch dashboard statistics:', err);
      setError('Could not load dashboard data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  // Format date helper
  const formatDate = (dateString) => {
    if (!dateString) return '—';
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  return (
    <div className="app-layout">
      <Sidebar />

      <div className="main-wrapper">
        <Navbar title="Dashboard Overview" />

        <main className="content-container">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
            <div>
              <h2 style={{ fontSize: '22px', fontWeight: 700, color: '#0f172a' }}>Welcome to TaskFlow</h2>
              <p style={{ color: '#64748b', fontSize: '14px' }}>Here is a summary of your task workload</p>
            </div>
            <button onClick={fetchDashboardStats} className="btn btn-secondary btn-sm">
              🔄 Refresh Stats
            </button>
          </div>

          {error && <div className="alert-error">{error}</div>}

          {/* Statistic Cards */}
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-info">
                <h3>Total Tasks</h3>
                <div className="stat-number">{stats.totalTasks}</div>
              </div>
              <div className="stat-icon icon-total">📁</div>
            </div>

            <div className="stat-card">
              <div className="stat-info">
                <h3>Pending</h3>
                <div className="stat-number">{stats.pendingTasks}</div>
              </div>
              <div className="stat-icon icon-pending">⏳</div>
            </div>

            <div className="stat-card">
              <div className="stat-info">
                <h3>In Progress</h3>
                <div className="stat-number">{stats.inProgressTasks}</div>
              </div>
              <div className="stat-icon icon-progress">🚀</div>
            </div>

            <div className="stat-card">
              <div className="stat-info">
                <h3>Completed</h3>
                <div className="stat-number">{stats.completedTasks}</div>
              </div>
              <div className="stat-icon icon-completed">✅</div>
            </div>

            <div className="stat-card">
              <div className="stat-info">
                <h3>Overdue</h3>
                <div className="stat-number" style={{ color: '#b91c1c' }}>
                  {stats.overdueTasks || 0}
                </div>
              </div>
              <div className="stat-icon icon-overdue">⚠️</div>
            </div>
          </div>

          {/* Priority Tasks Section */}
          <div className="table-card">
            <div className="table-header">
              <div>
                <h3>Priority Tasks</h3>
                <small style={{ color: '#64748b' }}>High priority pending and overdue tasks are prioritized</small>
              </div>
              <Link to="/tasks" className="btn btn-primary btn-sm">
                Manage All Tasks →
              </Link>
            </div>

            {loading ? (
              <div style={{ padding: '32px', textAlign: 'center', color: '#64748b' }}>
                Loading priority tasks...
              </div>
            ) : stats.recentTasks.length === 0 ? (
              <div className="empty-state">
                <h3>No tasks created yet</h3>
                <p>Start organizing your work by adding your first task!</p>
                <Link to="/tasks" className="btn btn-primary btn-sm" style={{ marginTop: '12px' }}>
                  + Create Task
                </Link>
              </div>
            ) : (
              <table className="custom-table">
                <thead>
                  <tr>
                    <th>Title</th>
                    <th>Status</th>
                    <th>Priority</th>
                    <th>Due Date</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.recentTasks.map((task) => (
                    <tr key={task._id}>
                      <td style={{ fontWeight: 600 }}>{task.title}</td>
                      <td>
                        <span
                          className={`badge ${
                            task.status === 'Completed'
                              ? 'badge-completed'
                              : task.status === 'In Progress'
                              ? 'badge-in-progress'
                              : task.status === 'Overdue'
                              ? 'badge-overdue'
                              : 'badge-pending'
                          }`}
                        >
                          {task.status}
                        </span>
                      </td>
                      <td>
                        <span
                          className={`badge ${
                            task.priority === 'High'
                              ? 'badge-priority-high'
                              : task.priority === 'Low'
                              ? 'badge-priority-low'
                              : 'badge-priority-medium'
                          }`}
                        >
                          {task.priority}
                        </span>
                      </td>
                      <td>{formatDate(task.dueDate)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </main>
      </div>
    </div>
  );
};

export default Dashboard;
