# TaskFlow — 10-Minute Presentation & Slide Deck Guide

**Course:** CSF402: Programming Node JS Applications  
**Evaluator / Faculty Supervisor:** Mr. Jitesh Kumar Bhatia  
**Project:** TaskFlow – Task Management System (MERN Stack)  
**Presenters:** 
- **Tejasvi** (Reg No: 12315197) — *First 5 Minutes (0:00 – 5:00)*
- **Arpan Dey** (Reg No: 12305886) — *Next 5 Minutes (5:00 – 10:00)*

---

## 📂 Generated PowerPoint File
Your actual PowerPoint slide deck has been generated and saved directly in your workspace:  
📄 **`TaskFlow_Presentation.pptx`**  
*(Double-click to open in **Microsoft PowerPoint**, **Apple Keynote**, or import into **Google Slides**).*

---

## ⏱️ 10-Minute Presentation Schedule & Slide Layout

```
┌────────────────────────────────────────────────────────┐
│ MINUTES 0:00 – 1:00 : Slides 1 & 2 (Introduction)      │
│ • Joint intro, system architecture & agenda division   │
├────────────────────────────────────────────────────────┤
│ MINUTES 1:00 – 5:00 : Slides 3, 4, 5 (Tejasvi's Work)  │
│ • User Registration & bcrypt Password Hashing (Slide 3)│
│ • Stateless JWT Tokens & ProtectedRoute (Slide 4)      │
│ • MongoDB Atlas Cloud & Live DB Monitor Tool (Slide 5) │
├────────────────────────────────────────────────────────┤
│ MINUTES 5:00 – 9:00 : Slides 6, 7, 8 (Arpan's Work)    │
│ • Task Schema & Compound Indexing (Slide 6)            │
│ • Full Task CRUD with Ownership Isolation (Slide 7)    │
│ • Multi-Filtering, Sorting & Pagination (Slide 8)      │
├────────────────────────────────────────────────────────┤
│ MINUTES 9:00 – 10:00: Slides 9 & 10 (Live Demo & Q&A)  │
│ • Sequential live demonstration execution plan         │
│ • Technical summary & ready for evaluation questions   │
└────────────────────────────────────────────────────────┘
```

---

## 📸 Proof-of-Work Screenshots Checklist

The PowerPoint presentation includes pre-formatted **screenshot frames** on Slides 3 through 8. Here are the **6 screenshots to take and paste**:

