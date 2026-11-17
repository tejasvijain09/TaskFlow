const express = require('express');
const router = express.Router();
const { parseTaskWithAI } = require('../controllers/aiController');
const { protect } = require('../middleware/authMiddleware');

// Route requires user authentication
router.use(protect);

/**
 * @swagger
 * tags:
 *   name: AI Assistant
 *   description: AI and Natural Language processing endpoints
 */

/**
 * @swagger
 * /api/ai/parse-task:
 *   post:
 *     summary: Parse natural language prompt into structured task
 *     tags: [AI Assistant]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required: [input]
 *             properties:
 *               input:
 *                 type: string
 *                 example: Submit CSF402 final project report by tomorrow 5pm with high priority
 *     responses:
 *       200:
 *         description: Structured task fields successfully extracted
 *       400:
 *         description: Missing input prompt
 */
router.post('/parse-task', parseTaskWithAI);

module.exports = router;
