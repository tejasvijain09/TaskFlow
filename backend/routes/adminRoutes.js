const express = require('express');
const router = express.Router();
const {
  getAllUsers,
  getAllTasks,
  deleteAdminTask
} = require('../controllers/adminController');
const { protect } = require('../middleware/authMiddleware');
const { requireAdmin } = require('../middleware/adminMiddleware');

// All admin routes require both authentication and Admin role
router.use(protect);
router.use(requireAdmin);

/**
 * @swagger
 * tags:
 *   name: Admin
 *   description: Administrator control endpoints
 */

/**
 * @swagger
 * /api/admin/users:
 *   get:
 *     summary: Get list of all registered users (Admin only)
 *     tags: [Admin]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: List of registered users
 *       403:
 *         description: Forbidden
 */
router.get('/users', getAllUsers);

/**
 * @swagger
 * /api/admin/tasks:
 *   get:
 *     summary: Get all tasks across all users (Admin only)
 *     tags: [Admin]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: List of all tasks with user info
 *       403:
 *         description: Forbidden
 */
router.get('/tasks', getAllTasks);

/**
 * @swagger
 * /api/admin/tasks/{id}:
 *   delete:
 *     summary: Delete any inappropriate task (Admin only)
 *     tags: [Admin]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Task deleted by admin
 *       403:
 *         description: Forbidden
 */
router.delete('/tasks/:id', deleteAdminTask);

module.exports = router;
