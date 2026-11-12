# TaskFlow — Comprehensive Viva Preparation Guide

**Course:** CSF402: Programming Node JS Applications  
**Evaluator / Faculty:** Mr. Jitesh Kumar Bhatia  
**Project:** TaskFlow – Task Management System (MERN Stack)

---

## 📋 Table of Contents
1. [Section 1: Tejasvi — Authentication & User Management](#section-1-tejasvi-reg-no-12315197)
2. [Section 2: Arpan Dey — Task Management (CRUD, Filters, Pagination)](#section-2-arpan-dey-reg-no-12305886)
3. [Section 3: Suraj Yadav — Dashboard Analytics, Socket.IO & Integration](#section-3-suraj-yadav-reg-no-12326764)

---

# SECTION 1: TEJASVI (REG NO: 12315197)
## Module 1: Authentication and User Security

### 1. What Your Module Does
Your module handles user identity and platform security. It enables new users to register securely, verifies login credentials against hashed passwords, issues signed JSON Web Tokens (JWT), extracts and validates user identity on incoming requests via middleware, and blocks non-admin users from administrative endpoints.

### 2. Files You Must Understand Thoroughly
- `backend/models/User.js`
- `backend/controllers/authController.js`
- `backend/routes/authRoutes.js`
- `backend/middleware/authMiddleware.js`
- `backend/middleware/adminMiddleware.js`
- `frontend/src/pages/Login.jsx`
- `frontend/src/pages/Register.jsx`
- `frontend/src/components/ProtectedRoute.jsx`

### 3. Explanation of Important Files
- **`User.js`**: Contains Mongoose schema for user entities. Fields: `name`, `email` (unique, lowercase, trimmed), `password` (hashed string), `role` (`User` or `Admin`, defaults to `User`), and timestamps (`createdAt`, `updatedAt`).
- **`authController.js`**: Houses business logic for `registerUser`, `loginUser`, `getMe`, and the `generateToken` helper function.
- **`authMiddleware.js`**: Intercepts requests, reads `Authorization: Bearer <token>`, verifies JWT with `jwt.verify()`, queries MongoDB for user details without password, and assigns to `req.user`.
- **`adminMiddleware.js`**: Simple gatekeeper that checks `if (req.user && req.user.role === 'Admin')`. Returns 403 Forbidden if not.
- **`ProtectedRoute.jsx`**: React route wrapper checking `localStorage.getItem('token')`. Redirects to `/login` if unauthenticated or `/dashboard` if non-admin tries to visit admin routes.

### 4. Explanation of Important Functions
- `generateToken(id)`: Uses `jwt.sign({ id }, process.env.JWT_SECRET, { expiresIn: '7d' })`. Signs the user ID into an encrypted token payload.
- `registerUser(req, res)`:
  1. Validates `name`, `email`, `password`.
  2. Runs `User.findOne({ email })` to reject duplicate accounts.
  3. Uses `bcrypt.genSalt(10)` and `bcrypt.hash(password, salt)` to hash password.
  4. Saves user document with role strictly set to `'User'`.
  5. Returns 201 status with JWT token and user info (excluding password).
- `loginUser(req, res)`:
  1. Finds user document by email.
  2. Compares incoming plain text password against hashed database password with `await bcrypt.compare(password, user.password)`.
  3. Returns JWT token on success or 401 Unauthorized on failure.
- `protect(req, res, next)`: Decodes bearer token, verifies signature, assigns `req.user`, and invokes `next()`.

### 5. API Endpoints in Your Module
- `POST /api/auth/register` — Register a new account.
- `POST /api/auth/login` — Login and receive JWT token.
- `GET /api/auth/me` — Protected endpoint returning logged-in user profile.

### 6. Frontend to Backend Communication
In `Login.jsx` and `Register.jsx`, form submissions trigger `API.post('/auth/login', { email, password })`. On success, token and user JSON are written to browser `localStorage`. For subsequent requests, the Axios interceptor in `api.js` attaches `Authorization: Bearer <token>`.

### 7. Key MongoDB Queries Used
- `User.findOne({ email: email.toLowerCase() })` — Checks existence of email.
- `User.create({ name, email, password: hashedPassword, role: 'User' })` — Saves new user.
- `User.findById(decoded.id).select('-password')` — Fetches user profile without exposing password hash.

### 8. 15 Teacher Viva Questions & Direct Code Answers

**Q1: Why do we use bcrypt instead of storing plain-text passwords?**  
*Answer:* Storing plain passwords is a major vulnerability. If database access is compromised, all user passwords leak. `bcrypt` uses one-way mathematical hashing with a configurable salt (we use 10 rounds) so the original password can never be reversed.

**Q2: What is the purpose of salt in bcrypt?**  
*Answer:* A salt is random data added before hashing. It prevents "rainbow table" lookup attacks where precomputed tables of hashes could crack commonly used passwords.

**Q3: How does JWT work in this project?**  
*Answer:* Upon login, `authController.js` calls `jwt.sign()` containing the user's `_id` and signed with `JWT_SECRET`. The client stores this string in `localStorage` and sends it in the `Authorization` HTTP header. Our backend verifies the signature on protected requests statelessly.

**Q4: What are the three parts of a JWT token?**  
*Answer:* Header (algorithm & token type), Payload (claims like user id and expiration date), and Signature (header + payload encrypted using secret key).

**Q5: Why is JWT called stateless?**  
*Answer:* Because the server does not keep session records in server memory or database for each logged-in user. The token carries verifiable proof of identity, allowing easy horizontal scaling.

**Q6: What happens if someone modifies the payload of a JWT in the browser?**  
*Answer:* The cryptographic signature will not match because the attacker does not have `process.env.JWT_SECRET`. `jwt.verify()` throws an error and returns 401 Unauthorized.

**Q7: How do you prevent a regular user from registering as an Admin?**  
*Answer:* In `authController.js`, inside `registerUser`, we hardcode `role: 'User'`. We do not read `req.body.role`, completely preventing privilege escalation during registration.

**Q8: Explain the `select('-password')` in `authMiddleware.js`.**  
*Answer:* When querying MongoDB for the user document, the minus sign tells Mongoose to omit the `password` field from the returned object so sensitive data is never attached to `req.user` or exposed.

**Q9: What HTTP status code is returned for bad login credentials?**  
*Answer:* `401 Unauthorized`. For validation errors like missing fields, we return `400 Bad Request`.

**Q10: Why do we use `email.toLowerCase()`?**  
*Answer:* To ensure case-insensitive email matching. Without it, `User@Example.com` and `user@example.com` could create duplicate accounts.

**Q11: How does `ProtectedRoute.jsx` prevent unauthorized page access?**  
*Answer:* It reads `localStorage.getItem('token')`. If absent, it returns `<Navigate to="/login" replace />`. If `adminOnly={true}` and `user.role !== 'Admin'`, it redirects to `/dashboard`.

**Q12: Where is the JWT secret kept and why?**  
*Answer:* In the `.env` file (`process.env.JWT_SECRET`), never hardcoded in source code or pushed to Git repositories.

**Q13: How does `bcrypt.compare` work if bcrypt cannot decrypt?**  
*Answer:* `bcrypt.compare` extracts the salt from the stored hash, hashes the incoming plain password with that same salt, and checks if the resulting hashes match.

**Q14: What is the difference between Authentication and Authorization?**  
*Answer:* Authentication verifies *who* the user is (handled by `authMiddleware.js`). Authorization verifies *what permissions* they have (e.g. `adminMiddleware.js` checking if role is `Admin`).

**Q15: How can an Admin account be created?**  
*Answer:* Through our secure seed script `seed.js` using `node seed.js`, which directly creates the administrator account with a hashed password in MongoDB.

### 9. Practical Demonstration Sequence for Tejasvi
1. Open `/register` in browser. Try submitting empty form and mismatched passwords to show client validation.
2. Register a new user e.g. `tejasvi.test@taskflow.com`.
3. Open MongoDB Compass or terminal, show that the password is saved as a secure `$2a$10$...` hash.
4. Log in and open Browser DevTools -> Application -> Local Storage. Point out `token` and `user`.
5. Try navigating directly to `/admin` using the URL bar, and show how the route guard prevents access.

---

# SECTION 2: ARPAN DEY (REG NO: 12305886)
## Module 2: Task Management (CRUD, Filtering, Sorting, Pagination)

### 1. What Your Module Does
Your module is the operational core of TaskFlow. It allows authenticated users to create tasks, browse only their own tasks, update task details (title, description, status, priority, due date), and delete tasks. It also implements URL query parameter filtering (by status and priority), multi-field sorting, and server-side pagination with limit and skip.

### 2. Files You Must Understand Thoroughly
- `backend/models/Task.js`
- `backend/controllers/taskController.js`
- `backend/routes/taskRoutes.js`
- `frontend/src/pages/Tasks.jsx`
- `frontend/src/components/TaskCard.jsx`

### 3. Explanation of Important Files
- **`Task.js`**: Mongoose model with fields:
  - `title` (String, required, trimmed)
  - `description` (String, default empty)
  - `status` (Enum: `Pending`, `In Progress`, `Completed`, default: `Pending`)
  - `priority` (Enum: `Low`, `Medium`, `High`, default: `Medium`)
  - `dueDate` (Date)
  - `user` (`ObjectId`, references `User` model, required)
  - Timestamps (`createdAt`, `updatedAt`)
  - Compound indexes on `{ user: 1, status: 1 }`, `{ user: 1, priority: 1 }`, and `{ user: 1, dueDate: 1 }`.
- **`taskController.js`**:
  - `createTask`: Links task to `req.user._id`.
  - `getTasks`: Applies filters, sorting, and pagination.
  - `getTaskById`: Validates ownership before returning single task.
  - `updateTask`: Validates ownership, saves updates, emits Socket.IO event if status changes.
  - `deleteTask`: Ensures only the task owner (or Admin) can delete.
- **`Tasks.jsx`**: Main task screen with search toolbar, task grid, modal dialog for create/edit, and pagination buttons.
- **`TaskCard.jsx`**: Card component with visual badges, quick status dropdown, and Edit/Delete buttons.

### 4. Explanation of Important Functions
- `createTask`: Reads body, assigns `user: req.user._id`, calls `Task.create()`, returns HTTP 201.
- `getTasks`:
  ```javascript
  const query = { user: req.user._id };
  if (status && status !== 'All') query.status = status;
  if (priority && priority !== 'All') query.priority = priority;
  const skip = (page - 1) * limit;
  const tasks = await Task.find(query).sort({ [sortBy]: sortOrder }).skip(skip).limit(limit);
  ```
- `updateTask`: Checks `if (task.user.toString() !== req.user._id.toString() && req.user.role !== 'Admin')`. Updates fields and saves.
- `deleteTask`: Checks ownership, calls `await task.deleteOne()`.

### 5. API Endpoints in Your Module
- `POST /api/tasks` — Create new task.
- `GET /api/tasks` — List tasks with query params (`?status=Pending&priority=High&sortBy=dueDate&order=asc&page=1&limit=6`).
- `GET /api/tasks/:id` — View single task.
- `PUT /api/tasks/:id` — Update task or status.
- `DELETE /api/tasks/:id` — Delete task.

### 6. Frontend to Backend Communication
`Tasks.jsx` uses `API.get('/tasks', { params })` to fetch tasks. When user clicks "Add Task", a modal form submits `API.post('/tasks', formData)`. Quick status dropdown triggers `API.put('/tasks/:id', { status })`. After any operation, `fetchTasks()` is re-invoked to refresh the UI.

### 7. Key MongoDB Queries Used
- `Task.create({ ...req.body, user: req.user._id })`
- `Task.find(query).sort(...).skip(skip).limit(limit)`
- `Task.countDocuments(query)` — Counts matching tasks to calculate `totalPages`.
- `Task.findById(id)`
- `task.deleteOne()`

### 8. 15 Teacher Viva Questions & Direct Code Answers

**Q1: How do you ensure User A cannot see User B's tasks?**  
*Answer:* In `taskController.js`, inside `getTasks`, we set `const query = { user: req.user._id }`. The database query is locked to the authenticated user's ID extracted from their verified JWT token.

**Q2: How does pagination work in MongoDB?**  
*Answer:* Using `skip()` and `limit()`. For page 1 with limit 5, skip is 0. For page 2 with limit 5, skip is `(2 - 1) * 5 = 5`. `limit(5)` specifies how many documents to return.

**Q3: How do you calculate total pages for pagination?**  
*Answer:* `Math.ceil(totalTasks / limitNum)`. For example, 11 tasks with limit 5 gives `Math.ceil(11 / 5) = 3` pages.

**Q4: Why do we add indexes to `Task.js`?**  
*Answer:* Without indexes, MongoDB performs a full collection scan (checking every document). With indexes on `{ user: 1, status: 1 }`, MongoDB uses a B-tree index to find matching tasks in `O(log N)` time.

**Q5: What are Mongoose timestamps?**  
*Answer:* Passing `{ timestamps: true }` in `new mongoose.Schema(..., { timestamps: true })` tells Mongoose to automatically create and manage `createdAt` and `updatedAt` Date fields.

**Q6: How do you implement sorting in Mongoose?**  
*Answer:* Using `.sort({ [sortBy]: sortOrder })` where `sortOrder` is `1` for ascending and `-1` for descending.

**Q7: What is the purpose of `ref: 'User'` in `Task.js`?**  
*Answer:* It tells Mongoose that the `user` field stores an `ObjectId` referencing the `User` collection, enabling relationship modeling and `.populate('user')`.

**Q8: What happens if a user submits an empty task title?**  
*Answer:* In `taskController.js`, we check `if (!title || title.trim() === '')` and return `400 Bad Request` with `{ message: 'Task title is required' }`. The Mongoose schema also enforces `required: true`.

**Q9: Why do we use `task.user.toString() === req.user._id.toString()`?**  
*Answer:* In MongoDB, IDs are `ObjectId` instances, which are objects. Direct object comparison (`===`) checks memory reference and would return false even if IDs are identical. Converting both to strings ensures proper value comparison.

**Q10: What HTTP verbs are used for CRUD operations?**  
*Answer:* `POST` for Create, `GET` for Read, `PUT` for Update, and `DELETE` for Delete.

**Q11: Can a user change just the status without resending all task fields?**  
*Answer:* Yes. In `updateTask`, we check `if (status !== undefined) task.status = status;` so partial updates work cleanly.

**Q12: How does the frontend know which page button is active?**  
*Answer:* In `Tasks.jsx`, we compare `currentPage === pageNum` and dynamically append the CSS class `active`.

**Q13: How is date formatting handled on the frontend?**  
*Answer:* Using JavaScript's `new Date(dateString).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })`.

**Q14: What is the benefit of using URL query parameters for filtering?**  
*Answer:* Query parameters follow RESTful conventions (e.g. `/api/tasks?status=Pending&priority=High`). They allow multiple optional filters in any combination without modifying route paths.

**Q15: How does the modal work in React without third-party libraries?**  
*Answer:* We use a simple boolean state `isModalOpen`. When true, React renders an overlay `div` with absolute/fixed positioning over the content.

### 9. Practical Demonstration Sequence for Arpan
1. Open the **My Tasks** page. Show existing tasks in the grid.
2. Click **Add New Task**, type "Complete Semester Report", select "High" priority, choose a due date, and submit. Show it appear instantly.
3. Use the filter dropdown to select **Status: In Progress**. Show how other statuses disappear.
4. Select **Priority: High** to demonstrate combined multi-parameter filtering.
5. Change sorting to **Due Date (Ascending)**.
6. Click **Delete** on a task, confirm the dialog, and show it removed from the UI.

---

# SECTION 3: SURAJ YADAV (REG NO: 12326764)
## Module 3: Dashboard Analytics, Socket.IO & System Integration

### 1. What Your Module Does
Your module delivers high-level visibility and platform integration. You implemented MongoDB's Aggregation Pipeline to compute dashboard KPI statistics, integrated Socket.IO for real-time task status notifications, set up interactive Swagger/OpenAPI documentation (`/api-docs`), developed the Administrator control panel, created the seeder script, and unified the React frontend with Express backend.

### 2. Files You Must Understand Thoroughly
- `backend/controllers/dashboardController.js`
- `backend/routes/dashboardRoutes.js`
- `backend/controllers/adminController.js`
- `backend/routes/adminRoutes.js`
- `backend/config/swagger.js`
- `backend/server.js` (Socket.IO & Express configuration)
- `backend/seed.js` (Database seeder)
- `frontend/src/pages/Dashboard.jsx`
- `frontend/src/pages/Admin.jsx`
- `frontend/src/App.jsx` (Socket.IO client & toast)
- `frontend/src/services/api.js` (Axios interceptor)
- `frontend/src/components/Navbar.jsx`
- `frontend/src/components/Sidebar.jsx`

### 3. Explanation of Important Files
- **`dashboardController.js`**: Implements MongoDB aggregation pipeline using `$match` and `$group` stages to calculate total, pending, in-progress, and completed counts, plus fetches the 5 most recent tasks.
- **`server.js`**: Integrates HTTP server, Express, Socket.IO with CORS, route registrations, and Swagger UI.
- **`swagger.js`**: OpenAPI 3.0 specification config with JWT Bearer security definitions.
- **`seed.js`**: Script that safely wipes and seeds default Admin (`admin@taskflow.com`), demo student (`suraj@taskflow.com`), and 6 sample tasks with realistic timestamps.
- **`adminController.js`**: Contains `getAllUsers`, `getAllTasks` with `.populate('user', 'name email')`, and `deleteAdminTask`.
- **`Dashboard.jsx`**: Visual dashboard rendering 4 statistics cards and recent tasks table.
- **`Admin.jsx`**: Administrative view with tab toggles for Registered Users and Platform Tasks.
- **`App.jsx`**: Listens for `taskStatusUpdated` Socket.IO events and renders floating toasts.

### 4. Explanation of Important Functions
- `getDashboardStats`:
  ```javascript
  const statsAggregation = await Task.aggregate([
    { $match: matchStage },
    { $group: { _id: '$status', count: { $sum: 1 } } }
  ]);
  ```
  Processes status distribution directly inside the database engine.
- Socket.IO Server Setup in `server.js`:
  ```javascript
  io.on('connection', (socket) => {
    socket.on('join', (userId) => socket.join(userId));
  });
  ```
  Attaches `io` to Express app via `app.set('io', io)`.
- Socket.IO Emission in `taskController.js`:
  ```javascript
  const io = req.app.get('io');
  if (io) {
    io.to(task.user.toString()).emit('taskStatusUpdated', {
      title: task.title,
      newStatus: task.status,
      message: `Task "${task.title}" status changed to ${task.status}`
    });
  }
  ```

### 5. API Endpoints in Your Module
- `GET /api/dashboard/stats` — Aggregation stats and recent tasks.
- `GET /api/admin/users` — List registered users (Admin only).
- `GET /api/admin/tasks` — List all platform tasks (Admin only).
- `DELETE /api/admin/tasks/:id` — Delete task (Admin only).
- `GET /api-docs` — Swagger UI API documentation.

### 6. Frontend to Backend Communication
`Dashboard.jsx` calls `API.get('/dashboard/stats')`. When task statuses change, backend Socket.IO emits directly to the user's room. `App.jsx` handles this via `socket.on('taskStatusUpdated')` and triggers a toast component.

### 7. Key MongoDB Queries Used
- `Task.aggregate([{ $match: ... }, { $group: ... }])`
- `Task.find().populate('user', 'name email').sort({ createdAt: -1 })` — Populates user details into task records.
- `User.find().select('-password')` — Fetches user list safely.

### 8. 15 Teacher Viva Questions & Direct Code Answers

**Q1: What is a MongoDB Aggregation Pipeline?**  
*Answer:* A multi-stage framework for data transformation and analytics. Documents pass through stages (like `$match` then `$group`), where each stage transforms the documents and passes the output to the next stage.

**Q2: Explain the stages in your dashboard aggregation.**  
*Answer:* 
Stage 1 is `$match: { user: req.user._id }`, which filters tasks to only the current user.  
Stage 2 is `$group: { _id: '$status', count: { $sum: 1 } }`, which groups tasks by their status value and counts occurrences.

**Q3: Why use aggregation instead of counting in JavaScript with `array.filter().length`?**  
*Answer:* Aggregation executes inside MongoDB's C++ database engine. If a user has 10,000 tasks, JavaScript filtering requires transferring all 10,000 documents over the network. Aggregation computes the 3 numbers in the database and returns only the final count, saving RAM and bandwidth.

**Q4: How does Socket.IO differ from standard HTTP REST requests?**  
*Answer:* HTTP is unidirectional and request-driven (client requests, server responds). Socket.IO establishes a persistent, full-duplex TCP WebSocket connection, allowing the server to push real-time events to the client instantly without the client polling.

**Q5: What is a Socket.IO "room"?**  
*Answer:* A room is an arbitrary channel that sockets can join or leave. In our project, when a user logs in, they join a room named after their `userId` (`socket.join(userId)`). This allows the server to send private notifications directly to that specific user via `io.to(userId).emit()`.

**Q6: What is Swagger / OpenAPI?**  
*Answer:* An industry-standard specification for documenting REST APIs. We use `swagger-ui-express` and `swagger-jsdoc` to generate interactive documentation at `/api-docs` directly from JSDoc comments in route files.

**Q7: How do you test protected endpoints inside Swagger UI?**  
*Answer:* In `swagger.js`, we configured a `bearerAuth` security scheme. In Swagger UI, click the **Authorize** button, paste the JWT token (`Bearer <token>`), and Swagger automatically attaches it to subsequent test requests.

**Q8: What does Mongoose `.populate('user', 'name email')` do?**  
*Answer:* It performs a foreign-key-like lookup. Since `Task.user` stores an `ObjectId`, `.populate()` replaces that ID with the actual `User` document containing `name` and `email` from the users collection.

**Q9: How do you prevent ordinary users from accessing `/api/admin` endpoints?**  
*Answer:* By combining two middlewares: `router.use(protect)` (verifies valid JWT token) followed by `router.use(requireAdmin)` (checks `req.user.role === 'Admin'`). If role is not Admin, it immediately returns `403 Forbidden`.

**Q10: What is CORS and why is it needed?**  
*Answer:* Cross-Origin Resource Sharing. Browsers block requests between different origins by default (e.g. frontend on `localhost:5173` calling backend on `localhost:5001`). The `cors()` middleware adds response headers (`Access-Control-Allow-Origin: *`) to permit communication.

**Q11: How does the Axios request interceptor work?**  
*Answer:* In `api.js`, `API.interceptors.request.use()` intercepts outgoing HTTP calls right before transmission, retrieves `localStorage.getItem('token')`, and adds `config.headers.Authorization = 'Bearer ' + token`.

**Q12: What does the Axios response interceptor do?**  
*Answer:* It intercepts responses. If an API returns `401 Unauthorized` (e.g. token expired), it clears `localStorage` and redirects the user to `/login`.

**Q13: How does the Admin page differ from the regular user Task page?**  
*Answer:* The regular Task page only fetches tasks belonging to the logged-in user. The Admin page calls `/api/admin/tasks`, which returns all tasks across all users on the platform with their creator's name and email, and provides an admin delete action.

**Q14: Where is Socket.IO initialized on the backend?**  
*Answer:* In `server.js`, we wrap the Express `app` with Node's native `http.createServer(app)` and pass that server instance to `new Server(server, { cors: { origin: '*' } })`.

**Q15: Why is `app.set('io', io)` used in `server.js`?**  
*Answer:* It attaches the Socket.IO instance to the Express app. In controllers like `taskController.js`, we retrieve it via `req.app.get('io')` to emit notifications without circular file imports.

### 9. Practical Demonstration Sequence for Suraj
1. Open `/dashboard` and point out the 4 statistic cards and recent tasks list generated via MongoDB aggregation.
2. Open two browser tabs side by side logged in to the same user. On Tab 1, go to **My Tasks** and change a task status from "In Progress" to "Completed".
3. Immediately point out the real-time floating notification toast appearing on Tab 2 via Socket.IO without refreshing the page!
4. Open `http://localhost:5001/api-docs` in the browser. Show the Swagger UI, click **Authorize**, input token, and execute `GET /api/dashboard/stats`.
5. Log in as Administrator (`admin@taskflow.com` / `admin123`), navigate to **Admin Panel**, show all registered users and all platform tasks, and delete a task.
