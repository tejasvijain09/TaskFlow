const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');
const dotenv = require('dotenv');
const swaggerUi = require('swagger-ui-express');

// Load environment variables from .env file
dotenv.config();

const connectDB = require('./config/db');
const swaggerSpec = require('./config/swagger');

// Import routes
const authRoutes = require('./routes/authRoutes');
const taskRoutes = require('./routes/taskRoutes');
const dashboardRoutes = require('./routes/dashboardRoutes');
const adminRoutes = require('./routes/adminRoutes');

// Connect to MongoDB database
connectDB();

const app = express();

// Standard middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Create HTTP server for Express and Socket.IO
const server = http.createServer(app);

// Initialize Socket.IO with CORS allowed for frontend dev server
const io = new Server(server, {
  cors: {
    origin: '*', // Allow connections from frontend
    methods: ['GET', 'POST', 'PUT', 'DELETE']
  }
});

// Socket.IO event handling
// When user connects, they join a private room named by their userId
io.on('connection', (socket) => {
  console.log(`Socket connected: ${socket.id}`);

  // User joins room corresponding to their user ID
  socket.on('join', (userId) => {
    if (userId) {
      socket.join(userId.toString());
      console.log(`User ${userId} joined personal socket room`);
    }
  });

  socket.on('disconnect', () => {
    console.log(`Socket disconnected: ${socket.id}`);
  });
});

// Attach io instance to express app so controllers can emit events
app.set('io', io);

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/tasks', taskRoutes);
app.use('/api/dashboard', dashboardRoutes);
app.use('/api/admin', adminRoutes);

// Swagger API Documentation route
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

// Root health route
app.get('/', (req, res) => {
  res.json({
    message: 'Welcome to TaskFlow API',
    documentation: '/api-docs',
    status: 'Running'
  });
});

// 404 Route Handler
app.use((req, res, next) => {
  res.status(404).json({ message: `Route ${req.originalUrl} not found` });
});

// Global Error Handler
app.use((err, req, res, next) => {
  console.error('Unhandled server error:', err.stack);
  res.status(500).json({
    message: err.message || 'Internal Server Error'
  });
});

const PORT = process.env.PORT || 5001;

// Periodically check and auto-update overdue tasks
const { autoUpdateOverdueTasks } = require('./utils/taskUtils');

server.listen(PORT, '0.0.0.0', () => {
  console.log(`TaskFlow Server running on port ${PORT}`);
  console.log(`Swagger Docs available at http://localhost:${PORT}/api-docs`);

  // Initial overdue check after startup
  setTimeout(() => {
    autoUpdateOverdueTasks(null, io).catch((err) =>
      console.error('Initial overdue check error:', err.message)
    );
  }, 3000);

  // Periodic overdue check every 60 seconds
  setInterval(() => {
    autoUpdateOverdueTasks(null, io).catch((err) =>
      console.error('Periodic overdue check error:', err.message)
    );
  }, 60 * 1000);
});
