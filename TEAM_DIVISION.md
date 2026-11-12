# TaskFlow — Team Division & Module Responsibilities

**Course:** CSF402: Programming Node JS Applications  
**Supervisor / Professor:** Mr. Jitesh Kumar Bhatia  
**Project:** TaskFlow – Task Management System (MERN Stack)

---

## 👥 Team Overview & Work Distribution Matrix

| Team Member | Registration No. | Assigned Module | Key Scope & Deliverables |
| :--- | :--- | :--- | :--- |
| **Tejasvi** | **12315197** | **Module 1: Authentication & User Management** | User registration, login, bcrypt password hashing, JWT token generation & verification, auth middleware, and route security. |
| **Arpan Dey** | **12305886** | **Module 2: Task Management (CRUD, Filters, Pagination)** | Task schema with compound indexes, full task CRUD, status & priority toggles, multi-parameter filtering, dynamic sorting, and pagination. |
| **Suraj Yadav** | **12326764** | **Module 3: Dashboard Analytics, Socket.IO & Integration** | MongoDB aggregation pipeline, real-time Socket.IO notifications, Swagger/OpenAPI docs, Admin control panel, seeder, and system integration. |

---

## 📌 Module 1: Tejasvi (Reg No: 12315197)
### Authentication and User Security

### 1. Scope & Core Responsibilities
- User registration with input validation and duplicate email prevention.
- One-way password hashing using `bcrypt` (10 salt rounds).
- Stateless JWT issuance upon login (`expiresIn: '7d'`).
- Route protection middleware (`protect`) that parses and verifies Bearer tokens.
- Role-based authorization middleware (`requireAdmin`) preventing privilege escalation.
- Profile retrieval endpoint (`/api/auth/me`).
- Frontend route guarding via `ProtectedRoute.jsx`.

### 2. Dedicated Source Files Owned
- **Backend:**
  - `backend/models/User.js` — User schema definition (name, email, password, role enum).
  - `backend/controllers/authController.js` — `registerUser`, `loginUser`, `getMe`, `generateToken`.
  - `backend/routes/authRoutes.js` — Auth REST endpoints and Swagger documentation annotations.
  - `backend/middleware/authMiddleware.js` — JWT Bearer token verification and `req.user` attachment.
  - `backend/middleware/adminMiddleware.js` — Admin role validation check.
- **Frontend:**
  - `frontend/src/pages/Login.jsx` — Login form with input validation and quick demo credential fill buttons.
  - `frontend/src/pages/Register.jsx` — Account registration with password confirmation matching.
  - `frontend/src/components/ProtectedRoute.jsx` — Client-side route guard based on JWT and role.

### 3. APIs Implemented
- `POST /api/auth/register` — Create new standard user.
- `POST /api/auth/login` — Authenticate credentials and return JWT token.
- `GET /api/auth/me` — Return currently authenticated user profile.

### 4. Step-by-Step Viva Demonstration Sequence
1. Navigate to `http://localhost:5173/register`. Submit the form with mismatched passwords to demonstrate client validation, then register a new user.
2. Open MongoDB database or logs and show that passwords are saved as secure `$2a$10$...` hashes, never plain text.
3. Log in with the registered credentials and inspect browser `localStorage` to show the saved JWT token.
4. Attempt to access `/admin` with a regular user account and show how `ProtectedRoute` redirects back to `/dashboard`.

---

## 📌 Module 2: Arpan Dey (Reg No: 12305886)
### Task Management (CRUD, Filtering, Sorting & Pagination)

### 1. Scope & Core Responsibilities
- Task database schema design with references (`ref: 'User'`) and compound indexes.
- Create task with title, description, status, priority, and due date.
- Read tasks strictly scoped to the logged-in user (`query.user = req.user._id`).
- Update task details and status on demand with ownership validation.
- Delete task with ownership validation.
- URL Query Filtering by status (`Pending`, `In Progress`, `Completed`) and priority (`Low`, `Medium`, `High`).
- Dynamic sorting by `dueDate`, `createdAt`, or `title` in ascending/descending order.
- Server-side pagination using Mongoose `skip()` and `limit()`.

### 2. Dedicated Source Files Owned
- **Backend:**
  - `backend/models/Task.js` — Task schema, field constraints, compound indexes (`user+status`, `user+priority`).
  - `backend/controllers/taskController.js` — `createTask`, `getTasks`, `getTaskById`, `updateTask`, `deleteTask`.
  - `backend/routes/taskRoutes.js` — Protected REST routes for `/api/tasks`.
- **Frontend:**
  - `frontend/src/pages/Tasks.jsx` — Main task management view, filters toolbar, modal form, pagination controls.
  - `frontend/src/components/TaskCard.jsx` — Individual task card displaying status/priority badges and action triggers.

