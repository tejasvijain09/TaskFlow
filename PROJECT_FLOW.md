# TaskFlow — Complete Project Architecture & Request-Response Flow

This document explains the step-by-step technical execution flow of the TaskFlow application for viva presentations and code inspection.

---

## 1. Complete Request-Response Lifecycle Flow

When a user performs an action in the application (for example, creating a task, filtering tasks, or viewing dashboard stats), the data travels through the following layers:

```
┌────────────────────────────────────────────────────────┐
│ 1. React Frontend (Browser)                           │
│    User clicks "Create Task" in Tasks.jsx              │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 2. Axios Service (src/services/api.js)                 │
│    Attaches JWT Token in Authorization header:         │
│    "Bearer eyJhbGciOi..."                              │
└──────────────────────────┬─────────────────────────────┘
                           │ HTTP Request (e.g. POST /api/tasks)
                           ▼
┌────────────────────────────────────────────────────────┐
│ 3. Express Server (backend/server.js)                  │
│    Parses JSON body via express.json() & checks CORS   │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 4. Express Routes (backend/routes/taskRoutes.js)       │
│    Matches URL pattern "/api/tasks"                    │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 5. Middleware (backend/middleware/authMiddleware.js)   │
│    - Extracts Bearer token                             │
│    - Verifies token signature using JWT_SECRET         │
│    - Fetches User from DB and attaches to req.user     │
└──────────────────────────┬─────────────────────────────┘
                           │ Calls next()
                           ▼
┌────────────────────────────────────────────────────────┐
│ 6. Controller (backend/controllers/taskController.js)  │
│    Executes business logic: validates title, associates│
│    user ID (req.user._id), and prepares data           │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 7. Mongoose Model (backend/models/Task.js)             │
│    Validates schema rules, types, default values       │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 8. MongoDB Database Engine                             │
│    Inserts document into "tasks" collection            │
└──────────────────────────┬─────────────────────────────┘
                           │ Returns saved document
                           ▼
┌────────────────────────────────────────────────────────┐
│ 9. Express Controller sends JSON Response              │
│    res.status(201).json(savedTask)                     │
└──────────────────────────┬─────────────────────────────┘
                           │ HTTP 201 Created Response
                           ▼
┌────────────────────────────────────────────────────────┐
│ 10. React Interface Update                             │
│     Axios returns data to component, useState triggers │
│     re-render, and new TaskCard appears instantly!     │
└────────────────────────────────────────────────────────┘
```

---

## 2. Authentication Flow (Registration & Login)

```
[User Form in Browser]
       │
       │ Enters Name, Email, Password
       ▼
[POST /api/auth/register or /login]
       │
       ▼
[authController.js]
  ├── Register:
  │     1. Validates input
  │     2. Checks User.findOne({ email }) to ensure uniqueness
  │     3. Generates salt via bcrypt.genSalt(10)
  │     4. Hashes password via bcrypt.hash(password, salt)
  │     5. Saves new User with role 'User'
  │     6. Signs JWT: jwt.sign({ id: user._id }, JWT_SECRET, { expiresIn: '7d' })
  │
  └── Login:
        1. Finds user by email
        2. Compares plain password with hash: bcrypt.compare(password, user.password)
        3. If matching, signs and returns JWT token
       │
       ▼
[Frontend Response Handler]
  ├── Saves token to localStorage.setItem('token', token)
  ├── Saves user info to localStorage.setItem('user', JSON.stringify(user))
  └── Redirects user to /dashboard via React Router navigate('/dashboard')
```

---

## 3. Real-Time Socket.IO Notification Flow

```
[User Logs In to Frontend]
       │
       ▼
[App.jsx Initializes Socket Client]
  ├── const socket = io('http://localhost:5001')
  └── socket.emit('join', user._id)
       │
       ▼
[server.js on Backend]
  └── socket.on('join', (userId) => socket.join(userId))
      Backend socket joins a dedicated private room identified by userId

                     ... Later ...

[Task Status Changed]
  ├── User changes status in UI (e.g. from "Pending" to "Completed")
  ├── Frontend sends PUT /api/tasks/:id { status: "Completed" }
  ├── taskController.js detects status change
  ├── Retrieves io instance via req.app.get('io')
  └── Emits:
        io.to(task.user.toString()).emit('taskStatusUpdated', {
          title: task.title,
          oldStatus: 'Pending',
          newStatus: 'Completed',
          message: 'Task "Design Schemas" status changed to Completed'
        })
       │
       ▼
[Socket.IO Client in App.jsx Receives Event]
  ├── socket.on('taskStatusUpdated', (data) => setNotification(data))
  └── Renders floating notification toast in top-right corner of the screen
      Auto-dismisses after 5 seconds!
```

---

## 4. Dashboard Aggregation Pipeline Flow

When the user visits the Dashboard, instead of fetching hundreds of task records and counting them in JavaScript loops, TaskFlow leverages **MongoDB's Aggregation Framework** directly:

```javascript
Task.aggregate([
  // Stage 1: $match
  // Filters documents down to only those owned by the authenticated user
  {
    $match: { user: new mongoose.Types.ObjectId(req.user._id) }
  },

  // Stage 2: $group
  // Groups matching documents by their 'status' field ('Pending', 'In Progress', 'Completed')
  // and increments count by 1 for each document
  {
    $group: {
      _id: '$status',
      count: { $sum: 1 }
    }
  }
])
```

- **Why this is better:**
  - Computation happens directly inside the database engine using C++ optimized routines.
  - Minimal network bandwidth consumed between database and Node.js backend.
  - Perfect demonstration of advanced database concepts for the semester viva evaluation.
