const Task = require('../models/Task');
const mongoose = require('mongoose');
const { autoUpdateOverdueTasks, getPriorityRankExpression } = require('../utils/taskUtils');

// @desc    Create a new task
// @route   POST /api/tasks
// @access  Private
const createTask = async (req, res) => {
  try {
    const { title, description, status, priority, dueDate } = req.body;

    // Validate required fields
    if (!title || typeof title !== 'string' || title.trim() === '') {
      return res.status(400).json({ message: 'Task title is required' });
    }

    // Determine initial status: if deadline is already in the past and not completed, mark Overdue
    let initialStatus = status || 'Pending';
    if (dueDate && new Date(dueDate) < new Date() && initialStatus !== 'Completed') {
      initialStatus = 'Overdue';
    }

    // Create the task associated with logged-in user
    const task = await Task.create({
      title: title.trim(),
      description: description ? description.trim() : '',
      status: initialStatus,
      priority: priority || 'Medium',
      dueDate: dueDate || null,
      user: req.user._id
    });

    res.status(201).json(task);
  } catch (error) {
    console.error('Create task error:', error.message);
    res.status(500).json({ message: 'Server error creating task' });
  }
};

// @desc    Get logged-in user tasks with filtering, sorting, and pagination
// @route   GET /api/tasks
// @access  Private
const getTasks = async (req, res) => {
  try {
    // 1. Auto-update any tasks whose deadline has passed to 'Overdue'
    await autoUpdateOverdueTasks(req.user._id, req.app.get('io'));

    const { status, priority, sortBy = 'priority', order = 'desc', page = 1, limit = 6 } = req.query;

    // Base query: filter by current user's ID
    const query = { user: req.user._id };

    // Apply status filter if provided
    if (status && status !== 'All') {
      query.status = status;
    }

    // Apply priority filter if provided
    if (priority && priority !== 'All') {
      query.priority = priority;
    }

    // Setup safe pagination numbers
    const pageNum = Math.max(1, parseInt(page, 10) || 1);
    const limitNum = Math.max(1, parseInt(limit, 10) || 6);
    const skip = (pageNum - 1) * limitNum;

    // Count total tasks matching query for pagination calculation
    const totalTasks = await Task.countDocuments(query);
    const totalPages = Math.ceil(totalTasks / limitNum) || 1;

    let tasks;

    // When sorting by priority (or default):
    // Show High priority Pending/Overdue first, then Medium, Low, with Completed last
    if (sortBy === 'priority') {
      tasks = await Task.aggregate([
        { $match: query },
        {
          $addFields: {
            rankWeight: getPriorityRankExpression()
          }
        },
        { $sort: { rankWeight: 1, dueDate: 1, createdAt: -1 } },
        { $skip: skip },
        { $limit: limitNum }
      ]);
    } else {
      const allowedSortFields = ['createdAt', 'dueDate', 'title', 'status'];
      const sortField = allowedSortFields.includes(sortBy) ? sortBy : 'createdAt';
      const sortOrder = order === 'asc' ? 1 : -1;
      const sortCriteria = { [sortField]: sortOrder };

      tasks = await Task.find(query)
        .sort(sortCriteria)
        .skip(skip)
        .limit(limitNum);
    }

    res.json({
      tasks,
      currentPage: pageNum,
      totalPages,
      totalTasks
    });
  } catch (error) {
    console.error('Get tasks error:', error.message);
    res.status(500).json({ message: 'Server error fetching tasks' });
  }
};

