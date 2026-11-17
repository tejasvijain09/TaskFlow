import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import Navbar from '../components/Navbar';
import TaskCard from '../components/TaskCard';
import API from '../services/api';

const Tasks = () => {
  // Task list and pagination states
  const [tasks, setTasks] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalTasks, setTotalTasks] = useState(0);
  const [loading, setLoading] = useState(false);
  const [feedbackMessage, setFeedbackMessage] = useState('');

  // Filter and sort states
  const [statusFilter, setStatusFilter] = useState('All');
  const [priorityFilter, setPriorityFilter] = useState('All');
  const [sortBy, setSortBy] = useState('priority');
  const [sortOrder, setSortOrder] = useState('desc');

  // Modal states for Create / Edit
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState(null); // null when adding, task object when editing
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    status: 'Pending',
    priority: 'Medium',
    dueDate: ''
  });
  const [formError, setFormError] = useState('');

  // Fetch tasks with current query parameters
  const fetchTasks = async (pageToFetch = currentPage) => {
    try {
      setLoading(true);
      const params = {
        page: pageToFetch,
        limit: 6,
        sortBy,
        order: sortOrder
      };

      if (statusFilter !== 'All') params.status = statusFilter;
      if (priorityFilter !== 'All') params.priority = priorityFilter;

      const res = await API.get('/tasks', { params });
      setTasks(res.data.tasks);
      setCurrentPage(res.data.currentPage);
      setTotalPages(res.data.totalPages);
      setTotalTasks(res.data.totalTasks);
    } catch (err) {
      console.error('Fetch tasks error:', err);
      setFeedbackMessage('Failed to load tasks.');
    } finally {
      setLoading(false);
    }
  };

  // Re-fetch whenever filters or sorting change
  useEffect(() => {
    fetchTasks(1);
  }, [statusFilter, priorityFilter, sortBy, sortOrder]);

  // Open modal in "Add Task" mode
  const handleOpenAddModal = () => {
    setEditingTask(null);
    setFormData({
      title: '',
      description: '',
      status: 'Pending',
      priority: 'Medium',
      dueDate: ''
    });
    setFormError('');
    setIsModalOpen(true);
  };

  // Open modal in "Edit Task" mode
  const handleOpenEditModal = (task) => {
    setEditingTask(task);
    setFormData({
      title: task.title,
      description: task.description || '',
      status: task.status,
      priority: task.priority,
      dueDate: task.dueDate ? task.dueDate.split('T')[0] : ''
    });
    setFormError('');
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingTask(null);
    setFormError('');
  };

  // Handle Create or Update task submit
  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setFormError('');

    if (!formData.title.trim()) {
      setFormError('Task title is required');
      return;
    }

    try {
      if (editingTask) {
        // Update existing task
        await API.put(`/tasks/${editingTask._id}`, formData);
        setFeedbackMessage('Task updated successfully!');
      } else {
        // Create new task
        await API.post('/tasks', formData);
        setFeedbackMessage('New task created successfully!');
      }

      handleCloseModal();
      fetchTasks(currentPage);

      // Auto clear feedback message after 3 seconds
      setTimeout(() => setFeedbackMessage(''), 3000);
    } catch (err) {
      console.error('Save task error:', err);
      setFormError(
        err.response && err.response.data && err.response.data.message
          ? err.response.data.message
          : 'Failed to save task'
      );
    }
  };

  // Quick status update from task card dropdown
  const handleStatusChange = async (taskId, newStatus) => {
    try {
      await API.put(`/tasks/${taskId}`, { status: newStatus });
      fetchTasks(currentPage);
      setFeedbackMessage(`Status changed to ${newStatus}`);
      setTimeout(() => setFeedbackMessage(''), 3000);
    } catch (err) {
      console.error('Status change error:', err);
      setFeedbackMessage('Could not update status');
    }
  };

  // Delete task
  const handleDeleteTask = async (taskId) => {
    const confirmDelete = window.confirm('Are you sure you want to delete this task?');
    if (!confirmDelete) return;

    try {
      await API.delete(`/tasks/${taskId}`);
      setFeedbackMessage('Task deleted successfully!');
      setTimeout(() => setFeedbackMessage(''), 3000);

      // If last item on page was deleted, move back a page if possible
      if (tasks.length === 1 && currentPage > 1) {
        fetchTasks(currentPage - 1);
      } else {
        fetchTasks(currentPage);
      }
    } catch (err) {
      console.error('Delete task error:', err);
      setFeedbackMessage('Failed to delete task');
    }
  };

  return (
    <div className="app-layout">
      <Sidebar />

      <div className="main-wrapper">
        <Navbar title="My Tasks" />

        <main className="content-container">
          {/* Header & Add Task Button */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <div>
              <h2 style={{ fontSize: '22px', fontWeight: 700, color: '#0f172a' }}>Task Management</h2>
              <p style={{ color: '#64748b', fontSize: '14px' }}>
                Total: <strong>{totalTasks}</strong> {totalTasks === 1 ? 'task' : 'tasks'} found
              </p>
            </div>
            <button onClick={handleOpenAddModal} className="btn btn-primary">
              ➕ Add New Task
            </button>
          </div>

          {/* Feedback Banner */}
          {feedbackMessage && (
            <div
              style={{
                backgroundColor: '#e0f2fe',
                border: '1px solid #bae6fd',
                color: '#0369a1',
                padding: '10px 16px',
                borderRadius: '8px',
                marginBottom: '16px',
                fontSize: '14px',
                fontWeight: 500
              }}
            >
              {feedbackMessage}
            </div>
          )}

          {/* Filters, Sorting, and Search Toolbar */}
          <div className="toolbar-card">
            <div className="filter-group">
              {/* Status Filter */}
              <div className="filter-item">
                <label>Status:</label>
                <select
                  className="filter-select"
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                >
                  <option value="All">All Statuses</option>
                  <option value="Pending">Pending</option>
                  <option value="In Progress">In Progress</option>
                  <option value="Completed">Completed</option>
                  <option value="Overdue">Overdue</option>
                </select>
              </div>

              {/* Priority Filter */}
              <div className="filter-item">
                <label>Priority:</label>
                <select
                  className="filter-select"
                  value={priorityFilter}
                  onChange={(e) => setPriorityFilter(e.target.value)}
                >
                  <option value="All">All Priorities</option>
                  <option value="Low">Low</option>
                  <option value="Medium">Medium</option>
                  <option value="High">High</option>
                </select>
              </div>
            </div>

            <div className="filter-group">
              {/* Sort By Field */}
              <div className="filter-item">
                <label>Sort By:</label>
                <select
                  className="filter-select"
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                >
                  <option value="priority">Priority (High Priority First)</option>
                  <option value="createdAt">Date Created</option>
                  <option value="dueDate">Due Date</option>
                  <option value="title">Title (A-Z)</option>
                </select>
              </div>

              {/* Sort Order */}
              <div className="filter-item">
                <label>Order:</label>
                <select
                  className="filter-select"
                  value={sortOrder}
                  onChange={(e) => setSortOrder(e.target.value)}
                >
                  <option value="desc">Descending</option>
                  <option value="asc">Ascending</option>
                </select>
              </div>
            </div>
          </div>

          {/* Task Cards Grid or Loading/Empty state */}
          {loading ? (
            <div style={{ textAlign: 'center', padding: '60px 0', color: '#64748b' }}>
              Loading tasks...
            </div>
          ) : tasks.length === 0 ? (
            <div className="empty-state">
              <h3>No tasks found</h3>
              <p>There are no tasks matching your current filters. Try resetting the filters or add a new task!</p>
              <button onClick={handleOpenAddModal} className="btn btn-primary btn-sm" style={{ marginTop: '14px' }}>
                + Add Task Now
              </button>
            </div>
          ) : (
            <div className="task-grid">
              {tasks.map((task) => (
                <TaskCard
                  key={task._id}
                  task={task}
                  onEdit={handleOpenEditModal}
                  onDelete={handleDeleteTask}
                  onStatusChange={handleStatusChange}
                />
              ))}
            </div>
          )}

          {/* Pagination Controls */}
          {totalPages > 1 && (
            <div className="pagination">
              <button
                className="page-btn"
                disabled={currentPage === 1}
                onClick={() => fetchTasks(currentPage - 1)}
              >
                ← Previous
              </button>

              {Array.from({ length: totalPages }, (_, i) => i + 1).map((pageNum) => (
                <button
                  key={pageNum}
                  className={`page-btn ${currentPage === pageNum ? 'active' : ''}`}
                  onClick={() => fetchTasks(pageNum)}
                >
                  {pageNum}
                </button>
              ))}

              <button
                className="page-btn"
                disabled={currentPage === totalPages}
                onClick={() => fetchTasks(currentPage + 1)}
              >
                Next →
              </button>
            </div>
          )}
        </main>
      </div>

      {/* Add / Edit Task Modal Dialog */}
      {isModalOpen && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{editingTask ? 'Edit Task' : 'Add New Task'}</h3>
              <button className="modal-close" onClick={handleCloseModal}>
                ✕
              </button>
            </div>

            <form onSubmit={handleFormSubmit}>
              <div className="modal-body">
                {formError && <div className="alert-error">{formError}</div>}

                <div className="form-group">
                  <label htmlFor="modal-title">Task Title *</label>
                  <input
                    id="modal-title"
                    type="text"
                    className="form-control"
                    placeholder="e.g. Implement REST API endpoints"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="modal-desc">Description</label>
                  <textarea
                    id="modal-desc"
                    className="form-control"
                    placeholder="Optional description and notes..."
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                  <div className="form-group">
                    <label htmlFor="modal-status">Status</label>
                    <select
                      id="modal-status"
                      className="form-control"
                      value={formData.status}
                      onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                    >
                      <option value="Pending">Pending</option>
                      <option value="In Progress">In Progress</option>
                      <option value="Completed">Completed</option>
                      <option value="Overdue">Overdue</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="modal-priority">Priority</label>
                    <select
                      id="modal-priority"
                      className="form-control"
                      value={formData.priority}
                      onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                    >
                      <option value="Low">Low</option>
                      <option value="Medium">Medium</option>
                      <option value="High">High</option>
                    </select>
                  </div>
                </div>

                <div className="form-group">
                  <label htmlFor="modal-duedate">Due Date</label>
                  <input
                    id="modal-duedate"
                    type="date"
                    className="form-control"
                    value={formData.dueDate}
                    onChange={(e) => setFormData({ ...formData, dueDate: e.target.value })}
                  />
                </div>
              </div>

              <div className="modal-footer">
                <button type="button" onClick={handleCloseModal} className="btn btn-secondary">
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  {editingTask ? 'Save Changes' : 'Create Task'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Tasks;
