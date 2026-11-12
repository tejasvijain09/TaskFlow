# TaskFlow — 10-Minute Presentation & Slide Deck Guide

**Course:** CSF402: Programming Node JS Applications  
**Evaluator / Faculty Supervisor:** Mr. Jitesh Kumar Bhatia  
**Project:** TaskFlow – Task Management System (MERN Stack)  

**Speakers & Presentation Structure:**
- **Tejasvi** (Reg No: 12315197) — *First 5 Minutes (Slides 1 to 5: Architecture, Security, Authentication & Cloud DB)*
- **Arpan Dey** (Reg No: 12305886) — *Next 5 Minutes (Slides 6 to 9: Task Engine, Indexing, CRUD & Filtering)*

> [!NOTE]
> The presentation slide deck (`TaskFlow_Presentation.pptx`) is designed as a **cohesive, professional team presentation**. It does **not** clutter the screen with internal speaker badges, names, or countdowns in front of your teacher and classmates.  
> The 5-minute split is maintained seamlessly through the speaking transitions below.

---

## 📂 Slide Deck File
The updated PowerPoint presentation is saved in your project root:  
📄 **[`TaskFlow_Presentation.pptx`](file:///Users/tejasvi/Documents/Projects/College%20Projects/TaskFlow/TaskFlow_Presentation.pptx)**  
*(Open in **Microsoft PowerPoint**, **Apple Keynote**, or drag into **Google Slides**).*

---

## ⏱️ Slide Overview & Sequence

| Slide | Topic | Presenter | Purpose |
| :---: | :--- | :---: | :--- |
| **Slide 1** | **TaskFlow Project Title & Team** | Tejasvi & Arpan | Project introduction, team details, supervisor info. |
| **Slide 2** | **System Architecture & Stack** | Tejasvi | 3-tier MERN stack overview (React, Express, Atlas). |
| **Slide 3** | **User Authentication & Security** | Tejasvi | Input sanitization, bcrypt 10-round hashing, role locks. |
| **Slide 4** | **JWT Authorization & Route Guarding** | Tejasvi | Stateless tokens, Bearer middleware, `ProtectedRoute`. |
| **Slide 5** | **Cloud Database & Live Sync** | Tejasvi | Atlas 3-node replica set, `process.env`, live DB watcher. |
| **Slide 6** | **Task Modeling & Compound Indexing** | Arpan Dey | Schema design, enums, $O(\log N)$ compound indexes. |
| **Slide 7** | **Task CRUD & Tenant Isolation** | Arpan Dey | Full CRUD endpoints, `user: req.user._id` data isolation. |
| **Slide 8** | **Filtering, Sorting & Pagination** | Arpan Dey | Dynamic multi-filters, whitelisted sorting, server-side `.skip()/.limit()`. |
| **Slide 9** | **Live Demonstration & Summary** | Both | 4-step live walkthrough sequence, GitHub repository, Q&A. |

---

## 📸 Proof-of-Work Screenshots Checklist

Each technical slide (Slides 3 to 8) contains a dedicated screenshot frame on the right side. Use `Cmd + Shift + 4` on macOS to capture and drop these in:

| Slide | Screenshot | Where to Capture |
| :---: | :--- | :--- |
| **Slide 3** | **Auth UI** | Open `http://localhost:5173/login` in your browser. Capture the Login / Register form card. |
| **Slide 4** | **JWT Token** | In browser, press `Cmd + Option + I` ➔ **Application** tab ➔ **Local Storage** ➔ `http://localhost:5173`. Capture the row with the `token` key. |
| **Slide 5** | **Cloud Atlas & Watcher** | Open [cloud.mongodb.com](https://cloud.mongodb.com) cluster **`tms`**, or take a screenshot of the terminal running `npm run db:watch`. |
| **Slide 6** | **Task Document Schema** | In MongoDB Atlas Collections, capture a task document showing fields: `title`, `status`, `priority`, `dueDate`, `user` (ObjectId). |
| **Slide 7** | **Tasks Grid & Modal** | Open `http://localhost:5173/tasks`. Click **➕ Add New Task** to open the modal dialog over the task cards. |
| **Slide 8** | **Filter Toolbar & Pagination** | On `http://localhost:5173/tasks`, select filters (`Status: In Progress`, `Priority: High`) showing the active dropdowns and bottom page buttons. |

---

## 🎙️ Natural Speaking Script (5 Min Tejasvi + 5 Min Arpan)

### 🔵 PART 1: TEJASVI (0:00 – 5:00)

#### Slide 1: Title Slide (0:00 – 0:45)
> *"Good morning, Sir. Today Arpan and I are presenting **TaskFlow**, our full-stack Task Management System developed for CSF402 using the MERN stack.  
> In our presentation, I will cover our core system architecture, authentication security, and cloud database infrastructure. Then Arpan will walk through our task data modeling, indexing, CRUD operations, and filtering engine."*

#### Slide 2: System Architecture & Stack (0:45 – 1:45)
> *"TaskFlow is architected across three distinct tiers:  
> 1. On the **Client Tier**, we use React 18 with Vite for a fast single-page application, featuring Axios interceptors for JWT transmission and Tailwind CSS for responsive styling.  
> 2. On the **Application Tier**, Node.js and Express manage RESTful endpoints, bcrypt hashing, JWT route protection, and automated Swagger API documentation.  
> 3. On the **Data Tier**, MongoDB Atlas Cloud manages structured document storage with Mongoose schema validation and compound indexing."*

#### Slide 3: User Authentication & Security (1:45 – 2:50)
> *"For user security in `authController.js`:  
> - We sanitize user inputs by trimming whitespace and normalizing email addresses to lowercase to prevent accidental duplicate accounts.  
> - For passwords, we never store plain text. We implement **bcrypt with 10 salt rounds**, combining a unique salt with the password before one-way mathematical hashing to defend against rainbow-table attacks.  
> - When registering, the backend strictly hardcodes the user role as `'User'` to prevent unauthorized role escalation to Administrator.  
> - On login, `bcrypt.compare()` verifies credentials against the stored cryptographic hash."*

#### Slide 4: JWT Authorization & Route Guarding (2:50 – 3:55)
> *"To maintain security across requests without heavy server-side session memory:  
> - We issue **JSON Web Tokens (JWT)** signed with our environment secret key and a 7-day expiration.  
> - Our custom `protect` middleware intercepts incoming HTTP requests, extracts the Bearer token from the Authorization header, and verifies its cryptographic signature.  
> - When retrieving the user context, we use `.select('-password')`, guaranteeing that password hashes are never kept in server memory or sent in API responses.  
> - On the client, React's `ProtectedRoute` component inspects `localStorage` and automatically redirects unauthorized users to the login screen."*

#### Slide 5: Cloud Database & Real-Time Sync (3:55 – 5:00)
> *"For persistent storage and cloud deployment:  
> - Rather than relying solely on a local database, TaskFlow connects directly to a **MongoDB Atlas Cloud** 3-node replica set cluster hosted in AWS Mumbai.  
> - Connection strings are entirely dynamic through `process.env.MONGO_URI`, ensuring safe configuration across local and cloud environments.  
> - To demonstrate live database interaction, I created a custom terminal monitor (`npm run db:watch`) that streams real-time database modifications as users interact with the app.  
> - We also prepared deployment blueprints for Render and Vercel.  
> Now, Arpan will present our task data engine and operations."*

---

### 🟢 PART 2: ARPAN DEY (5:00 – 10:00)

#### Slide 6: Task Data Modeling & Compound Indexing (5:00 – 6:15)
> *"Thank you, Tejasvi. I will now present our task data engine and user features.  
> - In `models/Task.js`, each task establishes referential integrity by storing `user: { type: ObjectId, ref: 'User', required: true }`. This links every task directly to its creator.  
> - We enforce strict schema enums for task status (`Pending`, `In Progress`, `Completed`) and priority (`Low`, `Medium`, `High`), with automatic audit trails via `{ timestamps: true }`.  
> - For database performance, we implemented **compound indexes** on `{ user: 1, status: 1 }` and `{ user: 1, priority: 1 }`.  
> - Because our application frequently filters tasks by user and status together, these indexes avoid costly full collection scans, reducing query execution from $O(N)$ to $O(\log N)$ via B-Tree index lookups."*

#### Slide 7: Task CRUD & Tenant Isolation (6:15 – 7:30)
> *"Our core task controller implements complete RESTful CRUD operations:  
> - **CREATE:** Validates task title and due date, associates the authenticated `user: req.user._id`, and returns HTTP status 201.  
> - **READ & ISOLATION:** Queries are strictly scoped to the logged-in user: `const query = { user: req.user._id }`. This guarantees strict tenant isolation—no user can view or tamper with another user's private data.  
> - **UPDATE & DELETE:** The controller verifies that the task ID is a valid 24-character hexadecimal ObjectId and confirms ownership before allowing edits or document removal.  
> - On the frontend, React state updates immediately so changes reflect dynamically without reloading the page."*

#### Slide 8: Filtering, Sorting & Server Pagination (7:30 – 8:45)
> *"To provide a clean user experience as task volume grows:  
> - **Multi-Parameter Filtering:** Users can filter by status and priority simultaneously (`GET /api/tasks?status=Pending&priority=High`).  
> - **Whitelisted Dynamic Sorting:** To prevent query injection, sort fields are checked against an allowed whitelist (`dueDate`, `createdAt`, `title`) with support for ascending and descending order.  
> - **Server-Side Pagination:** Instead of transferring all tasks across the network, MongoDB's `.skip()` and `.limit()` methods retrieve only the requested page slice, keeping response times fast and payloads lightweight."*

#### Slide 9: Live Demonstration & Q&A (8:45 – 10:00)
> *"To conclude our demonstration, here is the sequence of our live walkthrough:  
> 1. We will show user login and inspect the JWT token stored in the browser.  
> 2. We will create a task via our modal interface and update its status.  
> 3. We will filter tasks by status and priority and demonstrate pagination.  
> 4. We will show the live document updating immediately in MongoDB Atlas Cloud.  
> 
> Our complete source code is maintained on GitHub at `github.com/tejasvijain09/TaskFlow`.  
> Thank you, Sir. We are now ready for your questions."*

---

## 🎯 Top 5 Viva Questions & Fast Answers

1. **"Why use bcrypt with 10 salt rounds?"**  
   *Answer:* Bcrypt generates a random cryptographic salt for each password and runs $2^{10}$ hashing iterations. This makes brute-force and rainbow-table dictionary attacks mathematically infeasible.

2. **"What is the advantage of compound indexes in MongoDB?"**  
   *Answer:* A compound index on `{ user: 1, status: 1 }` allows MongoDB to evaluate both the user ownership and status filter in a single indexed B-Tree traversal in $O(\log N)$ time, avoiding an expensive scan of all documents in the collection.

3. **"Why use JWT instead of traditional session cookies?"**  
   *Answer:* JWT is stateless. The user's identity is digitally signed inside the token, so the backend server doesn't need to maintain or query an in-memory session store on every request, making it lightweight and horizontally scalable.

4. **"How do you ensure one user cannot delete another user's task?"**  
   *Answer:* In `taskController.js`, before deleting, the backend fetches the task and checks `if (task.user.toString() !== req.user._id.toString())`. If they don't match, the server rejects the request with HTTP status 403 Forbidden.

5. **"Why is pagination done on the server instead of the client?"**  
   *Answer:* Client-side pagination would require downloading thousands of records over the network on every load. Server-side pagination with `.skip()` and `.limit()` transfers only the exact 6 or 10 tasks needed for the active page, saving bandwidth and memory.