// @desc    Get single task by ID
// @route   GET /api/tasks/:id
// @access  Private
const getTaskById = async (req, res) => {
  try {
    // Validate MongoDB ObjectId format
    if (!mongoose.Types.ObjectId.isValid(req.params.id)) {
      return res.status(400).json({ message: 'Invalid task ID format' });
    }

    const task = await Task.findById(req.params.id);

    if (!task) {
      return res.status(404).json({ message: 'Task not found' });
    }

    // Check ownership: regular user can only view their own task; Admin can view any
    if (task.user.toString() !== req.user._id.toString() && req.user.role !== 'Admin') {
      return res.status(403).json({ message: 'Not authorized to view this task' });
    }

    // Auto-update to Overdue if deadline passed and not completed
    if (task.dueDate && new Date(task.dueDate) < new Date() && !['Completed', 'Overdue'].includes(task.status)) {
      task.status = 'Overdue';
      await task.save();
    }

    res.json(task);
  } catch (error) {
    console.error('Get task by ID error:', error.message);
    res.status(500).json({ message: 'Server error fetching task' });
  }
};

// @desc    Update an existing task
// @route   PUT /api/tasks/:id
// @access  Private
const updateTask = async (req, res) => {
  try {
    // Validate MongoDB ObjectId format
    if (!mongoose.Types.ObjectId.isValid(req.params.id)) {
      return res.status(400).json({ message: 'Invalid task ID format' });
    }

    const task = await Task.findById(req.params.id);

    if (!task) {
      return res.status(404).json({ message: 'Task not found' });
    }

    // Check ownership
    if (task.user.toString() !== req.user._id.toString() && req.user.role !== 'Admin') {
      return res.status(403).json({ message: 'Not authorized to update this task' });
    }

    const oldStatus = task.status;
    const { title, description, status, priority, dueDate } = req.body;

    // Update fields if provided in request
    if (title !== undefined) task.title = title.trim();
    if (description !== undefined) task.description = description.trim();
    if (priority !== undefined) task.priority = priority;
    if (dueDate !== undefined) task.dueDate = dueDate ? new Date(dueDate) : null;

    if (status !== undefined) {
      task.status = status;
    }

    // Automatic overdue detection:
    // If task is not marked Completed:
    // 1. If dueDate is in the past, status automatically becomes Overdue
    // 2. If dueDate is extended into the future and previous status was Overdue, revert to Pending (or provided status)
    if (task.status !== 'Completed') {
      if (task.dueDate && new Date(task.dueDate) < new Date()) {
        task.status = 'Overdue';
      } else if (task.status === 'Overdue' && task.dueDate && new Date(task.dueDate) >= new Date()) {
        task.status = status && status !== 'Overdue' ? status : 'Pending';
      }
    }

    const updatedTask = await task.save();

    // If status was changed, emit real-time Socket.IO notification to user
    if (updatedTask.status !== oldStatus) {
      const io = req.app.get('io');
      if (io) {
        // Emit to user's personal room (named after their userId)
        io.to(task.user.toString()).emit('taskStatusUpdated', {
          taskId: task._id,
          title: task.title,
          oldStatus,
          newStatus: updatedTask.status,
          message: `Task "${task.title}" status changed to ${updatedTask.status}`
        });
      }
    }

    res.json(updatedTask);
  } catch (error) {
    console.error('Update task error:', error.message);
    res.status(500).json({ message: 'Server error updating task' });
  }
};

// @desc    Delete a task
// @route   DELETE /api/tasks/:id
// @access  Private
const deleteTask = async (req, res) => {
  try {
    // Validate MongoDB ObjectId format
    if (!mongoose.Types.ObjectId.isValid(req.params.id)) {
      return res.status(400).json({ message: 'Invalid task ID format' });
    }

    const task = await Task.findById(req.params.id);

    if (!task) {
      return res.status(404).json({ message: 'Task not found' });
    }

    // Check ownership: task owner or Admin can delete
    if (task.user.toString() !== req.user._id.toString() && req.user.role !== 'Admin') {
      return res.status(403).json({ message: 'Not authorized to delete this task' });
    }

    await task.deleteOne();

    res.json({ message: 'Task deleted successfully', id: req.params.id });
  } catch (error) {
    console.error('Delete task error:', error.message);
    res.status(500).json({ message: 'Server error deleting task' });
  }
};

module.exports = {
  createTask,
  getTasks,
  getTaskById,
  updateTask,
  deleteTask
};
