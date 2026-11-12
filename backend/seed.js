const mongoose = require('mongoose');
const dotenv = require('dotenv');
const bcrypt = require('bcryptjs');

dotenv.config();

const User = require('./models/User');
const Task = require('./models/Task');

// Database seeder script to initialize default Admin, test User, and sample tasks
const seedData = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI);
    console.log('Connected to MongoDB for seeding...');

    // Clear existing data to avoid duplicates
    await User.deleteMany();
    await Task.deleteMany();
    console.log('Previous users and tasks cleared.');

    // Password hashing
    const adminSalt = await bcrypt.genSalt(10);
    const adminHashedPassword = await bcrypt.hash('admin123', adminSalt);

    const userSalt = await bcrypt.genSalt(10);
    const userHashedPassword = await bcrypt.hash('user123', userSalt);

    // Create Admin user
    const admin = await User.create({
      name: 'Admin User',
      email: 'admin@taskflow.com',
      password: adminHashedPassword,
      role: 'Admin'
    });

    // Create regular User
    const user = await User.create({
      name: 'Suraj Yadav',
      email: 'suraj@taskflow.com',
      password: userHashedPassword,
      role: 'User'
    });

    console.log('Admin and standard user created successfully.');

    // Create sample tasks for standard user
    const today = new Date();
    const tasks = [
      {
        title: 'Design Database Schemas',
        description: 'Define User and Task Mongoose schemas with validation and indexes.',
        status: 'Completed',
        priority: 'High',
        dueDate: new Date(today.getTime() + 2 * 24 * 60 * 60 * 1000),
        user: user._id
      },
      {
        title: 'Implement JWT Authentication',
        description: 'Create login, register, and token verification middleware with bcrypt.',
        status: 'Completed',
        priority: 'High',
        dueDate: new Date(today.getTime() + 3 * 24 * 60 * 60 * 1000),
        user: user._id
      },
      {
        title: 'Develop Task CRUD Endpoints',
        description: 'Implement create, read, update, delete routes with status and priority.',
        status: 'In Progress',
        priority: 'Medium',
        dueDate: new Date(today.getTime() + 5 * 24 * 60 * 60 * 1000),
        user: user._id
      },
      {
        title: 'Add Dashboard Aggregation Pipeline',
        description: 'Group tasks by status using MongoDB aggregation pipeline for stats.',
        status: 'In Progress',
        priority: 'Medium',
        dueDate: new Date(today.getTime() + 7 * 24 * 60 * 60 * 1000),
        user: user._id
      },
      {
        title: 'Integrate Real-Time Socket.IO Notifications',
        description: 'Emit events when task status is updated and listen in React frontend.',
        status: 'Pending',
        priority: 'Medium',
        dueDate: new Date(today.getTime() + 9 * 24 * 60 * 60 * 1000),
        user: user._id
      },
      {
        title: 'Prepare Viva Presentation & Documentation',
        description: 'Draft VIVA_PREPARATION.md, README.md, and test all college demo scenarios.',
        status: 'Pending',
        priority: 'Low',
        dueDate: new Date(today.getTime() + 12 * 24 * 60 * 60 * 1000),
        user: user._id
      }
    ];

    await Task.insertMany(tasks);
    console.log(`${tasks.length} sample tasks seeded successfully.`);

    console.log('\n--- Credentials for Demo ---');
    console.log('Administrator: admin@taskflow.com / admin123');
    console.log('Normal User:   suraj@taskflow.com / user123');
    console.log('----------------------------\n');

    process.exit(0);
  } catch (error) {
    console.error('Seeding error:', error.message);
    process.exit(1);
  }
};

seedData();
