const Task = require('../models/Task');
const mongoose = require('mongoose');

// @desc    Get dashboard statistics using MongoDB aggregation
// @route   GET /api/dashboard/stats
// @access  Private
const getDashboardStats = async (req, res) => {
  try {
    // Stage 1: Define match condition
    // Normal users see their own task stats; Admin sees all tasks stats
    const matchStage = req.user.role === 'Admin'
      ? {}
      : { user: new mongoose.Types.ObjectId(req.user._id) };

    // Stage 2: MongoDB Aggregation Pipeline
    // Stage 2.1: $match - filters tasks belonging to user (or all if admin)
    // Stage 2.2: $group - groups by task 'status' and counts the occurrences
    const statsAggregation = await Task.aggregate([
      // STAGE 1: Match tasks
      {
        $match: matchStage
      },
      // STAGE 2: Group by status and count
      {
        $group: {
          _id: '$status',     // Group key: 'Pending', 'In Progress', 'Completed'
          count: { $sum: 1 }  // Increment count by 1 for each matching document
        }
      }
    ]);

    // Format aggregation results into easy-to-use numbers
    let pendingCount = 0;
    let inProgressCount = 0;
    let completedCount = 0;

    statsAggregation.forEach((item) => {
      if (item._id === 'Pending') pendingCount = item.count;
      if (item._id === 'In Progress') inProgressCount = item.count;
      if (item._id === 'Completed') completedCount = item.count;
    });

    const totalTasks = pendingCount + inProgressCount + completedCount;

    // Fetch the 5 most recent tasks for quick dashboard preview
    const recentTasks = await Task.find(matchStage)
      .sort({ createdAt: -1 })
      .limit(5)
      .populate('user', 'name email');

    res.json({
      totalTasks,
      pendingTasks: pendingCount,
      inProgressTasks: inProgressCount,
      completedTasks: completedCount,
      recentTasks
    });
  } catch (error) {
    console.error('Dashboard stats error:', error.message);
    res.status(500).json({ message: 'Server error calculating dashboard statistics' });
  }
};

module.exports = {
  getDashboardStats
};
