import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import Navbar from '../components/Navbar';
import API from '../services/api';

const Admin = () => {
  const [users, setUsers] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [activeTab, setActiveTab] = useState('tasks'); // 'tasks' or 'users'
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Fetch registered users
  const fetchUsers = async () => {
    try {
      setLoading(true);
      const res = await API.get('/admin/users');
      setUsers(res.data);
    } catch (err) {
      console.error('Admin users fetch error:', err);
      setMessage('Failed to load registered users');
    } finally {
      setLoading(false);
    }
  };

  // Fetch all tasks across platform
  const fetchTasks = async () => {
    try {
      setLoading(true);
      const res = await API.get('/admin/tasks');
      setTasks(res.data);
    } catch (err) {
      console.error('Admin tasks fetch error:', err);
      setMessage('Failed to load system tasks');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
    fetchTasks();
  }, []);

  // Admin delete task action
  const handleDeleteTask = async (taskId) => {
    const confirmDelete = window.confirm(
      'Administrator Action: Are you sure you want to remove this task from the system?'
    );
    if (!confirmDelete) return;

    try {
      await API.delete(`/admin/tasks/${taskId}`);
      setMessage('Task deleted successfully by administrator');
      fetchTasks();
      setTimeout(() => setMessage(''), 3000);
    } catch (err) {
      console.error('Admin delete error:', err);
      setMessage('Failed to delete task');
    }
  };

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
        <Navbar title="Administrator Control Panel" />

        <main className="content-container">
          <div style={{ marginBottom: '24px' }}>
            <h2 style={{ fontSize: '22px', fontWeight: 700, color: '#0f172a' }}>
              System Administration
            </h2>
            <p style={{ color: '#64748b', fontSize: '14px' }}>
              Inspect and moderate all registered users and tasks platform-wide.
            </p>
          </div>

          {/* Feedback banner */}
          {message && (
            <div
              style={{
                backgroundColor: '#dbeafe',
                border: '1px solid #bfdbfe',
                color: '#1e40af',
                padding: '10px 16px',
                borderRadius: '8px',
                marginBottom: '20px',
                fontSize: '14px'
              }}
            >
              {message}
            </div>
          )}

          {/* Tab selector buttons */}
          <div style={{ display: 'flex', gap: '12px', marginBottom: '20px' }}>
            <button
              className={`btn ${activeTab === 'tasks' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setActiveTab('tasks')}
            >
              📋 All System Tasks ({tasks.length})
            </button>
            <button
              className={`btn ${activeTab === 'users' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setActiveTab('users')}
            >
              👥 Registered Users ({users.length})
            </button>
          </div>

          {/* Tab 1: All System Tasks */}
          {activeTab === 'tasks' && (
            <div className="table-card">
              <div className="table-header">
                <h3>All Platform Tasks</h3>
                <button onClick={fetchTasks} className="btn btn-secondary btn-sm">
                  🔄 Refresh
                </button>
              </div>

              {loading ? (
                <div style={{ padding: '40px', textAlign: 'center', color: '#64748b' }}>
                  Loading all tasks...
                </div>
              ) : tasks.length === 0 ? (
                <div className="empty-state">
                  <h3>No tasks in the system</h3>
                </div>
              ) : (
                <table className="custom-table">
                  <thead>
                    <tr>
                      <th>Title</th>
                      <th>Owner / User</th>
                      <th>Status</th>
                      <th>Priority</th>
                      <th>Due Date</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {tasks.map((task) => (
                      <tr key={task._id}>
                        <td style={{ fontWeight: 600 }}>{task.title}</td>
                        <td>
                          {task.user ? (
                            <div>
                              <div>{task.user.name}</div>
                              <small style={{ color: '#64748b' }}>{task.user.email}</small>
                            </div>
                          ) : (
                            <em style={{ color: '#94a3b8' }}>Unknown User</em>
                          )}
                        </td>
                        <td>
                          <span
                            className={`badge ${
                              task.status === 'Completed'
                                ? 'badge-completed'
                                : task.status === 'In Progress'
                                ? 'badge-in-progress'
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
                        <td>
                          <button
                            onClick={() => handleDeleteTask(task._id)}
                            className="btn btn-danger btn-sm"
                            title="Admin Delete"
                          >
                            🗑️ Delete
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}

          {/* Tab 2: Registered Users */}
          {activeTab === 'users' && (
            <div className="table-card">
              <div className="table-header">
                <h3>Registered User Accounts</h3>
                <button onClick={fetchUsers} className="btn btn-secondary btn-sm">
                  🔄 Refresh
                </button>
              </div>

              {loading ? (
                <div style={{ padding: '40px', textAlign: 'center', color: '#64748b' }}>
                  Loading registered users...
                </div>
              ) : users.length === 0 ? (
                <div className="empty-state">
                  <h3>No registered users found</h3>
                </div>
              ) : (
                <table className="custom-table">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Role</th>
                      <th>Account Created</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.map((u) => (
                      <tr key={u._id}>
                        <td style={{ fontWeight: 600 }}>{u.name}</td>
                        <td>{u.email}</td>
                        <td>
                          <span
                            className={`badge ${
                              u.role === 'Admin' ? 'badge-priority-high' : 'badge-in-progress'
                            }`}
                          >
                            {u.role}
                          </span>
                        </td>
                        <td>{formatDate(u.createdAt)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default Admin;
