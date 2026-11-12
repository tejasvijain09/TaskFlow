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

    # Professional Modern Palette (Clean Slate & Vibrant Indigo Theme)
    BG_CANVAS = RGBColor(248, 250, 252)     # #f8fafc Soft off-white
    PRIMARY = RGBColor(79, 70, 229)         # #4f46e5 Modern Indigo
    DARK_TEXT = RGBColor(15, 23, 42)        # #0f172a Deep Slate
    BODY_TEXT = RGBColor(51, 65, 85)        # #334155 Slate
    MUTED_TEXT = RGBColor(100, 116, 139)    # #64748b Neutral Gray
    WHITE = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(226, 232, 240)   # #e2e8f0
    ACCENT_LINE = RGBColor(99, 102, 241)    # #6366f1
    FRAME_BG = RGBColor(241, 245, 249)      # #f1f5f9
    FRAME_BORDER = RGBColor(203, 213, 225)  # #cbd5e1

    blank_layout = prs.slide_layouts[6]

    def set_canvas_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_CANVAS
        bg.line.fill.background()
        return bg

    def add_card(slide, left, top, width, height, bg_color=WHITE, border_color=CARD_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
        return shape

    def add_header(slide, title_text, category_text=None):
        # Header box
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.95))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        if category_text:
            p_cat = tf.paragraphs[0]
            p_cat.text = category_text.upper()
            p_cat.font.size = Pt(11)
            p_cat.font.bold = True
            p_cat.font.color.rgb = PRIMARY
            p_cat.space_after = Pt(4)

            p_title = tf.add_paragraph()
        else:
            p_title = tf.paragraphs[0]

        p_title.text = title_text
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = DARK_TEXT

    def add_screenshot_frame(slide, left, top, width, height, label_title, tip_text):
        # Card container for screenshot
        add_card(slide, left, top, width, height, bg_color=FRAME_BG, border_color=FRAME_BORDER)

        tb = slide.shapes.add_textbox(left + Inches(0.4), top + Inches(1.2), width - Inches(0.8), height - Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = "PROOF OF WORK"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = PRIMARY
        p1.alignment = PP_ALIGN.CENTER
        p1.space_after = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = label_title
        p2.font.size = Pt(16)
        p2.font.bold = True
        p2.font.color.rgb = DARK_TEXT
        p2.alignment = PP_ALIGN.CENTER
        p2.space_after = Pt(12)

        p3 = tf.add_paragraph()
        p3.text = tip_text
        p3.font.size = Pt(12)
        p3.font.color.rgb = MUTED_TEXT
        p3.alignment = PP_ALIGN.CENTER

    def add_bullet_list(tf, items):
        for i, (heading, detail) in enumerate(items):
            p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
            p.space_after = Pt(14)
            p.line_spacing = 1.25

            # Bold Heading
            run_h = p.add_run()
            run_h.text = f"•  {heading}: "
            run_h.font.bold = True
            run_h.font.size = Pt(14)
            run_h.font.color.rgb = DARK_TEXT

            # Crisp detail
            run_d = p.add_run()
            run_d.text = detail
            run_d.font.bold = False
            run_d.font.size = Pt(13)
            run_d.font.color.rgb = BODY_TEXT

    # =========================================================================
    # SLIDE 1: Title Slide (Clean, Academic, Professional)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s1)

    # Main Card
    add_card(s1, Inches(1.0), Inches(0.9), Inches(11.333), Inches(5.7), bg_color=WHITE)

    # Top Tag
    tb1_tag = s1.shapes.add_textbox(Inches(1.5), Inches(1.3), Inches(10.3), Inches(0.4))
    tf1_tag = tb1_tag.text_frame
    p = tf1_tag.paragraphs[0]
    p.text = "ACADEMIC PROJECT DEMONSTRATION  •  CSF402"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    # Title
    tb1_title = s1.shapes.add_textbox(Inches(1.5), Inches(1.75), Inches(10.3), Inches(1.1))
    tf1_title = tb1_title.text_frame
    p = tf1_title.paragraphs[0]
    p.text = "TaskFlow"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT

    # Subtitle
    tb1_sub = s1.shapes.add_textbox(Inches(1.5), Inches(2.7), Inches(10.3), Inches(0.6))
    tf1_sub = tb1_sub.text_frame
    p = tf1_sub.paragraphs[0]
    p.text = "A Full-Stack Task Management System built with the MERN Stack"
    p.font.size = Pt(16)
    p.font.color.rgb = MUTED_TEXT

    # Evaluator Info
    tb1_eval = s1.shapes.add_textbox(Inches(1.5), Inches(3.35), Inches(10.3), Inches(0.5))
    tf1_eval = tb1_eval.text_frame
    p = tf1_eval.paragraphs[0]
    p.text = "Faculty Evaluator: Mr. Jitesh Kumar Bhatia"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT

    # Divider Line
    line1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.5), Inches(3.9), Inches(10.3), Inches(0.02))
    line1.fill.solid()
    line1.fill.fore_color.rgb = CARD_BORDER
    line1.line.fill.background()

    # Team Members (Clean 2-card layout)
    # Member 1
    add_card(s1, Inches(1.5), Inches(4.2), Inches(4.9), Inches(1.8), bg_color=FRAME_BG, border_color=CARD_BORDER)
    tb_m1 = s1.shapes.add_textbox(Inches(1.8), Inches(4.4), Inches(4.3), Inches(1.4))
    tf_m1 = tb_m1.text_frame
    p = tf_m1.paragraphs[0]
    p.text = "Tejasvi"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT
    p2 = tf_m1.add_paragraph()
    p2.text = "Registration No: 12315197\nArchitecture, Authentication & Cloud Database"
    p2.font.size = Pt(12)
    p2.font.color.rgb = MUTED_TEXT

    # Member 2
    add_card(s1, Inches(6.9), Inches(4.2), Inches(4.9), Inches(1.8), bg_color=FRAME_BG, border_color=CARD_BORDER)
    tb_m2 = s1.shapes.add_textbox(Inches(7.2), Inches(4.4), Inches(4.3), Inches(1.4))
    tf_m2 = tb_m2.text_frame
    p = tf_m2.paragraphs[0]
    p.text = "Arpan Dey"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT
    p2 = tf_m2.add_paragraph()
    p2.text = "Registration No: 12305886\nTask Modeling, CRUD Operations & Filtering Engine"
    p2.font.size = Pt(12)
    p2.font.color.rgb = MUTED_TEXT

    # =========================================================================
    # SLIDE 2: System Architecture Overview
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s2)
    add_header(s2, "System Architecture & Technology Stack", "Overview")

    arch_cards = [
        ("Client Tier", "React 18 + Vite", [
            "Component-driven SPA interface",
            "Client-side protected route guarding",
            "Axios JWT bearer token interceptor",
            "Responsive layout with Tailwind CSS"
        ]),
        ("Application Tier", "Node.js + Express", [
            "RESTful API design and route controllers",
            "Bcrypt security and JWT authorization",
            "Custom request error handling middleware",
            "Automated Swagger API documentation"
        ]),
        ("Data Tier", "MongoDB Atlas Cloud", [
            "Mongoose schema definitions & validations",
            "Referential user-task associations",
            "Performance compound indexing",
            "Live cloud replica set on AWS Mumbai"
        ])
    ]

    for idx, (tier_title, tech_sub, bullets) in enumerate(arch_cards):
        c_left = Inches(0.8 + idx * 4.0)
        add_card(s2, c_left, Inches(1.6), Inches(3.7), Inches(5.3), bg_color=WHITE)

        tb = s2.shapes.add_textbox(c_left + Inches(0.3), Inches(1.9), Inches(3.1), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = tier_title.upper()
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = PRIMARY
        p.space_after = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = tech_sub
        p2.font.size = Pt(18)
        p2.font.bold = True
        p2.font.color.rgb = DARK_TEXT
        p2.space_after = Pt(16)

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = f"•  {b}"
            pb.font.size = Pt(12)
            pb.font.color.rgb = BODY_TEXT
            pb.space_after = Pt(10)

    # =========================================================================
    # SLIDE 3: User Authentication & Password Security (Tejasvi's topic)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s3)
    add_header(s3, "User Authentication & Security", "Core Architecture")

    # Content Card (Left)
    add_card(s3, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), bg_color=WHITE)
    tb_c3 = s3.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True

    add_bullet_list(tf_c3, [
        ("Input Sanitization", "Trims whitespaces and lowercases emails to prevent accidental duplicates and invalid submissions."),
        ("Bcrypt Password Hashing", "Generates a 10-round salt before hashing. Plain text passwords are never stored in the database."),
        ("Escalation Defense", "Registration strictly hardcodes user privileges to prevent unauthorized administrative escalation."),
        ("Cryptographic Verification", "Login requests compare submitted credentials against the stored hash using secure salt comparison.")
    ])

    # Proof of Work Frame (Right)
    add_screenshot_frame(s3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
                         "Authentication & Registration UI",
                         "Paste screenshot of Login / Register card from http://localhost:5173/login")

    # =========================================================================
    # SLIDE 4: Stateless JWT Authorization & Route Protection (Tejasvi's topic)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s4)
    add_header(s4, "JWT Authorization & Route Guarding", "Session Security")

    # Content Card (Left)
    add_card(s4, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), bg_color=WHITE)
    tb_c4 = s4.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf_c4 = tb_c4.text_frame
    tf_c4.word_wrap = True

    add_bullet_list(tf_c4, [
        ("Stateless Tokenization", "Issues signed JSON Web Tokens (7-day validity) containing the user payload upon verified login."),
        ("Express Protect Middleware", "Extracts Bearer tokens from incoming headers and verifies signature integrity using process.env.JWT_SECRET."),
        ("Memory Protection", "Uses Mongoose .select('-password') when querying user context, ensuring password hashes are never held in memory."),
        ("Client Route Guard", "React ProtectedRoute blocks unauthenticated access and redirects unauthorized requests to login.")
    ])

    # Proof of Work Frame (Right)
    add_screenshot_frame(s4, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
                         "JWT Token in LocalStorage",
                         "Paste screenshot of browser DevTools -> Application -> Local Storage showing the active JWT token key")

    # =========================================================================
    # SLIDE 5: Cloud Database & Live Deployment (Tejasvi's topic)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s5)
    add_header(s5, "Cloud Database & Real-Time Sync", "Infrastructure")

    # Content Card (Left)
    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), bg_color=WHITE)
    tb_c5 = s5.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf_c5 = tb_c5.text_frame
    tf_c5.word_wrap = True

    add_bullet_list(tf_c5, [
        ("MongoDB Atlas Cluster", "Connected to a live 3-node replica set cluster (AWS Mumbai region) for high data availability."),
        ("Environment-Driven Config", "Database connection strings are read dynamically via process.env.MONGO_URI with zero hardcoded credentials."),
        ("Live Database Watcher", "Engineered a custom terminal monitoring tool (npm run db:watch) to stream live database modifications."),
        ("Cloud Blueprint Ready", "Configured Render blueprint (render.yaml) and Vercel routing rules for production deployment.")
    ])

    # Proof of Work Frame (Right)
    add_screenshot_frame(s5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
                         "MongoDB Atlas Cloud Cluster",
                         "Paste screenshot of MongoDB Atlas cluster dashboard or terminal running npm run db:watch")

    # =========================================================================
    # SLIDE 6: Task Modeling & Compound Indexing (Arpan's topic)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s6)
    add_header(s6, "Task Data Modeling & Compound Indexing", "Data Engine")

    # Content Card (Left)
    add_card(s6, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), bg_color=WHITE)
    tb_c6 = s6.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf_c6 = tb_c6.text_frame
    tf_c6.word_wrap = True

    add_bullet_list(tf_c6, [
        ("Referential Integrity", "Every task stores a required User ObjectId reference, establishing strict entity relationships in MongoDB."),
        ("Schema Constraints", "Standardizes task status (Pending, In Progress, Completed) and priority (Low, Medium, High) with automatic timestamps."),
        ("Compound Indexing", "Implemented multi-key indexes on { user: 1, status: 1 } and { user: 1, priority: 1 } to prevent full collection scans."),
        ("Query Performance", "Reduces complex user filtering query overhead from linear O(N) scans to logarithmic O(log N) B-Tree lookups.")
    ])

    # Proof of Work Frame (Right)
    add_screenshot_frame(s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
                         "Task Document & Index Schema",
                         "Paste screenshot of MongoDB Atlas Collections showing task fields (user ObjectId, status, priority, timestamps)")

    # =========================================================================
    # SLIDE 7: Task CRUD Operations & Ownership Isolation (Arpan's topic)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s7)
    add_header(s7, "Task CRUD & Tenant Isolation", "Core Logic")

    # Content Card (Left)
    add_card(s7, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), bg_color=WHITE)
    tb_c7 = s7.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf_c7 = tb_c7.text_frame
    tf_c7.word_wrap = True

    add_bullet_list(tf_c7, [
        ("Complete CRUD Operations", "Comprehensive endpoints for creating, reading, editing, and deleting tasks with standard HTTP response codes."),
        ("Strict Tenant Isolation", "Queries automatically bind to req.user._id, ensuring users cannot view, edit, or delete another user's tasks."),
        ("Input Validation", "Verifies 24-character hexadecimal ObjectId formats before processing queries to prevent unhandled database crashes."),
        ("Reactive UI Updates", "Frontend modal updates sync state immediately in React without requiring full browser page reloads.")
    ])

    # Proof of Work Frame (Right)
    add_screenshot_frame(s7, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
                         "Tasks Grid & Modal Interface",
                         "Paste screenshot of http://localhost:5173/tasks showing task cards and the Add/Edit Task modal dialog")

    # =========================================================================
    # SLIDE 8: Multi-Filtering, Sorting & Pagination (Arpan's topic)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s8)
    add_header(s8, "Filtering, Sorting & Server Pagination", "Performance")

    # Content Card (Left)
    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), bg_color=WHITE)
    tb_c8 = s8.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf_c8 = tb_c8.text_frame
    tf_c8.word_wrap = True

    add_bullet_list(tf_c8, [
        ("Multi-Parameter Filtering", "Dynamically combines multiple query parameters (e.g. status + priority) to fetch specific task subsets."),
        ("Whitelisted Dynamic Sorting", "Validates requested sort keys against an allowed list (dueDate, createdAt, title) to prevent query injection."),
        ("Server-Side Pagination", "Calculates page slices on the server using MongoDB .skip() and .limit(), keeping payloads light and fast."),
        ("Synchronized UI Toolbar", "Instant dropdown selection updates the task view without page resets.")
    ])

    # Proof of Work Frame (Right)
    add_screenshot_frame(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
                         "Filter Toolbar & Pagination",
                         "Paste screenshot of active filter dropdowns and bottom page navigation buttons on http://localhost:5173/tasks")

    # =========================================================================
    # SLIDE 9: Live Demonstration & Summary
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s9)
    add_header(s9, "Live Demonstration & Summary", "Conclusion")

    # Left: 4-Step Demo Flow
    add_card(s9, Inches(0.8), Inches(1.6), Inches(6.5), Inches(5.3), bg_color=WHITE)
    tb_d = s9.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.9), Inches(4.7))
    tf_d = tb_d.text_frame
    tf_d.word_wrap = True

    p = tf_d.paragraphs[0]
    p.text = "DEMONSTRATION WORKFLOW"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(12)

    demo_steps = [
        ("1. User Access & Security", "Demonstrate registration, password hashing verification, and JWT route guarding."),
        ("2. Task Operations", "Create and edit a task via modal dialog with form validation."),
        ("3. Query Performance", "Apply simultaneous status/priority filters and switch sort criteria."),
        ("4. Live Cloud Sync", "Show instant document reflection in MongoDB Atlas Cloud.")
    ]
    for step_num, step_desc in demo_steps:
        p_s = tf_d.add_paragraph()
        p_s.text = f"{step_num}: "
        p_s.font.bold = True
        p_s.font.size = Pt(13)
        p_s.font.color.rgb = DARK_TEXT
        
        p_sd = tf_d.add_paragraph()
        p_sd.text = step_desc
        p_sd.font.size = Pt(12)
        p_sd.font.color.rgb = BODY_TEXT
        p_sd.space_after = Pt(8)

    # Right: Project Summary & Links
    add_card(s9, Inches(7.6), Inches(1.6), Inches(4.9), Inches(5.3), bg_color=WHITE)
    tb_r = s9.shapes.add_textbox(Inches(7.9), Inches(1.9), Inches(4.3), Inches(4.7))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "PROJECT REPOSITORY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(8)

    p_repo = tf_r.add_paragraph()
    p_repo.text = "GitHub Repository:\ngithub.com/tejasvijain09/TaskFlow\n"
    p_repo.font.size = Pt(13)
    p_repo.font.color.rgb = DARK_TEXT
    p_repo.space_after = Pt(14)

    p_q = tf_r.add_paragraph()
    p_q.text = "Thank you!"
    p_q.font.size = Pt(28)
    p_q.font.bold = True
    p_q.font.color.rgb = PRIMARY
    p_q.space_after = Pt(6)

    p_qa = tf_r.add_paragraph()
    p_qa.text = "We are ready for questions and evaluation."
    p_qa.font.size = Pt(13)
    p_qa.font.color.rgb = MUTED_TEXT

    # Save presentation
    output_path = "/Users/tejasvi/Documents/Projects/College Projects/TaskFlow/TaskFlow_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    create_presentation()
