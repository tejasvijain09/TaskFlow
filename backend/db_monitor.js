const mongoose = require('mongoose');
const dotenv = require('dotenv');

dotenv.config();

const Task = require('./models/Task');
const User = require('./models/User');

// ANSI Colors for clean terminal display
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const CYAN = '\x1b[36m';
const RED = '\x1b[31m';
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';

async function startMonitor() {
  try {
    await mongoose.connect(process.env.MONGO_URI);
    console.clear();
    console.log(`${BOLD}${CYAN}====================================================${RESET}`);
    console.log(`${BOLD}${CYAN}       TASKFLOW — LIVE MONGODB REAL-TIME MONITOR    ${RESET}`);
    console.log(`${BOLD}${CYAN}====================================================${RESET}`);
    console.log(`${GREEN}Connected to Database:${RESET} ${mongoose.connection.name}`);
    console.log(`${GREEN}Host:${RESET} ${mongoose.connection.host}`);
    console.log(`${YELLOW}Listening for live changes from React frontend...${RESET}\n`);

    let lastTaskCount = -1;
    let lastUpdatedTime = null;

    const displayCurrentState = async () => {
      const users = await User.find({}, { name: 1, email: 1, role: 1 });
      const tasks = await Task.find({}).sort({ updatedAt: -1 }).populate('user', 'name');

      console.log(`${BOLD}--- Current Database Summary ---${RESET}`);
      console.log(`Registered Users (${users.length}):`, users.map(u => `${u.name} (${u.role})`).join(', '));
      console.log(`Total Tasks in MongoDB: ${BOLD}${tasks.length}${RESET}\n`);

      console.log(`${BOLD}Most Recent Tasks:${RESET}`);
      tasks.slice(0, 5).forEach((t, i) => {
        const statusColor = t.status === 'Completed' ? GREEN : (t.status === 'In Progress' ? CYAN : YELLOW);
        console.log(`  [${i + 1}] ${BOLD}${t.title}${RESET}`);
        console.log(`      Status: ${statusColor}${t.status}${RESET} | Priority: ${t.priority} | User: ${t.user?.name || 'Unknown'}`);
        console.log(`      Last Modified: ${t.updatedAt.toLocaleTimeString()}\n`);
      });
      console.log(`${YELLOW}>>> Perform any action in the browser (Create, Edit, Status change, Delete) to see live updates below... <<<\n${RESET}`);
    };

    await displayCurrentState();

    // Check for changes every 1.5 seconds
    setInterval(async () => {
      try {
        const count = await Task.countDocuments();
        const latestTask = await Task.findOne().sort({ updatedAt: -1 });

        if (lastTaskCount !== -1 && count !== lastTaskCount) {
          console.log(`${BOLD}${GREEN}[REAL-TIME DATABASE EVENT]${RESET} Task count changed: ${lastTaskCount} -> ${BOLD}${count}${RESET}`);
          if (latestTask) {
            console.log(`  Task: "${latestTask.title}" | Status: ${latestTask.status} | Priority: ${latestTask.priority}`);
            console.log(`  MongoDB _id: ${latestTask._id}\n`);
          }
          lastTaskCount = count;
        } else if (latestTask && lastUpdatedTime && latestTask.updatedAt > lastUpdatedTime) {
          console.log(`${BOLD}${CYAN}[REAL-TIME DATABASE EVENT]${RESET} Task Modified in Database:`);
          console.log(`  Title: ${BOLD}${latestTask.title}${RESET}`);
          console.log(`  New Status: ${latestTask.status} | Priority: ${latestTask.priority}`);
          console.log(`  Updated At: ${latestTask.updatedAt.toLocaleTimeString()}`);
          console.log(`  Raw MongoDB Document:`, {
            _id: latestTask._id.toString(),
            title: latestTask.title,
            status: latestTask.status,
            priority: latestTask.priority,
            updatedAt: latestTask.updatedAt
          });
          console.log('');
          lastUpdatedTime = latestTask.updatedAt;
        }

        lastTaskCount = count;
        if (latestTask) {
          lastUpdatedTime = latestTask.updatedAt;
        }
      } catch (err) {
        // ignore interval errors
      }
    }, 1500);

  } catch (err) {
    console.error('Monitor connection error:', err.message);
  }
}

startMonitor();
