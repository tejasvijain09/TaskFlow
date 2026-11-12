import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen slides (13.333 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # High-Contrast Projector Palette
    BG_CANVAS = RGBColor(248, 250, 252)     # #f8fafc Clean canvas
    PRIMARY = RGBColor(67, 56, 202)         # #4338ca Deep High-Contrast Indigo
    DARK_TEXT = RGBColor(15, 23, 42)        # #0f172a Deep Slate (Maximum contrast)
    BODY_TEXT = RGBColor(30, 41, 59)        # #1e293b Very Dark Slate for projector readability
    MUTED_TEXT = RGBColor(71, 85, 105)      # #475569 Crisp Medium Slate
    WHITE = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(203, 213, 225)   # #cbd5e1 Strong crisp border
    FRAME_BG = RGBColor(241, 245, 249)      # #f1f5f9
    FRAME_BORDER = RGBColor(148, 163, 184)  # #94a3b8

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
        shape.line.width = Pt(1.5)
        return shape

    def add_header(slide, title_text, category_text=None):
        # Header box with large fonts for projector
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.05))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        if category_text:
            p_cat = tf.paragraphs[0]
            p_cat.text = category_text.upper()
            p_cat.font.size = Pt(13)
            p_cat.font.bold = True
            p_cat.font.color.rgb = PRIMARY
            p_cat.space_after = Pt(2)

            p_title = tf.add_paragraph()
        else:
            p_title = tf.paragraphs[0]

        p_title.text = title_text
        p_title.font.size = Pt(32)
        p_title.font.bold = True
        p_title.font.color.rgb = DARK_TEXT

    def add_screenshot_frame(slide, left, top, width, height, label_title, tip_text):
        # Card container for screenshot
        add_card(slide, left, top, width, height, bg_color=FRAME_BG, border_color=FRAME_BORDER)

        tb = slide.shapes.add_textbox(left + Inches(0.4), top + Inches(1.3), width - Inches(0.8), height - Inches(2.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = "PROOF OF WORK"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = PRIMARY
        p1.alignment = PP_ALIGN.CENTER
        p1.space_after = Pt(10)

        p2 = tf.add_paragraph()
        p2.text = label_title
        p2.font.size = Pt(18)
        p2.font.bold = True
        p2.font.color.rgb = DARK_TEXT
        p2.alignment = PP_ALIGN.CENTER
        p2.space_after = Pt(14)

        p3 = tf.add_paragraph()
        p3.text = tip_text
        p3.font.size = Pt(14)
        p3.font.color.rgb = MUTED_TEXT
        p3.alignment = PP_ALIGN.CENTER

    def add_large_bullet_list(tf, items):
        for i, (heading, detail) in enumerate(items):
            p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
            p.space_after = Pt(16)
            p.line_spacing = 1.25

            # Bold Heading (17pt for projector visibility)
            run_h = p.add_run()
            run_h.text = f"•  {heading}: "
            run_h.font.bold = True
            run_h.font.size = Pt(17)
            run_h.font.color.rgb = DARK_TEXT

            # Detail text (15pt for projector visibility)
            run_d = p.add_run()
            run_d.text = detail
            run_d.font.bold = False
            run_d.font.size = Pt(15)
            run_d.font.color.rgb = BODY_TEXT

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s1)

    add_card(s1, Inches(0.9), Inches(0.8), Inches(11.533), Inches(5.9), bg_color=WHITE)

    # Top Tag
    tb1_tag = s1.shapes.add_textbox(Inches(1.4), Inches(1.2), Inches(10.5), Inches(0.4))
    tf1_tag = tb1_tag.text_frame
    p = tf1_tag.paragraphs[0]
    p.text = "ACADEMIC PROJECT DEMONSTRATION  •  CSF402"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    # Title
    tb1_title = s1.shapes.add_textbox(Inches(1.4), Inches(1.65), Inches(10.5), Inches(1.2))
    tf1_title = tb1_title.text_frame
    p = tf1_title.paragraphs[0]
    p.text = "TaskFlow"
    p.font.size = Pt(46)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT

    # Subtitle
    tb1_sub = s1.shapes.add_textbox(Inches(1.4), Inches(2.75), Inches(10.5), Inches(0.6))
    tf1_sub = tb1_sub.text_frame
    p = tf1_sub.paragraphs[0]
    p.text = "A Full-Stack Task Management System built with the MERN Stack"
    p.font.size = Pt(18)
    p.font.color.rgb = MUTED_TEXT

    # Faculty Info
    tb1_eval = s1.shapes.add_textbox(Inches(1.4), Inches(3.45), Inches(10.5), Inches(0.5))
    tf1_eval = tb1_eval.text_frame
    p = tf1_eval.paragraphs[0]
    p.text = "Faculty Evaluator: Mr. Jitesh Kumar Bhatia"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT

    # Divider
    line1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.4), Inches(4.05), Inches(10.5), Inches(0.02))
    line1.fill.solid()
    line1.fill.fore_color.rgb = CARD_BORDER
    line1.line.fill.background()

    # Team Members (Large, prominent cards)
    add_card(s1, Inches(1.4), Inches(4.35), Inches(5.1), Inches(1.9), bg_color=FRAME_BG, border_color=CARD_BORDER)
    tb_m1 = s1.shapes.add_textbox(Inches(1.7), Inches(4.55), Inches(4.5), Inches(1.5))
    tf_m1 = tb_m1.text_frame
    p = tf_m1.paragraphs[0]
    p.text = "Tejasvi"
    p.font.size = Pt(19)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT
    p2 = tf_m1.add_paragraph()
    p2.text = "Registration No: 12315197\nArchitecture, Authentication & Cloud Database"
    p2.font.size = Pt(14)
    p2.font.color.rgb = MUTED_TEXT

    add_card(s1, Inches(6.8), Inches(4.35), Inches(5.1), Inches(1.9), bg_color=FRAME_BG, border_color=CARD_BORDER)
    tb_m2 = s1.shapes.add_textbox(Inches(7.1), Inches(4.55), Inches(4.5), Inches(1.5))
    tf_m2 = tb_m2.text_frame
    p = tf_m2.paragraphs[0]
    p.text = "Arpan Dey"
    p.font.size = Pt(19)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT
    p2 = tf_m2.add_paragraph()
    p2.text = "Registration No: 12305886\nTask Modeling, CRUD Operations & Filtering Engine"
    p2.font.size = Pt(14)
    p2.font.color.rgb = MUTED_TEXT

    # =========================================================================
    # SLIDE 2: Architecture Overview
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s2)
    add_header(s2, "System Architecture & Technology Stack", "Overview")

    arch_cards = [
        ("Client Tier", "React 18 + Vite", [
            "Component-based Single Page App",
            "Client-side protected route guarding",
            "Axios JWT bearer token interceptor",
            "Responsive UI with Tailwind CSS"
        ]),
        ("Application Tier", "Node.js + Express", [
            "RESTful API design and controllers",
            "Bcrypt security & JWT authorization",
            "Centralized error handling middleware",
            "Automated Swagger API documentation"
        ]),
        ("Data Tier", "MongoDB Atlas Cloud", [
            "Mongoose schema validation & enums",
            "Referential user-task associations",
            "High-performance compound indexing",
            "Live cloud replica set on AWS Mumbai"
        ])
    ]

    for idx, (tier_title, tech_sub, bullets) in enumerate(arch_cards):
        c_left = Inches(0.8 + idx * 4.0)
        add_card(s2, c_left, Inches(1.6), Inches(3.7), Inches(5.3), bg_color=WHITE)

        tb = s2.shapes.add_textbox(c_left + Inches(0.35), Inches(1.9), Inches(3.0), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = tier_title.upper()
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = PRIMARY
        p.space_after = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = tech_sub
        p2.font.size = Pt(20)
        p2.font.bold = True
        p2.font.color.rgb = DARK_TEXT
        p2.space_after = Pt(16)

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = f"•  {b}"
            pb.font.size = Pt(14)
            pb.font.color.rgb = BODY_TEXT
            pb.space_after = Pt(12)

    # =========================================================================
    # SLIDE 3: User Authentication & Security (Tejasvi)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s3)
    add_header(s3, "User Authentication & Security", "Core Security")

    add_card(s3, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), bg_color=WHITE)
    tb_c3 = s3.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True

    add_large_bullet_list(tf_c3, [
        ("Input Sanitization", "Trims whitespace and lowercases emails to prevent duplicate accounts and injection flaws."),
        ("Bcrypt Password Hashing", "Generates a 10-round salt prior to hashing. Plain text passwords are never stored in the database."),
        ("Escalation Defense", "Registration hardcodes default user privileges to block unauthorized administrative escalation."),
        ("Cryptographic Verification", "Login requests compare submitted credentials against stored hashes using secure mathematical comparisons.")
    ])

    add_screenshot_frame(s3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
                         "Authentication & Registration UI",
                         "Paste screenshot of Login / Register card from http://localhost:5173/login")

    # =========================================================================
    # SLIDE 4: JWT Authorization & Route Guarding (Tejasvi)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s4)
    add_header(s4, "JWT Authorization & Route Guarding", "Session Security")

    add_card(s4, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), bg_color=WHITE)
    tb_c4 = s4.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf_c4 = tb_c4.text_frame
    tf_c4.word_wrap = True

    add_large_bullet_list(tf_c4, [
        ("Stateless Tokenization", "Issues signed JSON Web Tokens (7-day validity) containing user ID claims upon verified login."),
        ("Express Protect Middleware", "Extracts Bearer tokens from incoming headers and validates cryptographic signatures via JWT_SECRET."),
        ("Memory Protection", "Uses Mongoose .select('-password') when querying user context, ensuring password hashes are never leaked."),
        ("Client Route Guard", "React ProtectedRoute checks browser localStorage and automatically redirects unauthorized visits to login.")
    ])

    add_screenshot_frame(s4, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
                         "JWT Token in LocalStorage",
                         "Paste screenshot of browser DevTools -> Application -> Local Storage showing the active JWT token key")

    # =========================================================================
    # SLIDE 5: Cloud Database & Live Sync (Tejasvi)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s5)
    add_header(s5, "Cloud Database & Real-Time Sync", "Infrastructure")

    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), bg_color=WHITE)
    tb_c5 = s5.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf_c5 = tb_c5.text_frame
    tf_c5.word_wrap = True

    add_large_bullet_list(tf_c5, [
        ("MongoDB Atlas Cluster", "Connected to a live 3-node replica set cluster (AWS Mumbai region) for high data availability."),
        ("Dynamic Environment Config", "Connection strings are read dynamically via process.env.MONGO_URI with zero hardcoded credentials."),
        ("Live Database Watcher", "Engineered custom terminal monitoring tool (npm run db:watch) to stream live database modifications."),
        ("Cloud Blueprint Ready", "Configured Render blueprint (render.yaml) and Vercel routing rules for production deployment.")
    ])

    add_screenshot_frame(s5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
                         "MongoDB Atlas Cloud Cluster",
                         "Paste screenshot of MongoDB Atlas cluster dashboard or terminal running npm run db:watch")

    # =========================================================================
    # SLIDE 6: Task Modeling & Compound Indexing (Arpan)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s6)
    add_header(s6, "Task Data Modeling & Compound Indexing", "Data Engine")

    add_card(s6, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), bg_color=WHITE)
    tb_c6 = s6.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf_c6 = tb_c6.text_frame
    tf_c6.word_wrap = True

    add_large_bullet_list(tf_c6, [
        ("Referential Integrity", "Every task stores a required User ObjectId reference, establishing strict entity relationships in MongoDB."),
        ("Schema Constraints", "Standardizes task status (Pending, In Progress, Completed) and priority (Low, Medium, High) with timestamps."),
        ("Compound Indexing", "Implemented multi-key indexes on { user: 1, status: 1 } and { user: 1, priority: 1 } to prevent full scans."),
        ("Query Performance", "Reduces complex user filtering query overhead from linear O(N) scans to logarithmic O(log N) B-Tree lookups.")
    ])

    add_screenshot_frame(s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
                         "Task Document & Index Schema",
                         "Paste screenshot of MongoDB Atlas Collections showing task fields (user ObjectId, status, priority, timestamps)")

    # =========================================================================
    # SLIDE 7: Task CRUD & Tenant Isolation (Arpan)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s7)
    add_header(s7, "Task CRUD & Tenant Isolation", "Core Logic")

    add_card(s7, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), bg_color=WHITE)
    tb_c7 = s7.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf_c7 = tb_c7.text_frame
    tf_c7.word_wrap = True

    add_large_bullet_list(tf_c7, [
        ("Complete CRUD Operations", "Comprehensive endpoints for creating, reading, editing, and deleting tasks with standard HTTP response codes."),
        ("Strict Tenant Isolation", "Queries automatically bind to req.user._id, ensuring users cannot view, edit, or delete another user's tasks."),
        ("Input Validation", "Verifies 24-character hexadecimal ObjectId formats before processing queries to prevent unhandled database crashes."),
        ("Reactive UI Updates", "Frontend modal updates sync state immediately in React without requiring full browser page reloads.")
    ])

    add_screenshot_frame(s7, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
                         "Tasks Grid & Modal Interface",
                         "Paste screenshot of http://localhost:5173/tasks showing task cards and the Add/Edit Task modal dialog")

    # =========================================================================
    # SLIDE 8: Filtering, Sorting & Server Pagination (Arpan)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s8)
    add_header(s8, "Filtering, Sorting & Server Pagination", "Performance")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), bg_color=WHITE)
    tb_c8 = s8.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf_c8 = tb_c8.text_frame
    tf_c8.word_wrap = True

    add_large_bullet_list(tf_c8, [
        ("Multi-Parameter Filtering", "Dynamically combines multiple query parameters (e.g. status + priority) to fetch specific task subsets."),
        ("Whitelisted Dynamic Sorting", "Validates requested sort keys against an allowed list (dueDate, createdAt, title) to prevent query injection."),
        ("Server-Side Pagination", "Calculates page slices on the server using MongoDB .skip() and .limit(), keeping payloads light and fast."),
        ("Synchronized UI Toolbar", "Instant dropdown selection updates the task view without page resets.")
    ])

    add_screenshot_frame(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
                         "Filter Toolbar & Pagination",
                         "Paste screenshot of active filter dropdowns and bottom page navigation buttons on http://localhost:5173/tasks")

    # =========================================================================
    # SLIDE 9: Additional Features (Dashboard Analytics, Socket.IO, Swagger, Admin)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s9)
    add_header(s9, "Analytics, Real-Time Alerts & Administration", "Extended Capabilities")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), bg_color=WHITE)
    tb_c9 = s9.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf_c9 = tb_c9.text_frame
    tf_c9.word_wrap = True

    add_large_bullet_list(tf_c9, [
        ("Aggregation Pipeline", "Uses MongoDB $match and $group stages to compute live dashboard metrics (Total, Pending, In Progress, Completed)."),
        ("Real-Time Socket.IO", "Delivers instant websocket push alerts across client browser sessions upon task creation and status changes."),
        ("Interactive Swagger Docs", "Integrated OpenAPI 3.0 specification at /api-docs allowing live API testing with Bearer authorization."),
        ("Admin Control Panel", "Dedicated management panel (/admin) with requireAdmin middleware for user oversight and task moderation.")
    ])

    add_screenshot_frame(s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
                         "Analytics Dashboard & Swagger UI",
                         "Paste screenshot of Dashboard metrics cards from http://localhost:5173/dashboard or Swagger UI at /api-docs")

    # =========================================================================
    # SLIDE 10: Live Demonstration & Summary
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s10)
    add_header(s10, "Live Demonstration & Summary", "Conclusion")

    # Left: 4-Step Demo Flow
    add_card(s10, Inches(0.8), Inches(1.6), Inches(6.5), Inches(5.3), bg_color=WHITE)
    tb_d = s10.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.9), Inches(4.7))
    tf_d = tb_d.text_frame
    tf_d.word_wrap = True

    p = tf_d.paragraphs[0]
    p.text = "DEMONSTRATION WORKFLOW"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(14)

    demo_steps = [
        ("1. User Access & Security", "Demonstrate registration, password hashing verification, and JWT route guarding."),
        ("2. Task Operations", "Create and edit a task via modal dialog with form validation."),
        ("3. Query Performance", "Apply simultaneous status/priority filters and switch sort criteria."),
        ("4. Live Cloud Sync & Real-Time", "Show instant document reflection in MongoDB Atlas Cloud and Socket.IO alerts.")
    ]
    for step_num, step_desc in demo_steps:
        p_s = tf_d.add_paragraph()
        p_s.text = f"{step_num}: "
        p_s.font.bold = True
        p_s.font.size = Pt(15)
        p_s.font.color.rgb = DARK_TEXT
        
        p_sd = tf_d.add_paragraph()
        p_sd.text = step_desc
        p_sd.font.size = Pt(14)
        p_sd.font.color.rgb = BODY_TEXT
        p_sd.space_after = Pt(10)

    # Right: Project Summary & Links
    add_card(s10, Inches(7.6), Inches(1.6), Inches(4.9), Inches(5.3), bg_color=WHITE)
    tb_r = s10.shapes.add_textbox(Inches(7.9), Inches(1.9), Inches(4.3), Inches(4.7))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "PROJECT REPOSITORY"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(10)

    p_repo = tf_r.add_paragraph()
    p_repo.text = "GitHub Repository:\ngithub.com/tejasvijain09/TaskFlow\n"
    p_repo.font.size = Pt(15)
    p_repo.font.color.rgb = DARK_TEXT
    p_repo.space_after = Pt(16)

    p_q = tf_r.add_paragraph()
    p_q.text = "Thank you!"
    p_q.font.size = Pt(32)
    p_q.font.bold = True
    p_q.font.color.rgb = PRIMARY
    p_q.space_after = Pt(8)

    p_qa = tf_r.add_paragraph()
    p_qa.text = "We are ready for questions and evaluation."
    p_qa.font.size = Pt(15)
    p_qa.font.color.rgb = MUTED_TEXT

    # Save presentation
    output_path = "/Users/tejasvi/Documents/Projects/College Projects/TaskFlow/TaskFlow_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    create_presentation()
