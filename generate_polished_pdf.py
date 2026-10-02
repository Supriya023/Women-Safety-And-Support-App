import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# Theme Palette
PRIMARY = colors.HexColor("#5B34E6")       # Vibrant Purple Brand
PRIMARY_DARK = colors.HexColor("#37179E")  # Deep Purple
TEXT_MAIN = colors.HexColor("#1A1F36")     # Charcoal
TEXT_MUTED = colors.HexColor("#5A6282")    # Subtle Slate
BG_LIGHT = colors.HexColor("#F8F9FC")      # Soft Light Gray
BG_CARD = colors.HexColor("#FFFFFF")       # Card White
BORDER_COLOR = colors.HexColor("#DDE2F0")  # Soft Border

ACCENT_RED = colors.HexColor("#DC2626")    # SOS Red
BG_RED = colors.HexColor("#FEF2F2")        # Soft Red Card
ACCENT_GREEN = colors.HexColor("#059669")  # Volunteer Green
BG_GREEN = colors.HexColor("#ECFDF5")      # Soft Green Card
ACCENT_PURPLE = colors.HexColor("#7C3AED") # AI Purple
BG_PURPLE = colors.HexColor("#F5F3FF")     # Soft Purple Card
ACCENT_AMBER = colors.HexColor("#D97706")  # Warning Amber
BG_AMBER = colors.HexColor("#FFFBEB")      # Soft Amber Card
ACCENT_BLUE = colors.HexColor("#2563EB")   # Tech Blue
BG_BLUE = colors.HexColor("#EFF6FF")       # Soft Blue Card
CODE_BG = colors.HexColor("#0F172A")       # Dark code block background
WHITE = colors.HexColor("#FFFFFF")

