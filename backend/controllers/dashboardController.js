const Task = require('../models/Task');
const mongoose = require('mongoose');
const { autoUpdateOverdueTasks, getPriorityRankExpression } = require('../utils/taskUtils');

// @desc    Get dashboard statistics using MongoDB aggregation
// @route   GET /api/dashboard/stats
// @access  Private
const getDashboardStats = async (req, res) => {
  try {
    // Stage 1: Auto-update any overdue tasks before calculating statistics
    const targetUserId = req.user.role === 'Admin' ? null : req.user._id;
    await autoUpdateOverdueTasks(targetUserId, req.app.get('io'));

    // Stage 2: Define match condition
    // Normal users see their own task stats; Admin sees all tasks stats
    const matchStage = req.user.role === 'Admin'
      ? {}
      : { user: new mongoose.Types.ObjectId(req.user._id) };

    // Stage 3: MongoDB Aggregation Pipeline
    // Groups by task 'status' and counts the occurrences
    const statsAggregation = await Task.aggregate([
      {
        $match: matchStage
      },
      {
        $group: {
          _id: '$status',     // Group key: 'Pending', 'In Progress', 'Completed', 'Overdue'
          count: { $sum: 1 }  // Increment count by 1 for each matching document
        }
      }
    ]);

    // Format aggregation results into easy-to-use numbers
    let pendingCount = 0;
    let inProgressCount = 0;
    let completedCount = 0;
    let overdueCount = 0;

    statsAggregation.forEach((item) => {
      if (item._id === 'Pending') pendingCount = item.count;
      if (item._id === 'In Progress') inProgressCount = item.count;
      if (item._id === 'Completed') completedCount = item.count;
      if (item._id === 'Overdue') overdueCount = item.count;
    });

    const totalTasks = pendingCount + inProgressCount + completedCount + overdueCount;

    // Fetch priority-ranked active tasks for dashboard preview (High-priority Pending/Overdue tasks first)
    const priorityTasks = await Task.aggregate([
      { $match: matchStage },
      {
        $addFields: {
          rankWeight: getPriorityRankExpression()
        }
      },
      { $sort: { rankWeight: 1, dueDate: 1, createdAt: -1 } },
      { $limit: 6 },
      {
        $lookup: {
          from: 'users',
          localField: 'user',
          foreignField: '_id',
          as: 'user'
        }
      },
      {
        $unwind: {
          path: '$user',
          preserveNullAndEmptyArrays: true
        }
      },
      {
        $project: {
          'user.password': 0
        }
      }
    ]);

    res.json({
      totalTasks,
      pendingTasks: pendingCount,
      inProgressTasks: inProgressCount,
      completedTasks: completedCount,
      overdueTasks: overdueCount,
      recentTasks: priorityTasks
    });
  } catch (error) {
    console.error('Dashboard stats error:', error.message);
    res.status(500).json({ message: 'Server error calculating dashboard statistics' });
  }
};

module.exports = {
  getDashboardStats
};
