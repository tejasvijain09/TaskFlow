# TaskFlow — Task Management System (MERN Stack)

**TaskFlow** is a modern, responsive, beginner-friendly task management web application built using the complete **MERN Stack** (MongoDB, Express.js, React.js, and Node.js). 

Developed as a semester project for **CSF402: Programming Node JS Applications** under the supervision of **Mr. Jitesh Kumar Bhatia**.

---

## 👥 Development Team & Module Distribution

| Member Name | Registration No. | Module Assigned | Key Focus Areas |
| :--- | :--- | :--- | :--- |
| **Suraj Yadav** | 12326764 | **Module 1: Authentication & User Management** | User registration, login, bcrypt password hashing, JWT tokens, auth middleware, role authorization |
| **Arpan Dey** | 12305886 | **Module 2: Task Management** | Task CRUD, status/priority tracking, server-side filtering, multi-field sorting, pagination |
| **Tejasvi** | 12315197 | **Module 3: Dashboard Analytics & Integration** | MongoDB aggregation pipeline, Socket.IO real-time alerts, Swagger docs, admin panel, system integration |

For in-depth module responsibility documentation, see [TEAM_DIVISION.md](TEAM_DIVISION.md) and [VIVA_PREPARATION.md](VIVA_PREPARATION.md).

---

## 🚀 Key Features

- **🔐 Secure Authentication:** User registration, password encryption using `bcrypt` (10 rounds), and stateless session authentication using JSON Web Tokens (JWT).
- **🛡️ Role-Based Access Control:** Strict separation between standard **Users** (own task isolation) and **Administrators** (platform-wide oversight).
- **📋 Full Task CRUD:** Create, read, update details/status, and delete tasks with ownership checks.
- **🔍 Filtering, Sorting & Pagination:**
  - Filter by **Status** (`Pending`, `In Progress`, `Completed`) and **Priority** (`Low`, `Medium`, `High`).
  - Sort by **Due Date**, **Creation Date**, or **Title** (`Ascending` / `Descending`).
  - Server-side pagination with `skip()` and `limit()`.
- **📊 MongoDB Aggregation Dashboard:** 4 KPI summary cards (Total, Pending, In Progress, Completed) and recent tasks computed directly inside MongoDB using `$match` and `$group`.
- **🔔 Real-Time Notifications:** Instant task status change notifications pushed to the user's browser via **Socket.IO** rooms without page reloads.
- **📖 Swagger / OpenAPI Documentation:** Interactive API documentation and testing sandbox accessible at `/api-docs`.
- **🎨 Clean, Modern User Interface:** Built with React 18, Vite, and clean plain CSS without bulky third-party UI libraries.

---

## 🛠️ Technology Stack

- **Frontend:** React.js (v18), React Router (v6), Axios, Socket.IO Client, Vite
- **Backend:** Node.js (v18+), Express.js (v4), Socket.IO (v4), Cors, Dotenv
- **Database:** MongoDB with Mongoose ODM (v8)
- **Security:** JSON Web Tokens (`jsonwebtoken`), Password Hashing (`bcryptjs`)
- **Documentation:** Swagger UI Express, Swagger JSDoc (OpenAPI 3.0)

---

## 📁 Project Folder Structure

```
TaskFlow/
│
├── backend/
│   ├── config/
│   │   ├── db.js             # MongoDB connection setup
│   │   └── swagger.js        # Swagger / OpenAPI specification
│   ├── models/
│   │   ├── User.js           # User schema (Name, Email, Password, Role)
│   │   └── Task.js           # Task schema (Title, Status, Priority, DueDate, User ref)
│   ├── controllers/
│   │   ├── authController.js       # Register, Login, Profile logic
│   │   ├── taskController.js       # CRUD, Filters, Sorting, Pagination
│   │   ├── dashboardController.js  # MongoDB Aggregation pipeline
│   │   └── adminController.js      # Admin users & tasks management
│   ├── routes/
│   │   ├── authRoutes.js           # /api/auth routes
│   │   ├── taskRoutes.js           # /api/tasks routes
│   │   ├── dashboardRoutes.js      # /api/dashboard routes
│   │   └── adminRoutes.js          # /api/admin routes
│   ├── middleware/
│   │   ├── authMiddleware.js       # JWT verification & req.user attachment
│   │   └── adminMiddleware.js      # Admin role validation
│   ├── seed.js               # Database seeder for demo credentials
│   ├── server.js             # Express app & Socket.IO server entrypoint
│   ├── package.json
│   ├── .env.example
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx          # Header with user greeting & logout
│   │   │   ├── Sidebar.jsx         # Clean navigation sidebar
│   │   │   ├── TaskCard.jsx        # Individual task card with action triggers
│   │   │   └── ProtectedRoute.jsx  # Auth & role guard wrapper
│   │   ├── pages/
│   │   │   ├── Login.jsx           # Sign-in with quick demo fill buttons
│   │   │   ├── Register.jsx        # Account registration with validation
│   │   │   ├── Dashboard.jsx       # 4 KPI cards & recent task table
│   │   │   ├── Tasks.jsx           # Task CRUD, filters, modal & pagination
│   │   │   └── Admin.jsx           # Admin user & task management panel
│   │   ├── services/
│   │   │   └── api.js              # Axios instance with Bearer interceptor
│   │   ├── App.jsx                 # Routing & Socket.IO real-time toast
│   │   ├── main.jsx
│   │   └── index.css               # Clean, modern custom CSS
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── README.md                 # Master project documentation
├── TEAM_DIVISION.md          # Detailed team responsibilities
├── PROJECT_FLOW.md           # Visual architecture & request-response flow
├── VIVA_PREPARATION.md       # Complete 3-member viva guide with 45+ questions
└── .gitignore
```