| Slide | Screenshot Name | How to Capture on Your Mac (Cmd + Shift + 4) |
| :---: | :--- | :--- |
| **Slide 3** | **Registration & Login UI** | Open `http://localhost:5173/login` in your browser. Take a clean capture of the Login/Register card showing email and password fields. |
| **Slide 4** | **JWT Token in Local Storage** | In browser, press `Cmd + Option + I` ➔ **Application** tab ➔ **Local Storage** ➔ `http://localhost:5173`. Capture the row showing key `token` with its `eyJhbGciOi...` value. |
| **Slide 5** | **Cloud MongoDB Atlas & DB Watcher** | Open [cloud.mongodb.com](https://cloud.mongodb.com) showing cluster **`tms`**, or take a screenshot of your terminal running `npm run db:watch` showing live database connection. |
| **Slide 6** | **MongoDB Task Document & Indexes** | In MongoDB Atlas Collections (or Compass), capture a task document showing fields: `title`, `status`, `priority`, `dueDate`, `user` (ObjectId), and `timestamps`. |
| **Slide 7** | **My Tasks Grid & Add/Edit Modal** | Open `http://localhost:5173/tasks`. Click **➕ Add New Task** to open the modal dialog. Take a capture showing the task modal over the task cards. |
| **Slide 8** | **Filter Toolbar & Pagination** | On `http://localhost:5173/tasks`, select **Status: In Progress** and **Priority: High**. Take a screenshot showing the active filter dropdowns and bottom page buttons. |

---

## 🎙️ Exact Slide-by-Slide Speaking Script

### 🔵 SLIDE 1 & 2: Project Overview & Sequential Agenda (0:00 – 1:00)
- **Speaker:** Tejasvi starts.
- **Script:**
  > *"Good morning, Sir. Today we are presenting **TaskFlow**, a full-stack Task Management System built with the MERN stack—MongoDB Atlas, Express.js, React.js, and Node.js.  
  > 
  > To respect your time, our presentation is structured sequentially into two 5-minute segments:  
  > I will spend the first 5 minutes explaining our **Authentication Architecture, bcrypt Password Security, JWT Tokenization, and Cloud Database Integration**.  
  > Then Arpan will take over for the next 5 minutes to explain our **Task Schema, Database Compound Indexing, Full CRUD Operations, Multi-Parameter Filtering, and Server-Side Pagination**."*

---

### 🔵 SLIDE 3: User Registration & bcrypt Password Encryption (1:00 – 2:30)
- **Speaker:** Tejasvi
- **Script:**
  > *"Starting with user onboarding and security in `authController.js`:  
  > 1. We sanitize input using `name.trim()` and `email.trim().toLowerCase()` to avoid accidental whitespace errors or case-mismatched duplicate registrations.  
  > 2. Passwords are never stored in plain text. We use `bcrypt` with 10 salt rounds. A unique 10-round salt is generated and combined with the password before mathematical one-way hashing. This completely defends against rainbow-table attacks.  
  > 3. To prevent privilege tampering, our backend strictly hardcodes `role: 'User'` upon registration, ensuring no user can assign themselves Administrator privileges through API manipulation.  
  > 4. For login verification, `bcrypt.compare()` verifies the entered password against the stored hash cryptographically without ever needing to decrypt the hash."*

---

### 🔵 SLIDE 4: Stateless JWT Authorization & Route Guard (2:30 – 3:45)
- **Speaker:** Tejasvi
- **Script:**
  > *"Next is our session management and route protection:  
  > 1. Rather than maintaining heavy session tables in server memory, we use **JSON Web Tokens (JWT)** signed with `process.env.JWT_SECRET` and a 7-day expiration.  
  > 2. In `authMiddleware.js`, our `protect` middleware intercepts incoming HTTP requests, extracts `Bearer <token>` from the Authorization header, and verifies its cryptographic signature using `jwt.verify()`.  
  > 3. When querying MongoDB for user context, we explicitly use `.select('-password')`. This guarantees the password hash is never loaded into `req.user` memory or leaked in API responses.  
  > 4. On the frontend, our React component `ProtectedRoute.jsx` checks the token in `localStorage` and automatically blocks unauthenticated access to dashboard and task routes."*

---

### 🔵 SLIDE 5: Cloud Database Integration & Real-Time Monitoring (3:45 – 5:00)
- **Speaker:** Tejasvi
- **Script:**
  > *"Finally for my module, our cloud database infrastructure:  
  > 1. We migrated from local storage to **MongoDB Atlas Cloud** on a 3-node replica set cluster (`tms.l7vt8kf.mongodb.net` hosted in AWS Mumbai region).  
  > 2. In `config/db.js`, the connection string is completely environment-driven via `process.env.MONGO_URI`, making our application 100% cloud-ready.  
  > 3. We authored `seed.js` to initialize demo accounts and sample tasks with one command (`npm run seed`).  
  > 4. I also built a real-time database monitor tool (`npm run db:watch`) that streams live database modifications in colored terminal outputs whenever the frontend performs actions.  
  > 5. We configured `render.yaml` for 1-click cloud deployment on Render.  
  > 
  > Now I will hand over to Arpan to explain our core Task Management system."*

---

### 🟢 SLIDE 6: Task Model Schema Design & Compound Indexing (5:00 – 6:15)
- **Speaker:** Arpan Dey
- **Script:**
  > *"Thank you, Tejasvi. I will now present our **Task Management** module.  
  > 1. In `models/Task.js`, each task establishes referential integrity by storing `user: { type: ObjectId, ref: 'User', required: true }`. This links every task directly to its creator.  
  > 2. We enforce strict data types and schema enums for `status` (`Pending`, `In Progress`, `Completed`) and `priority` (`Low`, `Medium`, `High`), with automatic audit trails via `{ timestamps: true }`.  
  > 3. For performance optimization, we implemented **Compound Indexes** in MongoDB:  
  >    `taskSchema.index({ user: 1, status: 1 });`  
  >    `taskSchema.index({ user: 1, priority: 1 });`  
  > 4. In a real application with thousands of records, querying tasks by user and status without an index results in a slow full collection scan. Our compound indexes allow MongoDB to use a B-Tree index lookup, reducing query time from O(N) to O(log N)."*

---

### 🟢 SLIDE 7: Full Task CRUD Implementation & Ownership Isolation (6:15 – 7:30)
- **Speaker:** Arpan Dey
- **Script:**
  > *"Moving to our core CRUD API operations in `taskController.js`:  
  > 1. **CREATE (`POST /api/tasks`):** Validates the title, automatically associates `user: req.user._id` from the decoded JWT token, and saves the task with HTTP status 201.  
  > 2. **READ (`GET /api/tasks`):** Strictly enforces user isolation with `const query = { user: req.user._id };`. This guarantees User A can never inspect or retrieve User B's private tasks.  
  > 3. **UPDATE (`PUT /api/tasks/:id`):** Validates that the task ID is a valid 24-character hex ObjectId, checks ownership before applying updates, and allows both partial status updates and full title/due date edits.  
  > 4. **DELETE (`DELETE /api/tasks/:id`):** Verifies task ownership and removes the document using `task.deleteOne()`.  
  > 5. In React (`Tasks.jsx`), state updates trigger an instant re-render, so created, edited, or deleted tasks reflect immediately without refreshing the page."*

---

### 🟢 SLIDE 8: Multi-Parameter Filtering, Sorting & Pagination (7:30 – 8:45)
- **Speaker:** Arpan Dey
- **Script:**
  > *"To ensure usability when a user has dozens of tasks, I implemented advanced query handling:  
  > 1. **Multi-Parameter Filtering:** Users can filter by status and priority simultaneously (`GET /api/tasks?status=Pending&priority=High`). The backend dynamically builds the query object.  
  > 2. **Whitelisted Dynamic Sorting:** To prevent injection or sorting on invalid fields, we whitelist allowed sort keys (`dueDate`, `createdAt`, `title`) and apply dynamic order (`asc` / `desc`).  
  > 3. **Server-Side Pagination:** We avoid loading all documents into memory by calculating:  
  >    `skip = (pageNum - 1) * limitNum`  
  >    `totalPages = Math.ceil(totalTasks / limitNum)`  
  >    MongoDB's `.skip()` and `.limit()` fetch only the requested page slice, keeping page loads fast and responsive."*

---

### 🤝 SLIDE 9 & 10: Live Workflow Demo & Viva Conclusion (8:45 – 10:00)
- **Speaker:** Joint (Tejasvi & Arpan)
- **Script:**
  > **Arpan:** *"To conclude our presentation, here is the sequence of our live demonstration:  
  > Tejasvi will demonstrate user registration, JWT token storage, and route protection.  
  > Then I will demonstrate adding a task, applying status and priority filters, sorting by due date, editing a task, and deleting it.  
  > We will also show our live cloud MongoDB Atlas database updating in real time."*  
  > 
  > **Tejasvi:** *"Our complete source code, documentation, and cloud deployment blueprints are maintained on GitHub at `https://github.com/tejasvijain09/TaskFlow`.  
  > Thank you, Sir. We are now ready for your evaluation questions."*

---

## 🎯 Top 5 Questions the Examiner Will Ask & Quick Answers

1. **Teacher:** *"Why did you use JWT instead of express-session with cookies?"*  
   **Tejasvi:** *"JWT is stateless, meaning the server doesn't have to allocate memory or query a database session table on every single request. The token itself carries the cryptographically signed user ID, allowing the API to scale easily."*

2. **Teacher:** *"Why did you use compound indexing in Mongoose?"*  
   **Arpan:** *"Because our task queries filter by two fields at once—`user` and `status`. A compound index on `{ user: 1, status: 1 }` enables MongoDB to locate the exact slice in an indexed B-Tree in O(log N) time rather than scanning every document in the collection."*

3. **Teacher:** *"How do you prevent SQL/NoSQL injection in your task querying?"*  
   **Arpan:** *"In `taskController.js`, we do not blindly pass `req.query` into MongoDB. We explicitly map known fields (`status`, `priority`) and validate sort fields against an allowed whitelist array (`['createdAt', 'dueDate', 'title', 'priority', 'status']`)."*

4. **Teacher:** *"What does `select('-password')` do in your middleware?"*  
   **Tejasvi:** *"It tells Mongoose to exclude the hashed password field when querying the user document from MongoDB, ensuring the password hash is never attached to `req.user` in memory or returned in API responses."*

5. **Teacher:** *"Is this application connected to a local database or the cloud?"*  
   **Tejasvi:** *"It is connected directly to **MongoDB Atlas Cloud** on a 3-node replica set cluster hosted in AWS Mumbai (`tms.l7vt8kf.mongodb.net`), verified live via `process.env.MONGO_URI`."*