### 3. APIs Implemented
- `POST /api/tasks` — Create task for authenticated user.
- `GET /api/tasks` — List tasks with query parameters (`?status=...&priority=...&sortBy=...&order=...&page=...&limit=...`).
- `GET /api/tasks/:id` — Get single task by ID.
- `PUT /api/tasks/:id` — Update task details or status.
- `DELETE /api/tasks/:id` — Delete task by ID.

### 4. Step-by-Step Viva Demonstration Sequence
1. Log in to TaskFlow and open the **My Tasks** page.
2. Click **➕ Add New Task**, fill out the modal form, and submit. Point out that the task card immediately appears in the grid.
3. Use the quick status dropdown on the card to change from `Pending` to `In Progress`.
4. Select **Status: In Progress** in the filter toolbar to prove server-side filtering works.
5. Demonstrate sorting by Due Date, then navigate through pages to demonstrate pagination math.
6. Click **Delete Task**, confirm the browser prompt, and demonstrate removal.

---

## 📌 Module 3: Suraj Yadav (Reg No: 12326764)
### Dashboard Analytics, Socket.IO & System Integration

### 1. Scope & Core Responsibilities
- Dashboard analytics computation using MongoDB's Aggregation Pipeline (`$match` + `$group`).
- Real-time bidirectional notification delivery using `Socket.IO` rooms on task status change.
- Swagger/OpenAPI documentation (`/api-docs`) with JWT Bearer scheme configuration.
- Administrator control panel (view registered users, inspect all platform tasks, administrative deletion).
- Full-stack integration connecting React (Vite), Axios interceptors, Express, and MongoDB.
- Database seeder script (`seed.js`) providing demo accounts and initial dataset.

### 2. Dedicated Source Files Owned
- **Backend:**
  - `backend/controllers/dashboardController.js` — MongoDB Aggregation pipeline (`$match`, `$group`) & recent task retrieval.
  - `backend/routes/dashboardRoutes.js` — Protected `/api/dashboard/stats` route.
  - `backend/controllers/adminController.js` — `getAllUsers`, `getAllTasks`, `deleteAdminTask`.
  - `backend/routes/adminRoutes.js` — Protected Admin-only routes.
  - `backend/config/swagger.js` — OpenAPI 3.0 specification setup.
  - `backend/server.js` — HTTP server wrapping Express, Socket.IO rooms, and middleware.
  - `backend/seed.js` — Database seeder for demo accounts and initial tasks.
- **Frontend:**
  - `frontend/src/pages/Dashboard.jsx` — 4 KPI summary cards (Total, Pending, In Progress, Completed) and recent tasks table.
  - `frontend/src/pages/Admin.jsx` — Admin management tabs for users and system-wide tasks.
  - `frontend/src/App.jsx` — Socket.IO client connection and floating toast notifications.
  - `frontend/src/services/api.js` — Axios client with automatic Bearer token interceptor.
  - `frontend/src/components/Navbar.jsx` — Header navigation with user greeting.
  - `frontend/src/components/Sidebar.jsx` — Primary navigation sidebar.

### 3. APIs Implemented
- `GET /api/dashboard/stats` — Aggregated task metrics via MongoDB aggregation.
- `GET /api/admin/users` — List all registered users (Admin only).
- `GET /api/admin/tasks` — List all platform tasks with populated user details (Admin only).
- `DELETE /api/admin/tasks/:id` — Administrative removal of inappropriate tasks.
- `GET /api-docs` — Interactive Swagger documentation UI.

### 4. Step-by-Step Viva Demonstration Sequence
1. Open `/dashboard` and point out the 4 statistic cards computed via MongoDB aggregation pipeline.
2. Open two browser windows side by side (or two tabs). Update a task status in one window, and demonstrate the real-time Socket.IO notification popup in the other without refreshing!
3. Open `http://localhost:5001/api-docs` in the browser. Show Swagger UI, click **Authorize**, input token, and execute a test request directly in Swagger.
4. Log in as Administrator (`admin@taskflow.com`), open **Admin Panel**, and show platform-wide user records and all users' tasks. Delete an inappropriate task to prove admin authority.

---

## 🤝 Teamwork & Integration Touchpoints

The modules interface cleanly without overlapping code ownership:
1. **Module 1 ➔ Module 2 & 3:** Member 1's `authMiddleware` attaches `req.user` to incoming requests, which Member 2 uses to isolate tasks (`req.user._id`) and Member 3 uses to match aggregation stages and check Admin role (`req.user.role`).
2. **Module 2 ➔ Module 3:** When Member 2's `updateTask` saves a changed status, it retrieves Member 3's `io` instance via `req.app.get('io')` and emits the real-time notification to the user's room.
3. **Module 3 ➔ All:** Member 3's Axios interceptor in `api.js` ensures every request made by Member 1's and Member 2's frontend pages automatically carries the Bearer token.