class ModernDocCanvas(canvas.Canvas):
    """
    Two-pass canvas for professional headers and footers with dynamic page numbers.
    Suppresses header/footer on page 1 (cover).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        if self._pageNumber == 1:
            return  # Clean cover page

        self.saveState()
        
        # Running Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(PRIMARY)
        self.drawString(50, 752, "WOMEN SAFETY AND SUPPORT SYSTEM (ADHIRA)")
        self.setFont("Helvetica", 8)
        self.setFillColor(TEXT_MUTED)
        self.drawRightString(562, 752, "Comprehensive Product & Architecture Guide")
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.75)
        self.line(50, 745, 562, 745)

        # Running Footer
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.75)
        self.line(50, 42, 562, 42)
        self.setFont("Helvetica", 8)
        self.setFillColor(TEXT_MUTED)
        self.drawString(50, 30, "Confidential • Women Empowerment, Safety Technology & Crisis Intervention")
        page_label = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(562, 30, page_label)

        self.restoreState()


def create_card(title, subtitle, body_paragraphs, accent_color, bg_color, width=512):
    """Creates a modern card flowable with colored left accent border and comfortable padding."""
    content = []
    if title:
        content.append(Paragraph(f"<b>{title}</b>", ParagraphStyle(
            "CardTitle", fontName="Helvetica-Bold", fontSize=10.5, leading=14, textColor=accent_color, spaceAfter=2
        )))
    if subtitle:
        content.append(Paragraph(subtitle, ParagraphStyle(
            "CardSub", fontName="Helvetica", fontSize=8.5, leading=12, textColor=TEXT_MUTED, spaceAfter=4
        )))
    for p in body_paragraphs:
        content.append(Paragraph(p, ParagraphStyle(
            "CardBody", fontName="Helvetica", fontSize=9, leading=13.5, textColor=TEXT_MAIN, spaceAfter=3
        )))

    card_table = Table([[content]], colWidths=[width])
    card_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_color),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('LINEBEFORE', (0,0), (0,-1), 4, accent_color),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    return card_table


def build_polished_pdf(filename="Women_Safety_And_Support_App_Detailed_Documentation.pdf"):
    # Usable width: 612 - 50*2 = 512 pt
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    s_title = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=26,
        leading=30,
        textColor=PRIMARY_DARK,
        spaceAfter=5
    )

    s_tagline = ParagraphStyle(
        "CoverTagline",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11.5,
        leading=16,
        textColor=TEXT_MUTED,
        spaceAfter=14
    )

    s_h1 = ParagraphStyle(
        "Heading1_Modern",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=PRIMARY_DARK,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    s_h2 = ParagraphStyle(
        "Heading2_Modern",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=TEXT_MAIN,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    s_body = ParagraphStyle(
        "Body_Modern",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=13.8,
        textColor=TEXT_MAIN,
        spaceAfter=5
    )

    s_bullet = ParagraphStyle(
        "Bullet_Modern",
        parent=s_body,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )

    s_th = ParagraphStyle(
        "TableHead",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=WHITE
    )

    s_td = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=TEXT_MAIN
    )

    s_td_bold = ParagraphStyle(
        "TableCellBold",
        parent=s_td,
        fontName="Helvetica-Bold"
    )

    s_code = ParagraphStyle(
        "CodeText",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0F172A")
    )

    elements = []

    # =========================================================================
    # PAGE 1: ELEGANT COVER PAGE
    # =========================================================================
    elements.append(Spacer(1, 10))

    # Top Pill Badge
    top_badge = Table(
        [[Paragraph("<b>COMPREHENSIVE PRODUCT OVERVIEW & ARCHITECTURE GUIDE</b>", ParagraphStyle(
            "BadgeStyle", fontName="Helvetica-Bold", fontSize=8.5, textColor=PRIMARY
        ))]],
        colWidths=[512]
    )
    top_badge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_PURPLE),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#DDD6FE")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    elements.append(top_badge)
    elements.append(Spacer(1, 12))

    # Title & Subtitle
    elements.append(Paragraph("Women Safety & Support Application", s_title))
    elements.append(Paragraph("<font color='#5B34E6'><b>Project Adhira</b></font> — A Unified Ecosystem for Emergency Response, AI Legal Guidance & Community Care", s_tagline))

    # 4 Highlights Stat Cards
    stat_cards = [
        [
            Paragraph("<b>EMERGENCY SOS</b><br/><font size=7 color='#64748B'>Instant GPS & SMS Alert</font>", ParagraphStyle("Sc1", fontName="Helvetica", fontSize=8, leading=11, alignment=1, textColor=ACCENT_RED)),
            Paragraph("<b>ADHIRA AI</b><br/><font size=7 color='#64748B'>Legal & Crisis Assistant</font>", ParagraphStyle("Sc2", fontName="Helvetica", fontSize=8, leading=11, alignment=1, textColor=ACCENT_PURPLE)),
            Paragraph("<b>VERIFIED VOLUNTEERS</b><br/><font size=7 color='#64748B'>Voter ID & NGO Vetted</font>", ParagraphStyle("Sc3", fontName="Helvetica", fontSize=8, leading=11, alignment=1, textColor=ACCENT_GREEN)),
            Paragraph("<b>SAFE FORUM</b><br/><font size=7 color='#64748B'>Zero-Shot AI Moderation</font>", ParagraphStyle("Sc4", fontName="Helvetica", fontSize=8, leading=11, alignment=1, textColor=ACCENT_BLUE)),
        ]
    ]
    stat_table = Table(stat_cards, colWidths=[128, 128, 128, 128])
    stat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), BG_RED),
        ('BACKGROUND', (1,0), (1,0), BG_PURPLE),
        ('BACKGROUND', (2,0), (2,0), BG_GREEN),
        ('BACKGROUND', (3,0), (3,0), BG_BLUE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    elements.append(stat_table)
    elements.append(Spacer(1, 12))

    # Metadata Grid
    meta_rows = [
        [Paragraph("<b>Target Operating Systems:</b> Web, Windows, Android, iOS", s_td),
         Paragraph("<b>Release State:</b> Stable Production v1.0.0+1 (Oct 2026)", s_td)],
        [Paragraph("<b>Frontend Framework:</b> Flutter 3 (Material Design 3)", s_td),
         Paragraph("<b>Backend Architecture:</b> Node.js, Express 5, MongoDB", s_td)],
        [Paragraph("<b>AI Infrastructure:</b> Groq (LLaMA 3.1 8B) & Google Gemini", s_td),
         Paragraph("<b>Security & Auth:</b> JWT Auth, Bcrypt, Voter ID Verification", s_td)],
    ]
    meta_tbl = Table(meta_rows, colWidths=[256, 256])
    meta_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(meta_tbl)
    elements.append(Spacer(1, 12))

    # Executive Summary Card
    exec_p = (
        "<b>Executive Summary:</b> Project Adhira bridges acute emergency response with sustained post-crisis support. "
        "Unlike conventional safety apps that only offer a raw panic buzzer, Adhira delivers an integrated continuum of care: "
        "one-tap satellite GPS tracking and cellular SMS broadcast, an on-demand verified volunteer network, an AI-moderated "
        "community feed, and 'Adhira'—a 24/7 empathetic conversational companion specialized in Indian legal statutes (IPC & Bharatiya "
        "Nyaya Sanhita - BNS) and crisis de-escalation in regional languages. Built on Flutter and Express 5, the platform ensures "
        "privacy, zero-toxicity auto-quarantine, and verified human intervention."
    )
    elements.append(create_card("Executive Mission & Solution Overview", None, [exec_p], PRIMARY, BG_PURPLE))
    elements.append(Spacer(1, 12))

    # Document Outline Box
    toc_rows = [
        [Paragraph("<b>DOCUMENT OUTLINE & ROADMAP</b>", s_th), Paragraph("", s_th)],
        [Paragraph("<b>1. The Core Problem & The 4 Architectural Pillars</b>", s_td_bold), Paragraph("Systemic safety gaps, care continuum, demographic reach", s_td)],
        [Paragraph("<b>2. End-to-End System Architecture & Tech Stack</b>", s_td_bold), Paragraph("Flutter client, Express 5 API, MongoDB, Groq & Gemini services", s_td)],
        [Paragraph("<b>3. Emergency SOS & Telemetric Dispatch Engine</b>", s_td_bold), Paragraph("Satellite GPS, native cellular SMS intent, 112/1091 dialers", s_td)],
        [Paragraph("<b>4. 'Adhira' AI Legal & Safety Conversational Companion</b>", s_td_bold), Paragraph("LLaMA 3.1 8B, Gemini failover, IPC/BNS rights, empathetic tone", s_td)],
        [Paragraph("<b>5. Community Feed & Verified Volunteer Network</b>", s_td_bold), Paragraph("Zero-shot AI moderation, Voter ID vetting, 1-on-1 private rooms", s_td)],
        [Paragraph("<b>6. Database Schemas, Security & Quick Start Guide</b>", s_td_bold), Paragraph("MongoDB models, privacy rules, PowerShell launcher, v2.0 roadmap", s_td)],
    ]
    toc_tbl = Table(toc_rows, colWidths=[240, 272])
    toc_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_DARK),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(toc_tbl)

    elements.append(PageBreak())

    # =========================================================================
    # PAGE 2: THE PROBLEM & 4 PILLARS
    # =========================================================================
    elements.append(Paragraph("1. The Core Problem & The Four Pillars", s_h1))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph(
        "Women frequently encounter acute physical vulnerabilities during commutes, at workplaces, and within domestic spheres. "
        "Standard safety applications fail to address these realities due to four critical architectural flaws:",
        s_body
    ))
    elements.append(Paragraph("• <b>Single-Point Failure of 'Panic Buzzers':</b> Conventional SOS apps only transmit a raw coordinate text without providing guidance on what to do during or after the incident.", s_bullet))
    elements.append(Paragraph("• <b>Severe Legal Information Gap:</b> Victims of stalking, domestic harassment, or cyberbullying often do not know that Indian law mandates <i>Zero FIR</i>, or how to invoke Section 354 IPC / BNS protections.", s_bullet))
    elements.append(Paragraph("• <b>Lack of Trusted Civilian Intermediaries:</b> Victims hesitate to approach unverified strangers online without verified credentials, NGO affiliations, or peer ratings.", s_bullet))
    elements.append(Paragraph("• <b>Isolation & Retaliation Fears:</b> Survivors of abuse fear retaliation if they post publicly, lacking secure spaces to share anonymously without toxicity.", s_bullet))

    elements.append(Paragraph("The Four Architectural Pillars of Adhira:", s_h2))

    # 4 Pillars as 2x2 Clean Cards
    p1 = "<b>Pillar 1: Emergency SOS Telematics</b><br/>Immediate satellite GPS coordinate capture, persistent cloud audit logging, native SMS broadcast with direct Google Maps hyperlinks to trusted contacts, and 112/1091 dialer escalation."
    p2 = "<b>Pillar 2: 'Adhira' AI Legal & Safety Guide</b><br/>Sub-400ms conversational LLM (Groq LLaMA 3.1 8B with Gemini failover). Educates users on Indian legal statutes, de-escalates panic, and maintains an empathetic sisterly tone."
    p3 = "<b>Pillar 3: Verified Volunteer Network</b><br/>Govt. Voter ID verified civilian and NGO volunteers. Features real-time Active/Inactive availability switches, skill matching, and 1-on-1 private guidance rooms."
    p4 = "<b>Pillar 4: Safe Community & Grievance AI</b><br/>Anonymous story sharing with zero-shot Gemini multimodal AI moderation: classifies urgency (green/yellow/red), tags domain categories, and auto-quarantines toxic content."

    pillar_grid = [
        [create_card(None, None, [p1], ACCENT_RED, BG_RED, width=250),
         create_card(None, None, [p2], ACCENT_PURPLE, BG_PURPLE, width=250)],
        [create_card(None, None, [p3], ACCENT_GREEN, BG_GREEN, width=250),
         create_card(None, None, [p4], ACCENT_BLUE, BG_BLUE, width=250)],
    ]
    p_grid_table = Table(pillar_grid, colWidths=[256, 256])
    p_grid_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(p_grid_table)
    elements.append(Spacer(1, 4))

    elements.append(Paragraph("Target Demographics & Operational Impact Matrix:", s_h2))
    demo_data = [
        [Paragraph("<b>User Demographic</b>", s_th), Paragraph("<b>Key Vulnerabilities Faced</b>", s_th), Paragraph("<b>Platform Solutions Provided</b>", s_th)],
        [
            Paragraph("<b>Solo Commuters & Students</b>", s_td_bold),
            Paragraph("Late-night travel, unfamiliar transit routes, cab harassment, street stalking risks.", s_td),
            Paragraph("One-tap SOS, live Google Maps SMS broadcast, trusted emergency contact circle.", s_td)
        ],
        [
            Paragraph("<b>Domestic Abuse Survivors</b>", s_td_bold),
            Paragraph("Coercive control, physical isolation, lack of legal rights awareness.", s_td),
            Paragraph("Adhira legal advisor (PWDVA, IPC 498A), verified NGO volunteer private sessions.", s_td)
        ],
        [
            Paragraph("<b>Workplace & Cyber Victims</b>", s_td_bold),
            Paragraph("Stalking, online defamation, workplace harassment under POSH Act.", s_td),
            Paragraph("Anonymous community posting, AI grievance classification, legal rights guidance.", s_td)
        ],
        [
            Paragraph("<b>Social Workers & Volunteers</b>", s_td_bold),
            Paragraph("Coordination bottlenecks, lack of structured verification, volunteer burnout.", s_td),
            Paragraph("Availability switch, ticket triage dashboard, verified badges, rating metrics.", s_td)
        ]
    ]
    demo_tbl = Table(demo_data, colWidths=[130, 192, 190])
    demo_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(demo_tbl)

    elements.append(PageBreak())

    # =========================================================================
    # PAGE 3: SYSTEM ARCHITECTURE & TECH STACK
    # =========================================================================
    elements.append(Paragraph("2. System Architecture & Technology Stack", s_h1))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph(
        "Project Adhira is engineered on a resilient, decoupled client-server architecture. "
        "A single, responsive Flutter codebase serves Web, Windows Desktop, and Mobile clients, connecting to "
        "a high-throughput Express 5 REST API gateway and intelligent cloud AI microservices.",
        s_body
    ))

    # Architecture Visual Flow Block
    arch_box_data = [
        [Paragraph("<b>CROSS-PLATFORM FRONTEND CLIENT (Flutter 3.x / Dart)</b><br/>"
                   "<font size=7.5 color='#475569'>Responsive User Shell • Volunteer Dashboard • Material 3 UI • Provider Polling • Device GPS Telematics</font>",
                   ParagraphStyle("A1", fontName="Helvetica", fontSize=9, leading=12, alignment=1, textColor=PRIMARY_DARK))],
        [Paragraph("▼   <b>HTTPS / Secure REST API Gateway (JSON)</b>   ▼",
                   ParagraphStyle("AArr", fontName="Helvetica-Bold", fontSize=8, leading=10, alignment=1, textColor=TEXT_MUTED))],
        [Paragraph("<b>BACKEND MICRO-SERVICES & BUSINESS LOGIC (Node.js & Express 5.2)</b><br/>"
                   "<font size=7.5 color='#475569'>JWT Role Guard • SOS Dispatcher • Volunteer Triage • Session Router • Grievance Controller</font>",
                   ParagraphStyle("A2", fontName="Helvetica", fontSize=9, leading=12, alignment=1, textColor=PRIMARY_DARK))],
        [
            Table([
                [
                    Paragraph("<b>MongoDB Store</b><br/><font size=7 color='#64748B'>Users, SOS Logs, Posts, Chat Sessions</font>", ParagraphStyle("D1", fontName="Helvetica", fontSize=7.5, leading=10, alignment=1)),
                    Paragraph("<b>Groq AI Engine</b><br/><font size=7 color='#64748B'>LLaMA 3.1 8B Sub-400ms Inference</font>", ParagraphStyle("D2", fontName="Helvetica", fontSize=7.5, leading=10, alignment=1)),
                    Paragraph("<b>Google Gemini</b><br/><font size=7 color='#64748B'>Zero-Shot Grievance & Web Grounding</font>", ParagraphStyle("D3", fontName="Helvetica", fontSize=7.5, leading=10, alignment=1)),
                    Paragraph("<b>Device Hardware</b><br/><font size=7 color='#64748B'>GPS Satellites & Native SMS Telephony</font>", ParagraphStyle("D4", fontName="Helvetica", fontSize=7.5, leading=10, alignment=1)),
                ]
            ], colWidths=[124, 124, 124, 124])
        ]
    ]
    arch_box_table = Table(arch_box_data, colWidths=[512])
    arch_box_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_PURPLE),
        ('BACKGROUND', (0,1), (-1,1), WHITE),
        ('BACKGROUND', (0,2), (-1,2), BG_LIGHT),
        ('BACKGROUND', (0,3), (-1,3), WHITE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    elements.append(arch_box_table)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Technology Specifications & Dependency Matrix:", s_h2))
    tech_rows = [
        [Paragraph("<b>Component Layer</b>", s_th), Paragraph("<b>Libraries & Frameworks</b>", s_th), Paragraph("<b>Key Responsibilities</b>", s_th)],
        [
            Paragraph("<b>Frontend Client</b>", s_td_bold),
            Paragraph("• Flutter 3.2.0+ (Dart)<br/>• <code>provider: ^6.1.2</code><br/>• <code>geolocator: ^12.0.0</code><br/>• <code>url_launcher: ^6.3.2</code><br/>• <code>image_picker: ^1.1.2</code>", s_td),
            Paragraph("Cross-platform responsive shells for Seekers and Volunteers. Manages background notification polling, device GPS interrogation, and telephony SMS triggers.", s_td)
        ],
        [
            Paragraph("<b>Backend Server</b>", s_td_bold),
            Paragraph("• Node.js & Express 5.2.1<br/>• <code>mongoose: ^9.4.1</code><br/>• <code>jsonwebtoken: ^9.0.3</code><br/>• <code>bcryptjs: ^3.0.3</code><br/>• <code>cors: ^2.8.6</code>", s_td),
            Paragraph("Stateless REST API gateway. Implements password encryption, JWT issuance, role-based route guardrails, 50MB media payload handling, and AI request orchestration.", s_td)
        ],
        [
            Paragraph("<b>Database</b>", s_td_bold),
            Paragraph("• MongoDB 6+ / Atlas<br/>• Docker Compose container<br/>• Mongoose ODM", s_td),
            Paragraph("Stores schemas for Users, Emergency Contacts, Verified Volunteers, SOS Events, Community Posts, Comments, and 1-on-1 Chat Sessions.", s_td)
        ],
        [
            Paragraph("<b>Cloud AI Services</b>", s_td_bold),
            Paragraph("• Groq Cloud (LLaMA 3.1 8B)<br/>• Google Gemini Flash & 2.5<br/>• Zero-shot Sentiment Engine<br/>• Gemini Search Grounding", s_td),
            Paragraph("Sub-second conversational generation for Adhira assistant; zero-shot multimodal grievance & toxicity classification; live search for safety articles.", s_td)
        ]
    ]
    tech_tbl = Table(tech_rows, colWidths=[100, 166, 246])
    tech_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_DARK),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(tech_tbl)

    elements.append(PageBreak())

    # =========================================================================
    # PAGE 4: EMERGENCY SOS & TELEMETRIC DISPATCH
    # =========================================================================
    elements.append(Paragraph("3. Emergency SOS & Telemetric Dispatch Engine", s_h1))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph(
        "The Emergency SOS subsystem is designed for deterministic execution under acute danger. "
        "When activated, the system executes a 4-phase parallel response that combines satellite telemetry, "
        "immutable cloud incident logging, and offline-resilient cellular SMS broadcast.",
        s_body
    ))

    # SOS 4 Phases
    sos_rows = [
        [Paragraph("<b>Response Phase</b>", s_th), Paragraph("<b>Action Taken</b>", s_th), Paragraph("<b>Technical & Operational Mechanism</b>", s_th)],
        [
            Paragraph("<b>Phase 1: Satellite Geocoding</b>", s_td_bold),
            Paragraph("Hardware GPS Interrogation", s_td),
            Paragraph("Queries device GPS hardware using <code>Geolocator.getCurrentPosition()</code> with high accuracy. Extracts latitude and longitude in milliseconds.", s_td)
        ],
        [
            Paragraph("<b>Phase 2: Cloud Incident Logging</b>", s_td_bold),
            Paragraph("Secure POST to <code>/api/sos</code>", s_td),
            Paragraph("Transmits coordinates, timestamp, and distress notes to MongoDB. Creates a permanent forensic record for responder auditing.", s_td)
        ],
        [
            Paragraph("<b>Phase 3: Cellular SMS Dispatch</b>", s_td_bold),
            Paragraph("Native OS SMS Broadcast", s_td),
            Paragraph("Compiles all registered emergency contacts into comma-separated recipient strings. Sends a direct Google Maps link: <code>https://maps.google.com/?q={lat},{lng}</code> via native cellular radio even if mobile data is lost.", s_td)
        ],
        [
            Paragraph("<b>Phase 4: Hotline Escalation</b>", s_td_bold),
            Paragraph("Telephony Shortcuts", s_td),
            Paragraph("Surfaces immediate one-tap dialers for national emergency helplines: <b>112</b> (Unified National Emergency) and <b>1091</b> (Women Helpline).", s_td)
        ]
    ]
    sos_tbl = Table(sos_rows, colWidths=[116, 150, 246])
    sos_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), ACCENT_RED),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('LINEBEFORE', (0,1), (0,-1), 3.5, ACCENT_RED),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(sos_tbl)
    elements.append(Spacer(1, 8))

    elements.append(Paragraph("Emergency Circles & Offline Cellular Resilience Rationale:", s_h2))
    elements.append(Paragraph(
        "Users can configure an unlimited list of trusted emergency contacts (name and phone number) in their profile. "
        "In crisis situations, mobile data (4G/5G) often drops in basements, transit tunnels, or remote roads. "
        "By packaging the distress message and Google Maps location into a standard <b>telephony SMS intent</b>, "
        "Project Adhira ensures the emergency beacon is dispatched through base cellular signaling without depending on internet access.",
        s_body
    ))

    # Real-World Incident Preview Card
    sms_mockup = (
        "<b>Automated Cellular Distress SMS (Delivered to Emergency Contacts):</b><br/>"
        "<i>\"🚨 SOS EMERGENCY! I need help. My location: https://maps.google.com/?q=28.6139,77.2090. Feeling unsafe near Central Metro station.\"</i><br/><br/>"
        "• <b>Direct Action:</b> Recipients can tap the link to open live turn-by-turn navigation directly to the user's coordinates.<br/>"
        "• <b>Zero Internet Reliance:</b> The SMS is transmitted via native cellular baseband even when WiFi and mobile data are disconnected."
    )
    elements.append(create_card("Live Telemetric SMS Dispatch Format", None, [sms_mockup], ACCENT_RED, BG_RED))
    elements.append(Spacer(1, 8))

    # Forensic Incident Trail
    sos_highlight = (
        "<b>Forensic Incident Audit Trail:</b> Every SOS trigger creates an immutable entry in MongoDB. "
        "This chronological record stores exact GPS coordinates, timestamps, and notes, providing formal documentation "
        "that can be presented to police investigators or legal counsel to establish the timeline of an assault or stalking event."
    )
    elements.append(create_card("Forensic Reliability & Legal Protection", None, [sos_highlight], PRIMARY, BG_LIGHT))

    elements.append(PageBreak())

    # =========================================================================
    # PAGE 5: ADHIRA AI LEGAL & SAFETY ASSISTANT
    # =========================================================================
    elements.append(Paragraph("4. 'Adhira' Intelligent AI Safety & Legal Assistant", s_h1))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph(
        "<b>Adhira</b> is an autonomous AI conversational companion built into the application. "
        "Configured with a distinct persona of a <i>'caring elder sister who knows the law'</i>, Adhira de-escalates panic, "
        "explains statutory rights in simple everyday language, and provides step-by-step guidance without legal jargon.",
        s_body
    ))

    elements.append(Paragraph("Resilient Dual-Engine AI Cascade:", s_h2))
    elements.append(Paragraph(
        "To ensure 99.9% uptime during emergencies, the chatbot backend implements an intelligent fallback cascade:",
        s_body
    ))
    elements.append(Paragraph("• <b>Primary Engine (Groq LLaMA 3.1 8B):</b> Delivers blazing sub-400ms inference with low temperature (0.3) for concise, supportive, and factually grounded advice.", s_bullet))
    elements.append(Paragraph("• <b>Secondary Engine (Google Gemini Flash):</b> Automatically engaged if Groq hits rate limits, network outages, or key exhaustion.", s_bullet))
    elements.append(Paragraph("• <b>Tertiary Deterministic Net:</b> Built-in keyword heuristics return pre-compiled helpline actions if all cloud services fail.", s_bullet))

    elements.append(Paragraph("Statutory Protections & Indian Legal Knowledge Base:", s_h2))
    legal_rows = [
        [Paragraph("<b>Statutory Protection</b>", s_th), Paragraph("<b>Key Provisions Covered</b>", s_th), Paragraph("<b>How Adhira Advises the User</b>", s_th)],
        [
            Paragraph("<b>Zero FIR Mandate</b>", s_td_bold),
            Paragraph("Sec 154 CrPC / BNSS provisions", s_td),
            Paragraph("Clarifies that any police station must register an FIR for cognizable crimes regardless of jurisdiction, without redirecting the victim.", s_td)
        ],
        [
            Paragraph("<b>Molestation & Stalking</b>", s_td_bold),
            Paragraph("IPC Sec 354, 354A, 354D / BNS Equiv.", s_td),
            Paragraph("Explains elements required to prove electronic/physical stalking, evidence gathering steps (call logs, screenshots), and non-bailable clauses.", s_td)
        ],
        [
            Paragraph("<b>Domestic Violence Act</b>", s_td_bold),
            Paragraph("PWDVA 2005 & IPC Sec 498A (Cruelty)", s_td),
            Paragraph("Outlines immediate Protection Orders, Right to Reside in shared households, and how to reach Protection Officers and recognized NGOs.", s_td)
        ],
        [
            Paragraph("<b>Cyber Crimes & Anonymity</b>", s_td_bold),
            Paragraph("IT Act Sec 66E, 67, 67A & Helpline 1930", s_td),
            Paragraph("Provides clear instructions on filing complaints for non-consensual image sharing, online blackmail, and reporting to National Cyber Crime portal.", s_td)
        ]
    ]
    legal_tbl = Table(legal_rows, colWidths=[120, 160, 232])
    legal_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_DARK),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(legal_tbl)
    elements.append(Spacer(1, 8))

    # Real Dialogue Example Card
    chat_dialogue = (
        "<b>Sample Conversation with Adhira (Empathetic & Legal Guidance):</b><br/>"
        "<b>User:</b> <i>\"Someone has been following me from the metro station for the last 3 days and taking photos. What can I do?\"</i><br/>"
        "<b>Adhira:</b> <i>\"I hear you, and you are not alone. First, please ensure you are in a crowded, well-lit place right now. "
        "What this person is doing is a serious crime under Section 354D of the Indian Penal Code (Stalking). "
        "You have the right to file an FIR at any police station without delay (Zero FIR). "
        "Here are three immediate steps: 1) Call 112 or share your live location with a trusted contact. "
        "2) Note down their vehicle number or appearance safely. 3) You can also connect with one of our verified legal volunteers right here in the app. "
        "Stay strong, I am here with you. 💕\"</i>"
    )
    elements.append(create_card("Conversational Persona & Anti-Victim Blaming Guardrail", None, [chat_dialogue], ACCENT_PURPLE, BG_PURPLE))

    elements.append(PageBreak())

    # =========================================================================
    # PAGE 6: COMMUNITY & VOLUNTEER NETWORK
    # =========================================================================
    elements.append(Paragraph("5. Community Forum & Verified Volunteer Network", s_h1))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph(
        "Project Adhira's Community & Guidance subsystems transform isolated victims into supported community members. "
        "Every post on the public feed is monitored by <b>Zero-Shot Multimodal Gemini AI</b>, while the Volunteer ecosystem "
        "connects seekers to vetted human advocates.",
        s_body
    ))

    # Grievance & Moderation Table
    griev_rows = [
        [Paragraph("<b>AI Metric</b>", s_th), Paragraph("<b>Triage Level</b>", s_th), Paragraph("<b>System Action & Feed Behavior</b>", s_th)],
        [
            Paragraph("<b>Urgency Level</b>", s_td_bold),
            Paragraph("<font color='#059669'><b>Green (Normal)</b></font>", s_td),
            Paragraph("General stories, advice, safety questions. Rendered with green badge.", s_td)
        ],
        [
            Paragraph("", s_td),
            Paragraph("<font color='#D97706'><b>Yellow (Distress)</b></font>", s_td),
            Paragraph("Emotional pain, anxiety, seeking advice. Highlighted to volunteers for rapid support.", s_td)
        ],
        [
            Paragraph("", s_td),
            Paragraph("<font color='#DC2626'><b>Red (Crisis)</b></font>", s_td),
            Paragraph("Active physical abuse, severe danger. Triggers automated prompt to user with SOS button.", s_td)
        ],
        [
            Paragraph("<b>Toxicity Moderation</b>", s_td_bold),
            Paragraph("<b>High Toxicity</b>", s_td_bold),
            Paragraph("<b>Auto-Quarantine:</b> Immediately flagged, soft-deleted (<code>isDeleted: true</code>), and hidden with notice: <i>'Deleted due to unethical content'</i>.", s_td)
        ],
        [
            Paragraph("<b>Domain Tagging</b>", s_td_bold),
            Paragraph("<b>Domain Tags</b>", s_td),
            Paragraph("Auto-classified: <i>Harassment, Domestic Violence, Stalking, Mental Health, Workplace Safety</i>.", s_td)
        ]
    ]
    griev_tbl = Table(griev_rows, colWidths=[110, 116, 286])
    griev_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(griev_tbl)
    elements.append(Spacer(1, 8))

    elements.append(Paragraph("Verified Volunteer Lifecycle & 1-on-1 Private Sessions:", s_h2))

    vol_p = (
        "• <b>Voter ID Verification:</b> Volunteers submit Govt. Voter ID credentials, phone, address, and NGO affiliations. Verified profiles display a verified badge.<br/>"
        "• <b>Availability Toggle:</b> Volunteers can toggle between <b>Active</b> and <b>Inactive</b> status. Only active volunteers appear in urgent search suggestions.<br/>"
        "• <b>1-on-1 Private Chat Sessions:</b> Seekers can request private guidance from a specific volunteer. When accepted, a private encrypted chat room is spun up.<br/>"
        "• <b>Ratings & Accountability:</b> Users submit 1-5 star ratings, written reviews, hours spent, and people helped, building a transparent track record."
    )
    elements.append(create_card("Verified Volunteer Ecosystem & Accountability", None, [vol_p], ACCENT_GREEN, BG_GREEN))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph("Companion Safety Apps Directory & Live AI Blogs:", s_h2))
    elements.append(Paragraph(
        "The app includes a curated directory linking directly to specialized safety utilities: <i>bSafe</i> (live tracking), "
        "<i>Raksha</i> (hardware volume SOS), <i>Himmat</i> (police direct video dispatch), <i>Circle of 6</i> (discreet group alerts), "
        "<i>My Safetipin</i> (street lighting safety audits), and <i>Shake2Safety</i> (haptic shake trigger). "
        "Additionally, the 'Know Your Community' tab pulls live, authentic blogs on women's legal rights and self-defense using Gemini Google Search Grounding.",
        s_body
    ))

    elements.append(PageBreak())

    # =========================================================================
    # PAGE 7: DATABASE SCHEMAS, SECURITY & DEPLOYMENT
    # =========================================================================
    elements.append(Paragraph("6. Database Schemas, Security & Quick Start Guide", s_h1))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph("Core Database Schemas (MongoDB / Mongoose):", s_h2))
    db_rows = [
        [Paragraph("<b>Collection</b>", s_th), Paragraph("<b>Key Attributes & Schema Fields</b>", s_th), Paragraph("<b>Operational Function</b>", s_th)],
        [
            Paragraph("<b>User</b>", s_td_bold),
            Paragraph("<code>name, email, password, googleId, role ('user'|'volunteer'), voterIdVerified, volunteerAvailability, emergencyContacts, ratings, followers, following</code>", ParagraphStyle("C1", fontName="Courier", fontSize=7.5, leading=9.5)),
            Paragraph("Stores profile credentials, emergency contacts, volunteer ratings, and mutual follow permissions.", s_td)
        ],
        [
            Paragraph("<b>HelpRequest</b>", s_td_bold),
            Paragraph("<code>requesterId, volunteerId, sosId, message, assistanceNote, hoursSpent, peopleHelped, rating (1-5), status ('pending'|'accepted'|'completed')</code>", ParagraphStyle("C2", fontName="Courier", fontSize=7.5, leading=9.5)),
            Paragraph("Tracks guidance ticket lifecycle, assigned volunteers, and resolution metrics.", s_td)
        ],
        [
            Paragraph("<b>Post</b>", s_td_bold),
            Paragraph("<code>userId, content, mediaUrl, mediaType ('text'|'image'|'audio'), isAnonymous, distressLevel, urgencyColor, toxicityLevel, isDeleted, likes</code>", ParagraphStyle("C3", fontName="Courier", fontSize=7.5, leading=9.5)),
            Paragraph("Community feed entries with AI sentiment tags and soft-delete quarantine flags.", s_td)
        ],
        [
            Paragraph("<b>PrivateChat</b>", s_td_bold),
            Paragraph("<code>Session: { helpSeekerId, volunteerId, status }</code><br/><code>Message: { sessionId, senderId, content, urgencyColor, toxicityLevel }</code>", ParagraphStyle("C4", fontName="Courier", fontSize=7.5, leading=9.5)),
            Paragraph("1-on-1 private messaging exchange between seeker and volunteer.", s_td)
        ],
        [
            Paragraph("<b>SOS Logs</b>", s_td_bold),
            Paragraph("<code>userId, location: { lat: Number, lng: Number }, notes, timestamps</code>", ParagraphStyle("C5", fontName="Courier", fontSize=7.5, leading=9.5)),
            Paragraph("Permanent historical audit log of emergency incidents.", s_td)
        ]
    ]
    db_tbl = Table(db_rows, colWidths=[86, 260, 166])
    db_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_DARK),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(db_tbl)
    elements.append(Spacer(1, 8))

    elements.append(Paragraph("Security, Privacy & Data Minimization:", s_h2))
    elements.append(Paragraph(
        "• <b>Anonymous Identity:</b> Survivors can post and seek help anonymously; real identity fields are scrubbed from feed payloads.<br/>"
        "• <b>Zero-Exposure Profiles:</b> Passwords (salted Bcrypt), voter IDs, and emergency contact phones are strictly omitted from public API queries.<br/>"
        "• <b>Follow Request System:</b> Prevents unwanted stalking between platform users by requiring explicit approval before profile visibility.",
        s_body
    ))

    elements.append(Paragraph("Quick Start & Execution Guide (PowerShell):", s_h2))
    qs_code = (
        "<b># 1. Quick Automated Launch:</b> powershell -ExecutionPolicy Bypass -File .\\run-windows.ps1 -Port 5000<br/>"
        "<b># 2. Run Backend Manually:</b> cd Backend &amp;&amp; npm install &amp;&amp; $env:PORT=5000 &amp;&amp; npm run dev<br/>"
        "<b># 3. Seed Default Admin (admin/admin):</b> cd Backend &amp;&amp; npm run seed:admin<br/>"
        "<b># 4. Run Flutter Client (Web):</b> cd frontend &amp;&amp; flutter pub get &amp;&amp; flutter run -d chrome --dart-define=API_BASE_URL=http://127.0.0.1:5000"
    )
    qs_card = Table([[Paragraph(qs_code, ParagraphStyle("QSC", fontName="Courier", fontSize=7.5, leading=10.5, textColor=colors.HexColor("#0F172A")))]], colWidths=[512])
    qs_card.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(qs_card)
    elements.append(Spacer(1, 6))

    elements.append(Paragraph("Future Strategic Roadmap (v2.0):", s_h2))
    elements.append(Paragraph(
        "• <b>Acoustic Distress & Scream Detection:</b> On-device ML listening in background for scream acoustics or distress voice triggers.<br/>"
        "• <b>BLE Mesh Networking:</b> Peer-to-peer relaying of SOS beacons across nearby devices even when cell data is completely disabled.<br/>"
        "• <b>Police ERSS 112 CAD Integration:</b> Direct API dispatch into State Police Computer-Aided Dispatch networks for immediate cruiser dispatch.",
        s_body
    ))

    # Build
    doc.build(elements, canvasmaker=ModernDocCanvas)
    print(f"SUCCESS: Generated {filename}")

if __name__ == "__main__":
    out_pdf = "Women_Safety_And_Support_App_Detailed_Documentation.pdf"
    if len(sys.argv) > 1:
        out_pdf = sys.argv[1]
    build_polished_pdf(out_pdf)
