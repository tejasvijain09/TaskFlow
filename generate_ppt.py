import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen slides
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Theme Colors
    PRIMARY = RGBColor(79, 70, 229)     # Indigo / Purple #4f46e5
    DARK_TEXT = RGBColor(15, 23, 42)    # Dark Slate #0f172a
    MUTED_TEXT = RGBColor(100, 116, 139)# Slate Gray #64748b
    LIGHT_BG = RGBColor(248, 250, 252)  # Light #f8fafc
    WHITE = RGBColor(255, 255, 255)
    ACCENT_TEJASVI = RGBColor(37, 99, 235)  # Blue #2563eb
    ACCENT_ARPAN = RGBColor(16, 185, 129)   # Emerald #10b981
    BORDER_COLOR = RGBColor(226, 232, 240)  # Border #e2e8f0

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text, presenter_tag=None, tag_color=PRIMARY):
        # Header category / module tracker
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = PRIMARY

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(9.5), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = DARK_TEXT

        # Presenter Badge on top right
        if presenter_tag:
            tag_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.5), Inches(0.55), Inches(2.0), Inches(0.5))
            tag_box.fill.solid()
            tag_box.fill.fore_color.rgb = tag_color
            tag_box.line.color.rgb = tag_color
            tf_tag = tag_box.text_frame
            p_tag = tf_tag.paragraphs[0]
            p_tag.text = presenter_tag
            p_tag.font.size = Pt(12)
            p_tag.font.bold = True
            p_tag.font.color.rgb = WHITE
            p_tag.alignment = PP_ALIGN.CENTER

    def add_card(slide, left, top, width, height, bg_color=WHITE, border_color=BORDER_COLOR):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
        return shape

    def add_screenshot_frame(slide, left, top, width, height, title, instruction):
        # Box container for screenshot
        frame = add_card(slide, left, top, width, height, bg_color=LIGHT_BG, border_color=PRIMARY)
        
        # Inner text instructing which screenshot to paste
        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.3), width - Inches(0.4), height - Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        p1.text = f"📸 SCREENSHOT PROOF:"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = PRIMARY
        p1.alignment = PP_ALIGN.CENTER

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.size = Pt(14)
        p2.font.bold = True
        p2.font.color.rgb = DARK_TEXT
        p2.alignment = PP_ALIGN.CENTER

        p3 = tf.add_paragraph()
        p3.text = f"\n{instruction}"
        p3.font.size = Pt(11)
        p3.font.color.rgb = MUTED_TEXT
        p3.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = LIGHT_BG
    bg1.line.fill.background()

    # Title card container
    add_card(slide1, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5), bg_color=WHITE)

    # App Tag
    t_box = slide1.shapes.add_textbox(Inches(1.6), Inches(1.3), Inches(10.1), Inches(0.5))
    tf1 = t_box.text_frame
    p = tf1.paragraphs[0]
    p.text = "ACADEMIC PROJECT DEMONSTRATION • CSF402"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    # Main Project Title
    t_box2 = slide1.shapes.add_textbox(Inches(1.6), Inches(1.7), Inches(10.1), Inches(1.1))
    tf2 = t_box2.text_frame
    p = tf2.paragraphs[0]
    p.text = "TaskFlow — Task Management System"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT

    # Subtitle
    t_box3 = slide1.shapes.add_textbox(Inches(1.6), Inches(2.7), Inches(10.1), Inches(0.6))
    tf3 = t_box3.text_frame
    p = tf3.paragraphs[0]
    p.text = "Full-Stack Web Application built on MERN (MongoDB Atlas, Express.js, React.js, Node.js)"
    p.font.size = Pt(15)
    p.font.color.rgb = MUTED_TEXT

    # Evaluator Information
    t_box4 = slide1.shapes.add_textbox(Inches(1.6), Inches(3.4), Inches(10.1), Inches(0.6))
    tf4 = t_box4.text_frame
    p = tf4.paragraphs[0]
    p.text = "Faculty Evaluator: Mr. Jitesh Kumar Bhatia | School of Computer Science & Engineering"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT

    # 2 Presenter Cards
    # Card A: Tejasvi
    c_tej = add_card(slide1, Inches(1.6), Inches(4.3), Inches(4.8), Inches(1.7), bg_color=WHITE, border_color=ACCENT_TEJASVI)
    tb_tej = slide1.shapes.add_textbox(Inches(1.8), Inches(4.45), Inches(4.4), Inches(1.4))
    tf_tej = tb_tej.text_frame
    p = tf_tej.paragraphs[0]
    p.text = "👤 TEJASVI (Reg No: 12315197)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_TEJASVI
    p2 = tf_tej.add_paragraph()
    p2.text = "Module 1: Authentication, Password Hashing,\nJWT Authorization & Cloud Atlas Integration\n⏱️ Speaking Time: First 5 Minutes"
    p2.font.size = Pt(11)
    p2.font.color.rgb = MUTED_TEXT

    # Card B: Arpan Dey
    c_arp = add_card(slide1, Inches(6.8), Inches(4.3), Inches(4.8), Inches(1.7), bg_color=WHITE, border_color=ACCENT_ARPAN)
    tb_arp = slide1.shapes.add_textbox(Inches(7.0), Inches(4.45), Inches(4.4), Inches(1.4))
    tf_arp = tb_arp.text_frame
    p = tf_arp.paragraphs[0]
    p.text = "👤 ARPAN DEY (Reg No: 12305886)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ARPAN
    p2 = tf_arp.add_paragraph()
    p2.text = "Module 2: Task Schema, Full CRUD Operations,\nFilters, Multi-Field Sorting & Pagination\n⏱️ Speaking Time: Next 5 Minutes"
    p2.font.size = Pt(11)
    p2.font.color.rgb = MUTED_TEXT

    # =========================================================================
    # SLIDE 2: Sequential Agenda & System Architecture
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Sequential Presentation Agenda & System Architecture", "Project Overview", "10 Minutes Total")

    # Left Container: Tejasvi's 5-Minute Agenda
    add_card(slide2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3), bg_color=WHITE, border_color=ACCENT_TEJASVI)
    tb_a1 = slide2.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(5.0), Inches(4.8))
    tfa1 = tb_a1.text_frame
    tfa1.word_wrap = True
    p = tfa1.paragraphs[0]
    p.text = "PART 1: TEJASVI (First 5 Minutes)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_TEJASVI

    items_tej = [
        ("1. User Security & Registration:", "Input validation, email normalization, prevention of role escalation to Admin."),
        ("2. Password Hashing (bcrypt):", "10-round salt hashing to ensure passwords are never stored in plain text."),
        ("3. Stateless JWT Tokenization:", "Signing verifiable tokens (7-day validity) on login."),
        ("4. Request Middleware (`protect`):", "Extracting Bearer tokens, decoding payload, attaching user context."),
        ("5. Live Cloud Deployment:", "MongoDB Atlas Cloud replica set & Render/Vercel architecture.")
    ]
    for title, desc in items_tej:
        p_t = tfa1.add_paragraph()
        p_t.text = f"• {title} "
        p_t.font.bold = True
        p_t.font.size = Pt(12)
        p_t.font.color.rgb = DARK_TEXT
        p_d = tfa1.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = MUTED_TEXT

    # Right Container: Arpan's 5-Minute Agenda
    add_card(slide2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3), bg_color=WHITE, border_color=ACCENT_ARPAN)
    tb_a2 = slide2.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.1), Inches(4.8))
    tfa2 = tb_a2.text_frame
    tfa2.word_wrap = True
    p = tfa2.paragraphs[0]
    p.text = "PART 2: ARPAN DEY (Next 5 Minutes)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ARPAN

    items_arp = [
        ("1. Task Schema & Relationship:", "Mongoose model referencing User via `ref: 'User'` with timestamps."),
        ("2. Database Performance Indexing:", "Compound indexes (`user+status`, `user+priority`) for O(log N) queries."),
        ("3. Complete Task CRUD Implementation:", "Create, Read, Update, Delete with ownership isolation (`query.user = req.user._id`)."),
        ("4. Advanced Query Parameters:", "URL status filtering, priority filtering, and dynamic sort criteria."),
        ("5. Server-Side Pagination:", "Math-backed pagination using `skip()` and `limit()` methods in MongoDB.")
    ]
    for title, desc in items_arp:
        p_t = tfa2.add_paragraph()
        p_t.text = f"• {title} "
        p_t.font.bold = True
        p_t.font.size = Pt(12)
        p_t.font.color.rgb = DARK_TEXT
        p_d = tfa2.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = MUTED_TEXT

    # =========================================================================
    # SLIDE 3: Tejasvi - Authentication & Password Hashing
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "User Registration & bcrypt Password Encryption", "Tejasvi's Module • Core Security", "Tejasvi (5 Min)", ACCENT_TEJASVI)

    # Left Column: Explanation & Code Highlights
    add_card(slide3, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.3))
    tb_s3 = slide3.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.6), Inches(4.8))
    tf_s3 = tb_s3.text_frame
    tf_s3.word_wrap = True
    p = tf_s3.paragraphs[0]
    p.text = "Key Engineering Contributions (authController.js):"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT

    points_s3 = [
        ("Sanitized Input Validation:", "Enforces `name.trim()` and `email.trim().toLowerCase()` to prevent whitespace accounts or case-mismatched duplicate entries."),
        ("bcrypt Salt Hashing (10 Rounds):", "Passwords are never stored in plain text. A 10-round random salt prevents rainbow table decryption:"),
        ("   const salt = await bcrypt.genSalt(10);", "code"),
        ("   const hashedPassword = await bcrypt.hash(password, salt);", "code"),
        ("Strict Role Control (Anti-Tampering):", "Hardcodes `role: 'User'` in `User.create()`, preventing attackers from registering themselves as Administrators via API payload manipulation."),
        ("Verified Login Validation:", "`bcrypt.compare(password, user.password)` cryptographically checks credentials without ever needing to decrypt the stored hash.")
    ]
    for item, itype in points_s3:
        p = tf_s3.add_paragraph()
        if itype == "code":
            p.text = item
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = PRIMARY
        else:
            p.text = f"• {item} "
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = DARK_TEXT
            p2 = tf_s3.add_paragraph()
            p2.text = f"  {itype}"
            p2.font.size = Pt(10)
            p2.font.color.rgb = MUTED_TEXT

    # Right Column: Screenshot Placeholder
    add_screenshot_frame(slide3, Inches(7.1), Inches(1.6), Inches(5.4), Inches(5.3),
                         "User Registration & Login Interface",
                         "Paste screenshot of:\n1. The clean Login / Register UI (Login.jsx)\n2. Form validation showing password requirement\n3. MongoDB document showing password saved as '$2a$10$...'")

    # =========================================================================
    # SLIDE 4: Tejasvi - JWT Tokens & Middleware Pipeline
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Stateless JWT Authorization & Protected Route Guard", "Tejasvi's Module • Access Control", "Tejasvi (5 Min)", ACCENT_TEJASVI)

    # Left Column: Explanation
    add_card(slide4, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.3))
    tb_s4 = slide4.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.6), Inches(4.8))
    tf_s4 = tb_s4.text_frame
    tf_s4.word_wrap = True
    p = tf_s4.paragraphs[0]
    p.text = "JWT Lifecycle & Middleware Architecture:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT

    points_s4 = [
        ("Stateless Token Issuance:", "Upon valid login, backend issues signed JWT token containing user's unique `_id` with 7-day expiration."),
        ("   jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: '7d' })", "code"),
        ("Auth Verification Middleware (`authMiddleware.js`):", "Extracts `Bearer <token>` from HTTP request headers, verifies signature, and attaches user to `req.user`:"),
        ("   const decoded = jwt.verify(token, process.env.JWT_SECRET);", "code"),
        ("   req.user = await User.findById(decoded.id).select('-password');", "code"),
        ("Data Leak Prevention (`select('-password')`):", "Explicitly excludes password hash so sensitive credentials are never stored in `req.user` memory or sent in API responses."),
        ("Client-Side Route Guard (`ProtectedRoute.jsx`):", "React Router wrapper checking `localStorage.getItem('token')`. Redirects unauthenticated visitors to `/login`.")
    ]
    for item, itype in points_s4:
        p = tf_s4.add_paragraph()
        if itype == "code":
            p.text = item
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = PRIMARY
        else:
            p.text = f"• {item} "
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = DARK_TEXT
            p2 = tf_s4.add_paragraph()
            p2.text = f"  {itype}"
            p2.font.size = Pt(10)
            p2.font.color.rgb = MUTED_TEXT

    # Right Column: Screenshot Placeholder
    add_screenshot_frame(slide4, Inches(7.1), Inches(1.6), Inches(5.4), Inches(5.3),
                         "JWT Storage & Network Inspector Proof",
                         "Paste screenshot of:\n1. Chrome DevTools -> Application -> Local Storage showing stored 'token' (eyJhbGci...)\n2. Network tab showing 'Authorization: Bearer <token>' header on /api/tasks requests")

    # =========================================================================
    # SLIDE 5: Tejasvi - Live Cloud Database & Monitoring
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Cloud Database Integration & Live Real-Time Monitor", "Tejasvi's Module • Cloud Infrastructure", "Tejasvi (5 Min)", ACCENT_TEJASVI)

    # Left Column
    add_card(slide5, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.3))
    tb_s5 = slide5.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.6), Inches(4.8))
    tf_s5 = tb_s5.text_frame
    tf_s5.word_wrap = True
    p = tf_s5.paragraphs[0]
    p.text = "Cloud Infrastructure & Real-Time Tooling:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT

    points_s5 = [
        ("MongoDB Atlas Cloud Sharding:", "Configured cluster `tms` on AWS Mumbai region (`tms.l7vt8kf.mongodb.net`). Replaced local storage with a 3-node replica set."),
        ("Environment-Driven Connection (`db.js`):", "Zero hardcoded URLs. Mongoose reads `process.env.MONGO_URI` dynamically, enabling seamless deployment across local and cloud targets."),
        ("Automated Database Seeder (`seed.js`):", "One-command database initialization (`npm run seed`) creating hashed Administrator and demo accounts with verified sample tasks."),
        ("Live Real-Time Database Monitor (`db_monitor.js`):", "Engineered custom terminal monitor (`npm run db:watch`) that streams live database modifications with colored JSON outputs whenever frontend makes CRUD requests."),
        ("Production Blueprint (`render.yaml`):", "Authored declarative blueprint for 1-click cloud backend deployment with pre-configured environment bindings.")
    ]
    for item, desc in points_s5:
        p = tf_s5.add_paragraph()
        p.text = f"• {item} "
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = DARK_TEXT
        p2 = tf_s5.add_paragraph()
        p2.text = f"  {desc}"
        p2.font.size = Pt(10)
        p2.font.color.rgb = MUTED_TEXT

    # Right Column: Screenshot Placeholder
    add_screenshot_frame(slide5, Inches(7.1), Inches(1.6), Inches(5.4), Inches(5.3),
                         "Live Cloud MongoDB Atlas & Real-time Watcher",
                         "Paste screenshot of:\n1. MongoDB Atlas Dashboard showing Cluster 'tms' & 'taskflow' database collections\n2. Terminal running 'npm run db:watch' showing real-time document modifications")

    # =========================================================================
    # SLIDE 6: Arpan Dey - Task Schema & Database Indexing
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Task Model Schema Design & Compound Indexing", "Arpan's Module • Database Architecture", "Arpan Dey (5 Min)", ACCENT_ARPAN)

    # Left Column
    add_card(slide6, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.3))
    tb_s6 = slide6.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.6), Inches(4.8))
    tf_s6 = tb_s6.text_frame
    tf_s6.word_wrap = True
    p = tf_s6.paragraphs[0]
    p.text = "Mongoose Data Modeling (Task.js):"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT

    points_s6 = [
        ("Relational Modeling via ObjectId:", "Each task references its creator via `user: { type: ObjectId, ref: 'User', required: true }`, establishing referential integrity in MongoDB."),
        ("Strict Schema Enums:", "Guarantees data consistency by constraining status (`Pending`, `In Progress`, `Completed`) and priority (`Low`, `Medium`, `High`)."),
        ("Automatic Timestamps:", "Enabled `{ timestamps: true }` to automatically track `createdAt` and `updatedAt` audit trails for every record."),
        ("Performance-Critical Compound Indexing:", "Added database indexes to eliminate costly full collection scans (COLLSCAN) during user queries:"),
        ("   taskSchema.index({ user: 1, status: 1 });", "code"),
        ("   taskSchema.index({ user: 1, priority: 1 });", "code"),
        ("   taskSchema.index({ user: 1, dueDate: 1 });", "code"),
        ("Viva Point:", "Queries filter by user AND status simultaneously. The compound index reduces lookup time from O(N) to O(log N) in B-Tree index structures.")
    ]
    for item, itype in points_s6:
        p = tf_s6.add_paragraph()
        if itype == "code":
            p.text = item
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = PRIMARY
        else:
            p.text = f"• {item} "
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = DARK_TEXT
            p2 = tf_s6.add_paragraph()
            p2.text = f"  {itype}"
            p2.font.size = Pt(10)
            p2.font.color.rgb = MUTED_TEXT

    # Right Column: Screenshot Placeholder
    add_screenshot_frame(slide6, Inches(7.1), Inches(1.6), Inches(5.4), Inches(5.3),
                         "Mongoose Task Schema & MongoDB Document",
                         "Paste screenshot of:\n1. MongoDB Compass / Atlas showing 'tasks' collection document structure\n2. Indexes tab in Atlas showing compound indexes { user: 1, status: 1 }")

    # =========================================================================
    # SLIDE 7: Arpan Dey - Task CRUD Operations
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Full Task CRUD Implementation & Ownership Isolation", "Arpan's Module • Core Business Logic", "Arpan Dey (5 Min)", ACCENT_ARPAN)

    # Left Column
    add_card(slide7, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.3))
    tb_s7 = slide7.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.6), Inches(4.8))
    tf_s7 = tb_s7.text_frame
    tf_s7.word_wrap = True
    p = tf_s7.paragraphs[0]
    p.text = "Complete CRUD Operations (taskController.js):"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT

    points_s7 = [
        ("CREATE (`POST /api/tasks`):", "Extracts title, description, priority, due date. Assigns authenticated `user: req.user._id` and saves via `Task.create()` (HTTP 201)."),
        ("READ (`GET /api/tasks`):", "Strictly isolates queries to the logged-in user: `const query = { user: req.user._id };`. Prevents unauthorized cross-tenant data leaks."),
        ("UPDATE (`PUT /api/tasks/:id`):", "Validates ObjectId format and verifies ownership before saving changes:"),
        ("   if (task.user.toString() !== req.user._id.toString() && req.user.role !== 'Admin')", "code"),
        ("   return res.status(403).json({ message: 'Not authorized' });", "code"),
        ("DELETE (`DELETE /api/tasks/:id`):", "Ensures only task owner (or Admin) can delete. Calls `await task.deleteOne()` and returns HTTP 200 with deleted ID confirmation."),
        ("Frontend State Sync:", "`Tasks.jsx` immediately re-invokes `fetchTasks()` to refresh UI dynamically without requiring full browser reload.")
    ]
    for item, itype in points_s7:
        p = tf_s7.add_paragraph()
        if itype == "code":
            p.text = item
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = PRIMARY
        else:
            p.text = f"• {item} "
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = DARK_TEXT
            p2 = tf_s7.add_paragraph()
            p2.text = f"  {itype}"
            p2.font.size = Pt(10)
            p2.font.color.rgb = MUTED_TEXT

    # Right Column: Screenshot Placeholder
    add_screenshot_frame(slide7, Inches(7.1), Inches(1.6), Inches(5.4), Inches(5.3),
                         "Live Task Card Grid & Edit Modal Dialog",
                         "Paste screenshot of:\n1. My Tasks view showing task cards with color-coded status and priority badges\n2. Add / Edit Task Modal Form with title, priority dropdown, and due date")

    # =========================================================================
    # SLIDE 8: Arpan Dey - Filtering, Sorting & Pagination
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Multi-Parameter Filtering, Dynamic Sorting & Pagination", "Arpan's Module • Advanced Querying", "Arpan Dey (5 Min)", ACCENT_ARPAN)

    # Left Column
    add_card(slide8, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.3))
    tb_s8 = slide8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.6), Inches(4.8))
    tf_s8 = tb_s8.text_frame
    tf_s8.word_wrap = True
    p = tf_s8.paragraphs[0]
    p.text = "Query Parameter Architecture:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT

    points_s8 = [
        ("Multi-Parameter Filtering:", "Supports status and priority filters simultaneously: `GET /api/tasks?status=Pending&priority=High`."),
        ("   if (status && status !== 'All') query.status = status;", "code"),
        ("   if (priority && priority !== 'All') query.priority = priority;", "code"),
        ("Whitelisted Dynamic Sorting:", "Prevents malicious query keys by checking allowed sort fields (`dueDate`, `createdAt`, `title`):"),
        ("   const sortOrder = order === 'asc' ? 1 : -1;", "code"),
        ("   const sortCriteria = { [sortField]: sortOrder };", "code"),
        ("Server-Side Pagination Math:", "Uses MongoDB `skip()` and `limit()` to avoid returning thousands of records at once:"),
        ("   const skip = (pageNum - 1) * limitNum;", "code"),
        ("   const totalPages = Math.ceil(totalTasks / limitNum) || 1;", "code"),
        ("Return Payload:", "Returns `{ tasks, currentPage, totalPages, totalTasks }` to render responsive pagination buttons.")
    ]
    for item, itype in points_s8:
        p = tf_s8.add_paragraph()
        if itype == "code":
            p.text = item
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = PRIMARY
        else:
            p.text = f"• {item} "
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = DARK_TEXT
            p2 = tf_s8.add_paragraph()
            p2.text = f"  {itype}"
            p2.font.size = Pt(10)
            p2.font.color.rgb = MUTED_TEXT

    # Right Column: Screenshot Placeholder
    add_screenshot_frame(slide8, Inches(7.1), Inches(1.6), Inches(5.4), Inches(5.3),
                         "Filter Toolbar & Pagination Controls",
                         "Paste screenshot of:\n1. The Filter & Sort Toolbar showing dropdowns: Status, Priority, Sort By, and Order\n2. Numbered pagination buttons at the bottom showing active page")

    # =========================================================================
    # SLIDE 9: Live Demonstration Sequence
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "Sequential Live Demonstration Execution Plan", "Step-by-Step Script", "Joint Demo (Both)")

    # Left Column: Tejasvi's Live Demo Steps
    add_card(slide9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3), bg_color=WHITE, border_color=ACCENT_TEJASVI)
    tb_d1 = slide9.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(5.0), Inches(4.8))
    tfd1 = tb_d1.text_frame
    tfd1.word_wrap = True
    p = tfd1.paragraphs[0]
    p.text = "TEJASVI'S LIVE DEMO (Minutes 1 - 5)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_TEJASVI

    demo_steps_tej = [
        ("Step 1: User Registration", "Open `/register`, demonstrate client password mismatch validation, then submit valid registration."),
        ("Step 2: Inspect JWT Token", "Open Chrome DevTools (F12) -> Application -> Local Storage. Point out stored `token` and `user` object."),
        ("Step 3: Route Protection Guard", "Attempt navigating to `/admin` as normal user; show `ProtectedRoute` redirecting back to `/dashboard`."),
        ("Step 4: Cloud MongoDB Atlas Proof", "Open MongoDB Atlas web dashboard (`tms` cluster) showing the newly created user document."),
        ("Step 5: Handover to Arpan", "Explain architectural integration and hand over to Arpan for task CRUD demo.")
    ]
    for step, desc in demo_steps_tej:
        p = tfd1.add_paragraph()
        p.text = f"👉 {step}: "
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = DARK_TEXT
        p2 = tfd1.add_paragraph()
        p2.text = f"   {desc}"
        p2.font.size = Pt(10)
        p2.font.color.rgb = MUTED_TEXT

    # Right Column: Arpan's Live Demo Steps
    add_card(slide9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3), bg_color=WHITE, border_color=ACCENT_ARPAN)
    tb_d2 = slide9.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.1), Inches(4.8))
    tfd2 = tb_d2.text_frame
    tfd2.word_wrap = True
    p = tfd2.paragraphs[0]
    p.text = "ARPAN'S LIVE DEMO (Minutes 6 - 10)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ARPAN

    demo_steps_arp = [
        ("Step 1: CREATE Task", "Navigate to `/tasks`, open modal, fill title & High priority, and submit. Show card appearing instantly."),
        ("Step 2: READ & Multi-Filter", "Filter by `Status: In Progress` and `Priority: High` to prove compound server-side querying."),
        ("Step 3: Dynamic Sorting", "Sort by `Due Date (Ascending)` and cycle through pages to demonstrate server-side pagination."),
        ("Step 4: UPDATE Task Details", "Use card dropdown to switch status to `Completed`; edit title via modal dialog."),
        ("Step 5: DELETE Task", "Click delete, confirm alert, and show instant removal from database."),
        ("Step 6: Live DB Watcher Sync", "Show terminal running `npm run db:watch` reflecting live updates in real time.")
    ]
    for step, desc in demo_steps_arp:
        p = tfd2.add_paragraph()
        p.text = f"👉 {step}: "
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = DARK_TEXT
        p2 = tfd2.add_paragraph()
        p2.text = f"   {desc}"
        p2.font.size = Pt(10)
        p2.font.color.rgb = MUTED_TEXT

    # =========================================================================
    # SLIDE 10: Conclusion & Technical Highlights
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "Summary of Technical Achievements & Viva Q&A", "Evaluation Conclusion", "Ready for Q&A")

    # 3 Summary Cards
    # Card 1: Tejasvi
    add_card(slide10, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.0), bg_color=WHITE, border_color=ACCENT_TEJASVI)
    tb_c1 = slide10.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(3.3), Inches(4.5))
    tfc1 = tb_c1.text_frame
    tfc1.word_wrap = True
    p = tfc1.paragraphs[0]
    p.text = "Tejasvi's Deliverables"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_TEJASVI
    pts_c1 = [
        "✓ Input Sanitization & Duplicate Email Check",
        "✓ 10-round bcrypt Salt Password Hashing",
        "✓ 7-day Stateless JWT Token Issuance",
        "✓ `authMiddleware` with Token Verification",
        "✓ Client-side `ProtectedRoute` Guard",
        "✓ MongoDB Atlas Cloud Replica Set Integration",
        "✓ Live Terminal Database Monitor Tool"
    ]
    for pt in pts_c1:
        p = tfc1.add_paragraph()
        p.text = pt
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT

    # Card 2: Arpan
    add_card(slide10, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.0), bg_color=WHITE, border_color=ACCENT_ARPAN)
    tb_c2 = slide10.shapes.add_textbox(Inches(5.0), Inches(1.8), Inches(3.3), Inches(4.5))
    tfc2 = tb_c2.text_frame
    tfc2.word_wrap = True
    p = tfc2.paragraphs[0]
    p.text = "Arpan's Deliverables"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ARPAN
    pts_c2 = [
        "✓ Normalized Mongoose Task Schema",
        "✓ Compound Indexes on user+status, user+priority",
        "✓ Full CRUD APIs (Create, Read, Update, Delete)",
        "✓ Strict User Ownership Isolation (`req.user._id`)",
        "✓ Multi-parameter URL Filtering",
        "✓ Whitelisted Dynamic Multi-field Sorting",
        "✓ Math-backed Server-side Pagination"
    ]
    for pt in pts_c2:
        p = tfc2.add_paragraph()
        p.text = pt
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT

    # Card 3: Project Architecture
    add_card(slide10, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.0), bg_color=WHITE, border_color=PRIMARY)
    tb_c3 = slide10.shapes.add_textbox(Inches(9.0), Inches(1.8), Inches(3.3), Inches(4.5))
    tfc3 = tb_c3.text_frame
    tfc3.word_wrap = True
    p = tfc3.paragraphs[0]
    p.text = "System Excellence"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    pts_c3 = [
        "✓ 100% Working MERN Request-Response Cycle",
        "✓ Clean React 18 Functional Architecture",
        "✓ Zero Heavy Over-engineered Libraries",
        "✓ Cloud MongoDB Atlas Database Active",
        "✓ Public GitHub Repository with Complete Documentation",
        "✓ Comprehensive 45-question Viva Guide",
        "\n🎓 Thank You! We are ready for your evaluation questions, Sir."
    ]
    for pt in pts_c3:
        p = tfc3.add_paragraph()
        p.text = pt
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT

    # Save presentation
    output_path = "/Users/tejasvi/Documents/Projects/College Projects/TaskFlow/TaskFlow_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_presentation()
