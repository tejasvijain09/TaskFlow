const User = require('../models/User');
const Task = require('../models/Task');
const mongoose = require('mongoose');

// @desc    Get all registered users (Admin only)
// @route   GET /api/admin/users
// @access  Private/Admin
const getAllUsers = async (req, res) => {
  try {
    // Return all users without password hash
    const users = await User.find().select('-password').sort({ createdAt: -1 });
    res.json(users);
  } catch (error) {
    console.error('Admin get users error:', error.message);
    res.status(500).json({ message: 'Server error fetching users' });
  }
};

// @desc    Get all tasks across all users (Admin only)
// @route   GET /api/admin/tasks
// @access  Private/Admin
const getAllTasks = async (req, res) => {
  try {
    // Populate user info (name, email)
    const tasks = await Task.find()
      .populate('user', 'name email')
      .sort({ createdAt: -1 });

    res.json(tasks);
  } catch (error) {
    console.error('Admin get tasks error:', error.message);
    res.status(500).json({ message: 'Server error fetching all tasks' });
  }
};

// @desc    Delete any task as admin
// @route   DELETE /api/admin/tasks/:id
// @access  Private/Admin
const deleteAdminTask = async (req, res) => {
  try {
    // Validate MongoDB ObjectId format
    if (!mongoose.Types.ObjectId.isValid(req.params.id)) {
      return res.status(400).json({ message: 'Invalid task ID format' });
    }

    const task = await Task.findById(req.params.id);

    if (!task) {
      return res.status(404).json({ message: 'Task not found' });
    }

    await task.deleteOne();
    res.json({ message: 'Task removed by administrator', id: req.params.id });
  } catch (error) {
    console.error('Admin delete task error:', error.message);
    res.status(500).json({ message: 'Server error deleting task' });
  }
};

module.exports = {
  getAllUsers,
  getAllTasks,
  deleteAdminTask
};
