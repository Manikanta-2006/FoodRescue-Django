import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Theme colors
    PRIMARY = RGBColor(25, 135, 84)      # Forest Green
    SECONDARY = RGBColor(20, 83, 45)    # Dark Green
    ACCENT = RGBColor(245, 158, 11)     # Warm Orange
    BG_LIGHT = RGBColor(248, 250, 245)  # Light Cream
    TEXT_DARK = RGBColor(33, 37, 41)    # Dark Slate
    TEXT_MUTED = RGBColor(108, 117, 125)# Gray
    WHITE = RGBColor(255, 255, 255)
    CARD_BG = RGBColor(255, 255, 255)
    BORDER_COLOR = RGBColor(220, 230, 220)

    def add_background(slide, color=BG_LIGHT):
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        shape.line.fill.background()
        return shape

    def add_header(slide, title_text, category_text="FOODRESCUE PLATFORM"):
        # Category badge
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.4))
        tf = cat_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = category_text.upper()
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = PRIMARY

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = SECONDARY

        # Green accent bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.7), Inches(1.5), Inches(0.06))
        bar.fill.solid()
        bar.fill.fore_color.rgb = PRIMARY
        bar.line.fill.background()

    def add_card(slide, left, top, width, height, title, body_bullets, icon_letter="●", header_color=SECONDARY):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1.5)

        tx = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(width - 0.5), Inches(height - 0.4))
        tf = tx.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"{icon_letter}  {title}"
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = header_color

        for item in body_bullets:
            p2 = tf.add_paragraph()
            p2.text = f"•  {item}"
            p2.font.size = Pt(13)
            p2.font.color.rgb = TEXT_DARK
            p2.space_before = Pt(6)

    # -------------------------------------------------------------------------
    # SLIDE 1: Title Slide (Dark Theme)
    # -------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    add_background(s1, SECONDARY)

    # Decorative accent band
    band = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.4), Inches(7.5))
    band.fill.solid()
    band.fill.fore_color.rgb = ACCENT
    band.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11.0), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "ACADEMIC CAPSTONE PROJECT • INT253 WEB DEVELOPMENT IN DJANGO"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT

    p1 = tf.add_paragraph()
    p1.text = "FoodRescue – Food Donation &\nRedistribution Management Platform"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(16)

    p2 = tf.add_paragraph()
    p2.text = "A full-stack, database-driven web application to bridge food donors, NGOs, and volunteers in real-time."
    p2.font.size = Pt(17)
    p2.font.color.rgb = RGBColor(220, 235, 220)
    p2.space_before = Pt(16)

    p3 = tf.add_paragraph()
    p3.text = "Technology Stack: Python 3.x | Django 6.x | SQLite (Django ORM) | Bootstrap 5 | Django DTL"
    p3.font.size = Pt(13)
    p3.font.color.rgb = RGBColor(254, 243, 199)
    p3.space_before = Pt(28)

    # -------------------------------------------------------------------------
    # SLIDE 2: Problem Statement & Motivation
    # -------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_background(s2)
    add_header(s2, "Problem Statement & Real-World Motivation", "THE CHALLENGE")

    add_card(s2, 0.8, 2.1, 3.6, 4.7, "The Food Waste Crisis", [
        "Over 68 million tons of edible food is discarded annually in India.",
        "Major sources: wedding halls, luxury banquet hotels, restaurants, and canteens.",
        "Disposal into municipal landfills generates toxic methane gas, worsening climate impact."
    ], "⚠️", RGBColor(220, 53, 69))

    add_card(s2, 4.8, 2.1, 3.6, 4.7, "Severe Food Insecurity", [
        "Simultaneously, millions in urban shelters, orphanages, and streets face acute hunger.",
        "NGOs struggle with limited budgets to purchase fresh wholesome meals daily.",
        "High rates of child malnutrition and destitute vulnerability."
    ], "💔", RGBColor(180, 80, 20))

    add_card(s2, 8.8, 2.1, 3.6, 4.7, "The Logistics Disconnect", [
        "Cooked meals have limited shelf lives (6-12 hours safe window).",
        "Donors lack verified contacts of nearby shelters needing urgent collection.",
        "Absence of transparent, volunteer-driven transportation logistics."
    ], "🚚", PRIMARY)

    # -------------------------------------------------------------------------
    # SLIDE 3: Proposed Solution & Key Objectives
    # -------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_background(s3)
    add_header(s3, "Proposed Solution: FoodRescue Platform", "SYSTEM OBJECTIVES")

    add_card(s3, 0.8, 2.1, 3.6, 4.7, "Real-Time Food Listing", [
        "Donors post surplus food in under 2 minutes.",
        "Record food name, portions, preparation timestamp, safe expiry cutoff, and pickup address.",
        "Automated expiry tracking prevents distribution of spoiled food."
    ], "🍲", PRIMARY)

    add_card(s3, 4.8, 2.1, 3.6, 4.7, "Hyperlocal NGO Discovery", [
        "Verified charities browse real-time listings filtered by city (Hyderabad, Bengaluru, Mumbai).",
        "Search by food keywords (Biryani, Pav, Atta, Fruits).",
        "Formal online food request mechanism with portion allocation."
    ], "🏢", SECONDARY)

    add_card(s3, 8.8, 2.1, 3.6, 4.7, "Volunteer Dispatch Network", [
        "Couriers claim open delivery tasks in their neighborhood.",
        "Real-time status updates: 'Collected / In Transit' to 'Delivered Successfully'.",
        "Complete digital audit trail with timestamps and remarks."
    ], "🚴", ACCENT)

    # -------------------------------------------------------------------------
    # SLIDE 4: Architecture & Design Pattern (MVT)
    # -------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_background(s4)
    add_header(s4, "System Architecture: Django MVT Pattern", "ARCHITECTURE & DESIGN")

    add_card(s4, 0.8, 2.1, 3.6, 4.7, "Model Layer (Data)", [
        "Django ORM classes mapping to SQLite database.",
        "Handles data validation, model relationships (1:1, 1:N), and automated slug generation.",
        "Zero raw SQL required; fully protected against SQL injection attacks."
    ], "🗄️", PRIMARY)

    add_card(s4, 4.8, 2.1, 3.6, 4.7, "View Layer (Logic)", [
        "Processes incoming HTTP GET & POST requests.",
        "Executes business logic, role verification decorators, and database queries.",
        "Prepares context payloads and returns HTML templates or JsonResponse data."
    ], "⚙️", SECONDARY)

    add_card(s4, 8.8, 2.1, 3.6, 4.7, "Template Layer (UI)", [
        "Presentation built with Django Template Language (DTL).",
        "Modular layout inheritance (base.html with extends and blocks).",
        "Reusable includes (navbar, footer, donation cards, status badges)."
    ], "🎨", ACCENT)

    # -------------------------------------------------------------------------
    # SLIDE 5: Modular Applications
    # -------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_background(s5)
    add_header(s5, "Modular Application Breakdown", "PROJECT STRUCTURE")

    add_card(s5, 0.8, 2.1, 3.6, 4.7, "App 1: accounts", [
        "User registration with role selection (Donor, NGO, Volunteer).",
        "Authentication, login, logout, and profile management.",
        "Role-based view decorators (@donor_required, @ngo_required, @volunteer_required).",
        "Context processor providing user role flags across all templates."
    ], "👤", PRIMARY)

    add_card(s5, 4.8, 2.1, 3.6, 4.7, "App 2: donations", [
        "Food donation creation, editing, and deletion (Full ORM CRUD).",
        "Public homepage with live database aggregate statistics.",
        "Hyperlocal search (Q objects) and category filtering.",
        "Custom path converters (slug, int, re_path) and JSON API endpoints."
    ], "📦", SECONDARY)

    add_card(s5, 8.8, 2.1, 3.6, 4.7, "App 3: requests", [
        "Formal food claiming by verified NGOs.",
        "Donor approval & rejection workflows.",
        "Automatic generation of Delivery dispatch tasks.",
        "Volunteer delivery claiming, status updating, and remarks logging."
    ], "📋", ACCENT)

    # -------------------------------------------------------------------------
    # SLIDE 6: User Roles & Ecosystem
    # -------------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_background(s6)
    add_header(s6, "User Roles & Permissions Ecosystem", "ROLES & SECURITY")

    add_card(s6, 0.8, 2.1, 2.7, 4.7, "Food Donor", [
        "Hotels, caterers, individuals.",
        "Post surplus food batches.",
        "Upload food images.",
        "Accept / reject incoming NGO requests.",
        "Track personal donation history."
    ], "🏨", PRIMARY)

    add_card(s6, 3.8, 2.1, 2.7, 4.7, "NGO Receiver", [
        "Orphanages, shelters, food banks.",
        "Browse available surplus food.",
        "Filter by city and food category.",
        "Submit food claims with portion count.",
        "Track delivery transit in real-time."
    ], "🏛️", SECONDARY)

    add_card(s6, 6.8, 2.1, 2.7, 4.7, "Volunteer", [
        "Passionate bike/cargo couriers.",
        "View open pickup tasks in vicinity.",
        "Inspect food packaging condition.",
        "Mark food as 'Collected'.",
        "Mark food as 'Delivered' with notes."
    ], "🚴", ACCENT)

    add_card(s6, 9.8, 2.1, 2.7, 4.7, "Administrator", [
        "Platform staff & directors.",
        "Built-in Django admin panel.",
        "Verify registered NGOs.",
        "Audit donations and deliveries.",
        "View system health analytics."
    ], "🛡️", RGBColor(13, 110, 253))

    # -------------------------------------------------------------------------
    # SLIDE 7: Database Models & Relational Schema
    # -------------------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_background(s7)
    add_header(s7, "Database Design: 4 Relational Models", "ORM DATA LAYER")

    add_card(s7, 0.8, 2.1, 2.7, 4.7, "UserProfile", [
        "1:1 relation with auth.User.",
        "role: Donor, NGO, Volunteer.",
        "phone: Indian mobile (+91).",
        "organization_name.",
        "city & address.",
        "is_verified boolean.",
        "profile_image."
    ], "1:1", PRIMARY)

    add_card(s7, 3.8, 2.1, 2.7, 4.7, "Donation", [
        "FK to User (Donor).",
        "food_name & unique slug.",
        "category (Biryani, Bread, Thali).",
        "quantity & unit (plates, kg, L).",
        "prepared_at & expiry_at.",
        "city & pickup_address.",
        "status: AVAILABLE, COLLECTED..."
    ], "1:N", SECONDARY)

    add_card(s7, 6.8, 2.1, 2.7, 4.7, "FoodRequest", [
        "FK to Donation.",
        "FK to User (NGO Receiver).",
        "quantity_requested (decimal).",
        "message: distribution plan.",
        "status: PENDING, APPROVED, REJECTED, COMPLETED.",
        "requested_at timestamp."
    ], "1:N", ACCENT)

    add_card(s7, 9.8, 2.1, 2.7, 4.7, "Delivery", [
        "1:1 with FoodRequest.",
        "FK to User (Volunteer, nullable).",
        "pickup_time & delivery_time.",
        "delivery_status: ASSIGNED, PICKED_UP, DELIVERED.",
        "remarks: package inspection notes."
    ], "1:1", RGBColor(108, 117, 125))

    # -------------------------------------------------------------------------
    # SLIDE 8: Academic URL Routing & Converters
    # -------------------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_background(s8)
    add_header(s8, "Mandatory Academic URL Routing Showcase", "INT253 SYLLABUS")

    add_card(s8, 0.8, 2.1, 5.6, 2.2, "slug Path Converter", [
        "Route: /donations/detail/<slug:slug>/",
        "View: donation_detail_slug_view()",
        "Uses unique slug for canonical, SEO-friendly detail pages."
    ], "🔗", PRIMARY)

    add_card(s8, 6.8, 2.1, 5.6, 2.2, "int Path Converter", [
        "Route: /donations/id/<int:pk>/",
        "View: donation_detail_id_view()",
        "Resolves primary key ID and performs 302 canonical redirection to slug."
    ], "🔢", SECONDARY)

    add_card(s8, 0.8, 4.6, 5.6, 2.2, "re_path() Regular Expression", [
        "Route: re_path(r'^donations/category/(?P<category_code>[a-zA-Z0-9_-]+)/$')",
        "View: donation_category_view()",
        "Captures regex group to filter food categories dynamically."
    ], "⚙️", ACCENT)

    add_card(s8, 6.8, 4.6, 5.6, 2.2, "str Path Converter & JSON APIs", [
        "Route: /accounts/role/<str:role_name>/",
        "JSON APIs: /api/donations/ & /api/stats/",
        "Returns JsonResponse payloads for asynchronous frontend widgets."
    ], "⚡", RGBColor(13, 110, 253))

    # -------------------------------------------------------------------------
    # SLIDE 9: Complete Redistribution Lifecycle
    # -------------------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_background(s9)
    add_header(s9, "Complete Food Redistribution Lifecycle", "WORKFLOW")

    add_card(s9, 0.8, 2.1, 2.7, 4.7, "Step 1: Listing", [
        "Grand Taj Banjara lists 70 plates of Veg Dum Biryani.",
        "Specifies 9-hour expiry.",
        "Status: AVAILABLE.",
        "Appears on public discovery and JSON search API."
    ], "1️⃣", PRIMARY)

    add_card(s9, 3.8, 2.1, 2.7, 4.7, "Step 2: Request", [
        "Akshaya Seva Foundation discovers the listing.",
        "Submits request for 60 plates for night shelter feed.",
        "Donation status transitions to REQUESTED.",
        "Donor notified on dashboard."
    ], "2️⃣", SECONDARY)

    add_card(s9, 6.8, 2.1, 2.7, 4.7, "Step 3: Dispatch", [
        "Taj Hotel accepts request.",
        "System creates Delivery object (ASSIGNED).",
        "Volunteer Ramesh claims task.",
        "Picks up food; marks 'Collected'. Status: IN TRANSIT."
    ], "3️⃣", ACCENT)

    add_card(s9, 9.8, 2.1, 2.7, 4.7, "Step 4: Fulfillment", [
        "Ramesh arrives at Secunderabad shelter.",
        "Verifies container temperature.",
        "Logs handover remarks.",
        "Marks 'Delivered'. Status: DELIVERED / COMPLETED."
    ], "4️⃣", RGBColor(25, 135, 84))

    # -------------------------------------------------------------------------
    # SLIDE 10: Security, Validation & Error Handling
    # -------------------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_background(s10)
    add_header(s10, "Security, Authorization & Quality Assurance", "ROBUSTNESS")

    add_card(s10, 0.8, 2.1, 3.6, 4.7, "Web Security", [
        "CSRF Protection: {% csrf_token %} on every state-modifying POST form.",
        "Password Hashing: Industry-standard PBKDF2 with SHA-256.",
        "SQL Injection Prevention: Guaranteed by Django ORM parameterized queries.",
        "Cross-Site Scripting (XSS) defense via automatic DTL HTML escaping."
    ], "🔒", PRIMARY)

    add_card(s10, 4.8, 2.1, 3.6, 4.7, "Access Control & Validation", [
        "Role Guards: @donor_required, @ngo_required, @volunteer_required decorators.",
        "Form Clean Methods: Validates quantity > 0 and expiry_at > prepared_at.",
        "Prevents requesting expired donations.",
        "Row-level authorization: users cannot edit or delete peers' donations."
    ], "🛡️", SECONDARY)

    add_card(s10, 8.8, 2.1, 3.6, 4.7, "Testing & Error Handling", [
        "7 Automated Unit Tests (donations/tests.py): 100% passing.",
        "Tests auth, CRUD, search Q queries, converters, and lifecycle.",
        "Custom Error Handlers: handler404 and handler500 with branded templates.",
        "get_object_or_404 guarantees graceful HTTP 404 responses."
    ], "✅", ACCENT)

    # -------------------------------------------------------------------------
    # SLIDE 11: Technology Stack Summary
    # -------------------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    add_background(s11)
    add_header(s11, "Technology Stack & Development Environment", "TECH ARCHITECTURE")

    add_card(s11, 0.8, 2.1, 5.6, 4.7, "Backend Architecture", [
        "Python 3.14: Clean, modern syntax & execution.",
        "Django 6.1: High-level Python web framework.",
        "SQLite 3: Zero-config, lightweight relational database.",
        "Django ORM: Full object-relational mapping without raw SQL.",
        "Django Authentication: Session middleware and user profiles.",
        "Pillow (PIL): Image processing and validation for food uploads."
    ], "💻", PRIMARY)

    add_card(s11, 6.8, 2.1, 5.6, 4.7, "Frontend & UI/UX Design", [
        "HTML5 & CSS3: Semantic markup and modern styling.",
        "Bootstrap 5.3: Responsive grid and mobile-first layout.",
        "Bootstrap Icons 1.11: Clean visual iconography.",
        "Vanilla JavaScript: Asynchronous live search widget with debounce.",
        "Theme Palette: Forest Green (#198754), Dark Green (#14532D), Warm Orange (#F59E0B).",
        "Django Template Language (DTL): Block inheritance and custom filters."
    ], "🎨", SECONDARY)

    # -------------------------------------------------------------------------
    # SLIDE 12: Conclusion & Future Scope
    # -------------------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    add_background(s12)
    add_header(s12, "Conclusion & Future Roadmap", "IMPACT & VISION")

    add_card(s12, 0.8, 2.1, 5.6, 4.7, "Project Achievements", [
        "Fully functional, production-style Django web application.",
        "100% compliant with all INT253 academic criteria.",
        "Eliminates food waste while feeding disadvantaged communities.",
        "Authentic Indian dataset (Biryani, Thali, Idli/Vada, Mandi fruits).",
        "Demonstrated 7/7 automated unit test suite passing."
    ], "🏆", PRIMARY)

    add_card(s12, 6.8, 2.1, 5.6, 4.7, "Future Enhancements", [
        "Mobile App: Flutter / React Native Android/iOS client.",
        "Live GPS Tracking: Volunteer route tracking via Google Maps API.",
        "AI Shelf-Life Predictor: Computer vision to detect food freshness.",
        "IoT Temperature Logging: Smart sensors for cold-chain compliance.",
        "SMS/WhatsApp Alerts: Instant Twilio/Gupshup delivery notifications."
    ], "🚀", ACCENT)

    # -------------------------------------------------------------------------
    # SLIDE 13: Thank You & Q&A (Dark Theme)
    # -------------------------------------------------------------------------
    s13 = prs.slides.add_slide(blank_layout)
    add_background(s13, SECONDARY)

    # Decorative accent band
    band13 = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.4), Inches(7.5))
    band13.fill.solid()
    band13.fill.fore_color.rgb = ACCENT
    band13.line.fill.background()

    tb13 = s13.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(11.0), Inches(4.5))
    tf13 = tb13.text_frame
    tf13.word_wrap = True

    p0 = tf13.paragraphs[0]
    p0.text = "ACADEMIC VIVA EXAMINATION • READY FOR DEMONSTRATION"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT

    p1 = tf13.add_paragraph()
    p1.text = "Thank You!"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(10)

    p2 = tf13.add_paragraph()
    p2.text = "FoodRescue: Rescue Food, Share Hope."
    p2.font.size = Pt(20)
    p2.font.color.rgb = RGBColor(220, 235, 220)
    p2.space_before = Pt(10)

    p3 = tf13.add_paragraph()
    p3.text = "Live Server: http://127.0.0.1:8000/  |  Admin Credentials: admin / admin123\nOpen for Questions & Professor Feedback"
    p3.font.size = Pt(15)
    p3.font.color.rgb = RGBColor(254, 243, 199)
    p3.space_before = Pt(28)

    output_path = "FoodRescue_Project_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation generated successfully: {output_path}")

if __name__ == "__main__":
    create_presentation()
