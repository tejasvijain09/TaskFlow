import React from 'react';

const TaskCard = ({ task, onEdit, onDelete, onStatusChange }) => {
  // Helper to format due date nicely
  const formatDate = (dateString) => {
    if (!dateString) return 'No due date';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  // Status CSS badge class mapper
  const getStatusBadge = (status) => {
    switch (status) {
      case 'Pending':
        return 'badge-pending';
      case 'In Progress':
        return 'badge-in-progress';
      case 'Completed':
        return 'badge-completed';
      case 'Overdue':
        return 'badge-overdue';
      default:
        return 'badge-pending';
    }
  };

  // Priority CSS badge class mapper
  const getPriorityBadge = (priority) => {
    switch (priority) {
      case 'Low':
        return 'badge-priority-low';
      case 'Medium':
        return 'badge-priority-medium';
      case 'High':
        return 'badge-priority-high';
      default:
        return 'badge-priority-medium';
    }
  };

  return (
    <div className="task-card">
      <div>
        <div className="task-card-header">
          <h3 className="task-title">{task.title}</h3>
          <span className={`badge ${getStatusBadge(task.status)}`}>
            {task.status}
          </span>
        </div>

        <p className="task-description">
          {task.description || <em>No description provided</em>}
        </p>
      </div>

      <div>
        <div className="task-meta">
          <div>
            <strong>Priority: </strong>
            <span className={`badge ${getPriorityBadge(task.priority)}`}>
              {task.priority}
            </span>
          </div>
          <div>
            <strong>Due: </strong>
            <span style={{ color: task.status === 'Overdue' ? '#b91c1c' : 'inherit', fontWeight: task.status === 'Overdue' ? 600 : 'normal' }}>
              {formatDate(task.dueDate)} {task.status === 'Overdue' && '⚠️'}
            </span>
          </div>
        </div>

        <div className="task-actions">
          {/* Quick status dropdown */}
          <select
            className="task-status-select"
            value={task.status}
            onChange={(e) => onStatusChange(task._id, e.target.value)}
          >
            <option value="Pending">Pending</option>
            <option value="In Progress">In Progress</option>
            <option value="Completed">Completed</option>
            <option value="Overdue">Overdue</option>
          </select>

          <div className="task-buttons">
            <button
              onClick={() => onEdit(task)}
              className="btn btn-secondary btn-sm"
              title="Edit Task"
            >
              ✏️ Edit
            </button>
            <button
              onClick={() => onDelete(task._id)}
              className="btn btn-danger btn-sm"
              title="Delete Task"
            >
              🗑️ Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskCard;