---

## ⚡ Prerequisites

Ensure the following tools are installed on your system:
- **Node.js** (v18.0.0 or higher) — check with `node -v`
- **npm** (v9.0.0 or higher) — check with `npm -v`
- **MongoDB** (v6.0 or higher running locally on port 27017 or a MongoDB Atlas cloud URI)

---

## 📥 Installation & Setup Instructions

### 1. Clone or Open the Project
Open terminal and navigate to the project directory:
```bash
cd TaskFlow
```

### 2. Configure Backend Environment
Navigate into `backend` and create your `.env` configuration file:
```bash
cd backend
cp .env.example .env
```

Your `backend/.env` file:
```env
PORT=5001
MONGO_URI=mongodb://127.0.0.1:27017/taskflow
JWT_SECRET=taskflow_super_secret_jwt_key_csf402_project_2026
```
*(Note: Port 5001 is used by default to prevent conflicts with macOS AirPlay Receiver on port 5000).*

### 3. Install Backend Dependencies & Seed Sample Data
From inside `backend`:
```bash
npm install
npm run seed
```
This populates MongoDB with an Administrator account, standard test account, and sample categorized tasks!

### 4. Install Frontend Dependencies
Open a second terminal window and navigate to `frontend`:
```bash
cd frontend
npm install
```

---

## 🏃 Running the Application

### Start Backend Server:
```bash
cd backend
npm run dev
# or: npm start
```
*Backend runs at:* **`http://localhost:5001`**  
*Swagger Documentation:* **`http://localhost:5001/api-docs`**

### Start Frontend Server:
```bash
cd frontend
npm run dev
```
*Frontend runs at:* **`http://localhost:5173`**

---

## 🔑 Demo Credentials for College Evaluation

The database seeder (`seed.js`) provides two ready-to-use accounts:

| Role | Email | Password | Access Rights |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@taskflow.com` | `admin123` | Full access to Dashboard, My Tasks, and Admin Control Panel |
| **Standard User** | `suraj@taskflow.com` | `user123` | Personal Dashboard and My Tasks CRUD (Isolated data) |

You can also click the **Demo User** or **Demo Admin** buttons directly on the Login page to fill credentials in one click!

---

## 📡 API Reference Overview

| HTTP Method | Endpoint | Description | Access Level |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Register new standard user | Public |
| `POST` | `/api/auth/login` | Authenticate and receive JWT | Public |
| `GET` | `/api/auth/me` | Fetch currently logged-in user profile | Protected (User) |
| `POST` | `/api/tasks` | Create a new task | Protected (User) |
| `GET` | `/api/tasks` | Query tasks (with status, priority, sort, page) | Protected (User) |
| `GET` | `/api/tasks/:id` | Fetch task by ID | Protected (Owner/Admin) |
| `PUT` | `/api/tasks/:id` | Update task fields or status | Protected (Owner/Admin) |
| `DELETE` | `/api/tasks/:id` | Delete task | Protected (Owner/Admin) |
| `GET` | `/api/dashboard/stats` | Aggregation KPI metrics & recent tasks | Protected (User/Admin) |
| `GET` | `/api/admin/users` | List all registered user accounts | Protected (Admin Only) |
| `GET` | `/api/admin/tasks` | List all platform tasks with owner info | Protected (Admin Only) |
| `DELETE` | `/api/admin/tasks/:id` | Admin delete of inappropriate task | Protected (Admin Only) |
| `GET` | `/api-docs` | Interactive Swagger API documentation | Public |

---

## 🛠️ Common Troubleshooting

1. **Port 5000 in use (`EADDRINUSE`):**
   - On macOS, the AirPlay Receiver service occupies port 5000. TaskFlow uses port `5001` out of the box to prevent this issue.
2. **MongoDB Connection Refused (`ECONNREFUSED 127.0.0.1:27017`):**
   - Ensure the MongoDB daemon is active. Start it using `brew services start mongodb-community` or run `mongod --dbpath <data_folder>`.
3. **CORS Errors in Browser Console:**
   - Verify that `cors()` is mounted in `backend/server.js` and that the backend server is running on port 5001.
4. **401 Unauthorized Errors:**
   - If a JWT token expires after 7 days, log out and sign in again to receive a fresh token.

---

## 📄 License
This project was developed for educational and academic submission purposes for the B.Tech CSE Degree Course at Lovely Professional University.
