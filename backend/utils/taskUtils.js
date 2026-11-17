const Task = require('../models/Task');

/**
 * Automatically updates tasks whose deadline has passed to 'Overdue' status.
 * Scoped to a specific user (if userId is provided) or platform-wide (if null).
 * Emits real-time Socket.IO notifications if the io instance is supplied.
 */
const autoUpdateOverdueTasks = async (userId = null, io = null) => {
  try {
    const now = new Date();
    const query = {
      dueDate: { $ne: null, $lt: now },
      status: { $nin: ['Completed', 'Overdue'] }
    };

    if (userId) {
      query.user = userId;
    }

    const overdueTasks = await Task.find(query);

    if (overdueTasks.length > 0) {
      await Task.updateMany(query, { $set: { status: 'Overdue' } });
      console.log(`[TaskFlow Auto-Update] Automatically marked ${overdueTasks.length} task(s) as Overdue.`);

      if (io) {
        overdueTasks.forEach((task) => {
          io.to(task.user.toString()).emit('taskStatusUpdated', {
            taskId: task._id,
            title: task.title,
            oldStatus: task.status,
            newStatus: 'Overdue',
            message: `Deadline passed: Task "${task.title}" is now marked as Overdue.`
          });
        });
      }
    }

    return overdueTasks.length;
  } catch (error) {
    console.error('[TaskFlow Auto-Update] Error updating overdue tasks:', error.message);
    return 0;
  }
};

/**
 * Returns the MongoDB $switch aggregation expression that ranks tasks so:
 * 1. High priority Pending (and Overdue) tasks show first
 * 2. High priority In Progress tasks
 * 3. Medium priority Pending (and Overdue) tasks
 * 4. Medium priority In Progress tasks
 * 5. Low priority Pending (and Overdue) tasks
 * 6. Low priority In Progress tasks
 * 7. Completed tasks last
 */
const getPriorityRankExpression = () => ({
  $switch: {
    branches: [
      {
        case: {
          $and: [
            { $in: ['$status', ['Pending', 'Overdue']] },
            { $eq: ['$priority', 'High'] }
          ]
        },
        then: 1
      },
      {
        case: {
          $and: [
            { $eq: ['$status', 'In Progress'] },
            { $eq: ['$priority', 'High'] }
          ]
        },
        then: 2
      },
      {
        case: {
          $and: [
            { $in: ['$status', ['Pending', 'Overdue']] },
            { $eq: ['$priority', 'Medium'] }
          ]
        },
        then: 3
      },
      {
        case: {
          $and: [
            { $eq: ['$status', 'In Progress'] },
            { $eq: ['$priority', 'Medium'] }
          ]
        },
        then: 4
      },
      {
        case: {
          $and: [
            { $in: ['$status', ['Pending', 'Overdue']] },
            { $eq: ['$priority', 'Low'] }
          ]
        },
        then: 5
      },
      {
        case: {
          $and: [
            { $eq: ['$status', 'In Progress'] },
            { $eq: ['$priority', 'Low'] }
          ]
        },
        then: 6
      },
      {
        case: { $eq: ['$status', 'Completed'] },
        then: 7
      }
    ],
    default: 8
  }
});

module.exports = {
  autoUpdateOverdueTasks,
  getPriorityRankExpression
};
