import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

# Theme Palette
PRIMARY = colors.HexColor("#5B34E6")       # Brand Violet / Purple
PRIMARY_DARK = colors.HexColor("#371B96")  # Dark Violet
TEXT_MAIN = colors.HexColor("#121633")     # Primary Dark Navy
TEXT_MUTED = colors.HexColor("#555E7E")    # Slate Muted Text
BG_LIGHT = colors.HexColor("#F8F9FD")      # Clean Light Background
BG_SOFT_PURPLE = colors.HexColor("#F1ECFF")# Soft Purple Accent
ACCENT_RED = colors.HexColor("#DC284C")    # Emergency Red
ACCENT_GREEN = colors.HexColor("#128751")  # Volunteer Green
ACCENT_AMBER = colors.HexColor("#D97706")  # Warning Amber
ACCENT_BLUE = colors.HexColor("#1D4ED8")   # Info Blue
BORDER_COLOR = colors.HexColor("#D9DFEF")  # Elegant border
CODE_BG = colors.HexColor("#0F172A")       # Dark code block background
WHITE = colors.HexColor("#FFFFFF")

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print 'Page X of Y' 
    and standard running headers and footers on all pages except the cover page.
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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress running header/footer on cover page

        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(TEXT_MUTED)

        # Header
        self.drawString(48, 752, "PROJECT ADHIRA — WOMEN SAFETY & SUPPORT APPLICATION")
        self.drawRightString(564, 752, "SYSTEM ARCHITECTURE & FEATURE GUIDE")
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.6)
        self.line(48, 746, 564, 746)

        # Footer
        self.setFont("Helvetica", 7.5)
        self.drawString(48, 34, "Confidential • Women Empowerment, Safety Technology & Crisis Intervention")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(564, 34, page_str)
        self.line(48, 42, 564, 42)

        self.restoreState()


def build_pdf(filename="Women_Safety_And_Support_App_Detailed_Documentation.pdf"):
    # Target 516 pt usable width: 612 - 48*2 = 516 pt
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=48,
        rightMargin=48,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    # Custom styles
    p_title = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=6
    )

    p_sub = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11.5,
        leading=16,
        textColor=TEXT_MUTED,
        spaceAfter=14
    )

    h1 = ParagraphStyle(
        "H1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=17,
        textColor=PRIMARY_DARK,
        spaceBefore=0,
        spaceAfter=4,
        keepWithNext=True
    )

    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=TEXT_MAIN,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12.2,
        textColor=TEXT_MAIN,
        spaceAfter=5
    )

    bullet = ParagraphStyle(
        "Bullet",
        parent=body,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    callout = ParagraphStyle(
        "Callout",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=12.5,
        textColor=TEXT_MAIN
    )

    tbl_hdr = ParagraphStyle(
        "TableHdr",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10.5,
        textColor=WHITE
    )

    tbl_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.8,
        leading=10.5,
        textColor=TEXT_MAIN
    )

    tbl_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=tbl_cell,
        fontName="Helvetica-Bold"
    )

    code_txt = ParagraphStyle(
        "CodeText",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor("#E2E8F0")
    )

    elements = []

    # =========================================================================
    # PAGE 1: COVER & EXECUTIVE SUMMARY
    # =========================================================================
    elements.append(Spacer(1, 10))
    badge = Table([[Paragraph("<b>PROJECT COMPREHENSIVE ARCHITECTURE & SYSTEM GUIDE • RELEASE v1.0</b>", ParagraphStyle(
        "B", fontName="Helvetica-Bold", fontSize=8, textColor=PRIMARY
    ))]], colWidths=[516])
    badge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_SOFT_PURPLE),
        ('PADDING', (0,0), (-1,-1), 6),
        ('LINEBEFORE', (0,0), (0,-1), 4, PRIMARY),
    ]))
    elements.append(badge)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Women Safety and Support Application<br/><b>Project Adhira</b>", p_title))
    elements.append(Paragraph(
        "An AI-grounded, multi-tiered digital safety ecosystem uniting emergency telemetric response, "
        "verified human volunteer networks, legal guidance, and community solidarity.",
        p_sub
    ))

    # Meta Table
    m_data = [
        [Paragraph("<b>Document Purpose:</b> Full Architectural & Feature Specification", tbl_cell),
         Paragraph("<b>Date of Publication:</b> October 2026", tbl_cell)],
        [Paragraph("<b>Target Operating Systems:</b> Web, Windows, Android, iOS, macOS", tbl_cell),
         Paragraph("<b>Application Status:</b> Stable Production v1.0.0+1", tbl_cell)],
        [Paragraph("<b>Frontend Framework:</b> Flutter 3 (Material Design 3 & Provider)", tbl_cell),
         Paragraph("<b>Backend Micro-Services:</b> Node.js, Express 5, MongoDB Mongoose", tbl_cell)],
        [Paragraph("<b>AI Engines:</b> Groq Cloud (LLaMA 3.1 8B Instant) & Google Gemini", tbl_cell),
         Paragraph("<b>Security & Auth:</b> JWT, Bcrypt, Google OAuth, Voter ID Verification", tbl_cell)],
    ]
    m_tbl = Table(m_data, colWidths=[258, 258])
    m_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(m_tbl)
    elements.append(Spacer(1, 10))

    # Executive Summary Card
    exec_text = (
        "<b>Executive Summary:</b> Project Adhira (Women Safety & Support App) addresses acute personal danger "
        "and systemic post-incident isolation through a unified multiplatform architecture. It bridges immediate "
        "physical safety through high-accuracy GPS tracking and SMS broadcast, with an on-demand verified volunteer corps, "
        "zero-shot AI grievance classification, 1-on-1 private counselling rooms, and 'Adhira'—a 24/7 empathetic conversational "
        "assistant offering guidance under Indian legal protections (IPC / Bharatiya Nyaya Sanhita - BNS) in regional languages. "
        "The system enforces strict zero-toxicity auto-quarantine, survivor anonymity, and complete audit logging."
    )
    exec_c = Table([[Paragraph(exec_text, callout)]], colWidths=[516])
    exec_c.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FAF9FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D8CCFC")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('LINEBEFORE', (0,0), (0,-1), 4, PRIMARY),
    ]))
    elements.append(exec_c)
    elements.append(Spacer(1, 10))

    # TOC
    toc_data = [
        [Paragraph("<b>TABLE OF CONTENTS</b>", tbl_hdr), Paragraph("<b>PAGES & COVERAGE</b>", tbl_hdr)],
        [Paragraph("<b>Section 1:</b> Executive Vision, Problem Statement & Four Pillars", tbl_cell_bold), Paragraph("Page 2 • Mission, systemic challenges, demographic reach", tbl_cell)],
        [Paragraph("<b>Section 2:</b> System Architecture & Technology Stack Breakdown", tbl_cell_bold), Paragraph("Page 3 • Multiplatform Flutter, Express 5, MongoDB, AI cloud", tbl_cell)],
        [Paragraph("<b>Section 3:</b> Emergency SOS & Telemetric Dispatch Protocol", tbl_cell_bold), Paragraph("Page 4 • GPS coordinates, SMS intent, 112/1091 integration", tbl_cell)],
        [Paragraph("<b>Section 4:</b> 'Adhira' Intelligent AI Safety & Legal Assistant", tbl_cell_bold), Paragraph("Page 5 • Groq + Gemini cascade, IPC/BNS, multilingual NLP", tbl_cell)],
        [Paragraph("<b>Section 5:</b> Community Forum & Zero-Shot AI Grievance Moderation", tbl_cell_bold), Paragraph("Page 6 • Urgency colors, toxicity quarantine, domain tagging", tbl_cell)],
        [Paragraph("<b>Section 6:</b> Verified Volunteer Network & 1-on-1 Private Guidance", tbl_cell_bold), Paragraph("Page 7 • Voter ID vetting, availability toggle, private sessions", tbl_cell)],
        [Paragraph("<b>Section 7:</b> Database Architecture & Core Mongoose Schemas", tbl_cell_bold), Paragraph("Page 8 • Schemas for Users, SOS, Posts, Chats, HelpTickets", tbl_cell)],
        [Paragraph("<b>Section 8:</b> Companion Safety Ecosystem & Real-Time AI Search", tbl_cell_bold), Paragraph("Page 9 • Safety app directory, Gemini search-grounded blogs", tbl_cell)],
        [Paragraph("<b>Section 9:</b> Setup, Deployment, API Reference & Strategic Roadmap", tbl_cell_bold), Paragraph("Page 10 • PowerShell scripts, .env configs, REST routes, v2.0", tbl_cell)],
    ]
    toc_tbl = Table(toc_data, colWidths=[290, 226])
    toc_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_DARK),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    elements.append(toc_tbl)

    elements.append(PageBreak())

    # =========================================================================
    # PAGE 2: 1. EXECUTIVE VISION, PROBLEM STATEMENT & FOUR PILLARS
    # =========================================================================
    elements.append(Paragraph("1. Executive Vision, Problem Statement & Four Pillars", h1))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph(
        "Across both public transit and private spaces, women frequently encounter acute hazards requiring split-second "
        "intervention, as well as complex legal and psychological aftermaths that standard law enforcement apps fail to address. "
        "Project Adhira directly tackles four systemic barriers:",
        body
    ))
    elements.append(Paragraph("• <b>Fragmented Emergency Tools:</b> Existing panic apps only send a single static alert, leaving the user with zero guidance or emotional grounding once the alert is fired.", bullet))
    elements.append(Paragraph("• <b>Information & Legal Asymmetry:</b> Victims of stalking, eve-teasing, or domestic harassment often do not know that police are required to register a <i>Zero FIR</i>, or how to invoke Section 354 IPC / BNS protections.", bullet))
    elements.append(Paragraph("• <b>Reluctance to Seek Unverified Help:</b> Survivors fear contacting strangers without identity guarantees, institutional backing, or past performance track records.", bullet))
    elements.append(Paragraph("• <b>Fear of Retaliation in Open Communities:</b> Trauma victims hesitate to share abuse narratives for fear of public exposure, victim blaming, or aggressive online harassment.", bullet))

    elements.append(Paragraph("The Four Core Architectural Pillars:", h2))
    p_data = [
        [
            Paragraph("<b>Pillar 1: Acute Emergency Telematics (SOS)</b><br/>Zero-latency GPS coordinate acquisition, persistent cloud audit logging, native SMS dispatch with Google Maps hyperlinks to trusted contacts, and direct 112/1091 calling.", tbl_cell),
            Paragraph("<b>Pillar 2: 'Adhira' AI Legal & Safety Companion</b><br/>High-speed LLM assistant powered by Groq (LLaMA 3.1 8B) with Gemini fallback. Educates users on Indian legal statutes, de-escalates panic, and maintains an empathetic sisterly tone.", tbl_cell)
        ],
        [
            Paragraph("<b>Pillar 3: Verified Civilian & NGO Volunteer Corps</b><br/>Voter ID verified volunteers with skill tags, language proficiencies, and NGO affiliations. Features an Active/Inactive status toggle and 1-on-1 private chat rooms.", tbl_cell),
            Paragraph("<b>Pillar 4: Safe Community & Grievance AI</b><br/>Anonymous story sharing with zero-shot multimodal Gemini AI moderation: classifies post urgency (green/yellow/red), assigns domain categories, and auto-quarantines toxic content.", tbl_cell)
        ]
    ]
    p_tbl = Table(p_data, colWidths=[258, 258])
    p_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(p_tbl)

    elements.append(Paragraph("Target Demographics & Operational Impact Matrix:", h2))
    dem_data = [
        [Paragraph("<b>Target Group</b>", tbl_hdr), Paragraph("<b>Specific Vulnerabilities Addressed</b>", tbl_hdr), Paragraph("<b>Key Platform Features Utilized</b>", tbl_hdr)],
        [
            Paragraph("<b>Solo Commuters & Students</b>", tbl_cell_bold),
            Paragraph("Late-night travel, cab harassment, suspicious following, street transit.", tbl_cell),
            Paragraph("One-tap SOS, live Google Maps SMS broadcast, trusted contact circles.", tbl_cell)
        ],
        [
            Paragraph("<b>Domestic Abuse Survivors</b>", tbl_cell_bold),
            Paragraph("Intimidation, coercive control, lack of legal rights awareness.", tbl_cell),
            Paragraph("Adhira legal advisor (PWDVA, IPC 498A), verified NGO volunteer private sessions.", tbl_cell)
        ],
        [
            Paragraph("<b>Workplace & Cyber Harassment Victims</b>", tbl_cell_bold),
            Paragraph("Stalking, online defamation, workplace harassment under POSH Act.", tbl_cell),
            Paragraph("Anonymous community posting, AI grievance classification, legal rights guidance.", tbl_cell)
        ],
        [
            Paragraph("<b>Active Volunteers & NGOs</b>", tbl_cell_bold),
            Paragraph("Coordination bottlenecks, lack of structured verification, volunteer burnout.", tbl_cell),
            Paragraph("Availability switch, ticket triage dashboard, verified badges, rating metrics.", tbl_cell)
        ]
    ]
    dem_tbl = Table(dem_data, colWidths=[120, 206, 190])
    dem_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(dem_tbl)

    elements.append(PageBreak())

    # =========================================================================
    # PAGE 3: 2. SYSTEM ARCHITECTURE & TECH STACK
    # =========================================================================
    elements.append(Paragraph("2. System Architecture & Technology Stack Breakdown", h1))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph(
        "Project Adhira is built as a resilient, decoupled client-server platform. "
        "A single, expressive Flutter client compiles across Web, Desktop (Windows), and Mobile devices, "
        "interacting with a secure Node.js/Express 5 API backed by MongoDB and cloud AI microservices.",
        body
    ))

    # Architecture ASCII Box
    arch_diagram = (
        "+-----------------------------------------------------------------------------------------+<br/>"
        "|                 <b>CROSS-PLATFORM FRONTEND LAYER (Flutter 3.x / Dart)</b>                    |<br/>"
        "|  User Shell • Role Selection • Material 3 UI • Provider Poller • Device GPS Hardware   |<br/>"
        "+-----------------------------------------------------------------------------------------+<br/>"
        "                                           │ HTTPS REST API Calls (JSON)<br/>"
        "                                           ▼<br/>"
        "+-----------------------------------------------------------------------------------------+<br/>"
        "|                 <b>API GATEWAY & BUSINESS LOGIC (Node.js / Express 5)</b>                    |<br/>"
        "|  Auth Middleware • Role Guard • SOS Dispatcher • Volunteer Matcher • Session Controller |<br/>"
        "+-------------------+-------------------+--------------------+------------------------+<br/>"
        "         │                   │                   │                       │<br/>"
        "         ▼                   ▼                   ▼                       ▼<br/>"
        "+-----------------+ +-----------------+ +------------------+ +---------------------------+<br/>"
        "|  <b>MongoDB Store</b>  | |  <b>Groq AI Engine</b> | | <b>Google Gemini</b>   | | <b>Device Telematics (OS)</b>   |<br/>"
        "| Users, SOS Logs | | LLaMA 3.1 8B    | | Zero-Shot AI     | | Geolocator GPS Satellites |<br/>"
        "| Posts, Sessions | | Sub-400ms Chat  | | Search Grounding | | Native SMS Intent Dispatch|<br/>"
        "+-----------------+ +-----------------+ +------------------+ +---------------------------+"
    )
    diag_tbl = Table([[Paragraph(arch_diagram, code_txt)]], colWidths=[516])
    diag_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#334155")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(diag_tbl)
    elements.append(Spacer(1, 6))

    elements.append(Paragraph("Technology Stack & Dependency Breakdown:", h2))
    tech_data = [
        [Paragraph("<b>Component Layer</b>", tbl_hdr), Paragraph("<b>Technology & Packages</b>", tbl_hdr), Paragraph("<b>Architectural Responsibility</b>", tbl_hdr)],
        [
            Paragraph("<b>Client Framework</b>", tbl_cell_bold),
            Paragraph("• Flutter 3.2.0+ (Dart)<br/>• <code>provider: ^6.1.2</code><br/>• <code>geolocator: ^12.0.0</code><br/>• <code>url_launcher: ^6.3.2</code><br/>• <code>image_picker: ^1.1.2</code>", tbl_cell),
            Paragraph("Renders responsive User & Volunteer Shells; manages background notification polling; queries device GPS hardware; triggers telephony SMS intents.", tbl_cell)
        ],
        [
            Paragraph("<b>Backend Server</b>", tbl_cell_bold),
            Paragraph("• Node.js & Express 5.2.1<br/>• <code>mongoose: ^9.4.1</code><br/>• <code>jsonwebtoken: ^9.0.3</code><br/>• <code>bcryptjs: ^3.0.3</code><br/>• <code>cors: ^2.8.6</code>", tbl_cell),
            Paragraph("Stateless REST API gateway. Handles password hashing, JWT issue/validation, role-based route guardrails, 50MB media payload payloads, and AI orchestration.", tbl_cell)
        ],
        [
            Paragraph("<b>Database</b>", tbl_cell_bold),
            Paragraph("• MongoDB 6+ / Atlas<br/>• Docker Compose container<br/>• Mongoose ODM", tbl_cell),
            Paragraph("Persists schemas for Users, Emergency Contacts, Verified Volunteers, SOS Events, Community Posts, Comments, and 1-on-1 Chat Sessions.", tbl_cell)
        ],
        [
            Paragraph("<b>Cloud AI Services</b>", tbl_cell_bold),
            Paragraph("• Groq Cloud API<br/>• Model: <code>llama-3.1-8b-instant</code><br/>• Google Gemini Flash & 2.5<br/>• Gemini Search Grounding", tbl_cell),
            Paragraph("High-speed conversational generation for Adhira assistant; zero-shot multimodal grievance & toxicity classification; live search for safety articles.", tbl_cell)
        ]
    ]
    tech_tbl = Table(tech_data, colWidths=[96, 170, 250])
    tech_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_DARK),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(tech_tbl)

    elements.append(PageBreak())

    # =========================================================================
    # PAGE 4: 3. EMERGENCY SOS & TELEMETRIC DISPATCH PROTOCOL
    # =========================================================================
    elements.append(Paragraph("3. Emergency SOS & Telemetric Dispatch Protocol", h1))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph(
        "The Emergency SOS subsystem is designed for deterministic execution under extreme urgency. "
        "When a user activates the SOS trigger, the client initiates a parallel telemetric dispatch protocol "
        "combining on-device satellite geocoding, persistent cloud logging, and cellular SMS broadcast.",
        body
    ))

    # SOS Steps Table
    sos_steps = [
        [Paragraph("<b>Phase</b>", tbl_hdr), Paragraph("<b>Subsystem Action</b>", tbl_hdr), Paragraph("<b>Implementation Details</b>", tbl_hdr)],
        [
            Paragraph("<b>Phase 1: Satellite Geolocation</b>", tbl_cell_bold),
            Paragraph("Device GPS Hardware Interrogation", tbl_cell),
            Paragraph("Invokes <code>Geolocator.getCurrentPosition()</code> with high-accuracy mode. Validates location service enablement and prompts permission escalation if denied.", tbl_cell)
        ],
        [
            Paragraph("<b>Phase 2: Cloud Incident Recording</b>", tbl_cell_bold),
            Paragraph("Secure REST API POST to <code>/api/sos</code>", tbl_cell),
            Paragraph("Serializes latitude, longitude, timestamp, and optional distress notes. Persists an immutable document in MongoDB for legal auditing and volunteer triage.", tbl_cell)
        ],
        [
            Paragraph("<b>Phase 3: Cellular SMS Dispatch</b>", tbl_cell_bold),
            Paragraph("Native OS SMS Intent via <code>url_launcher</code>", tbl_cell),
            Paragraph("Constructs recipient list from user's registered emergency contacts. Formats body with Google Maps hyperlink: <code>https://maps.google.com/?q={lat},{lng}</code>. Fires native SMS client even if data connection drops.", tbl_cell)
        ],
        [
            Paragraph("<b>Phase 4: Hotline Escalation</b>", tbl_cell_bold),
            Paragraph("Immediate Telephony Dialers", tbl_cell),
            Paragraph("Surfaces prominent dialer shortcuts for national emergency lines: <b>112</b> (National Emergency) and <b>1091</b> (Women Helpline).", tbl_cell)
        ]
    ]
    sos_tbl = Table(sos_steps, colWidths=[110, 160, 246])
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

    elements.append(Paragraph("Emergency Contact Management & Offline Resilience:", h2))
    elements.append(Paragraph(
        "Users can register multiple trusted contacts (family, friends, mentors) in their profile settings. "
        "Each contact entry contains a full name and verified phone number. In critical emergencies, reliance on "
        "push notifications or chat platforms frequently fails due to patchy 4G/5G data coverage or server latency. "
        "Project Adhira resolves this vulnerability by executing native telephony SMS broadcasts directly through the device's "
        "cellular radio, guaranteeing delivery anywhere a base cellular signal exists.",
        body
    ))

    # Code snippet of SMS trigger
    sms_code = (
        "// Frontend Emergency SMS Intent Dispatch Logic (from sos_screen.dart)\n"
        "final phones = user.emergencyContacts.map((c) => c.phone).join(',');\n"
        "final locationUrl = 'https://maps.google.com/?q=${position.latitude},${position.longitude}';\n"
        "final message = 'SOS EMERGENCY! I need help. My location: $locationUrl. ${_notesController.text.trim()}';\n"
        "final uri = Uri.parse('sms:$phones?body=${Uri.encodeComponent(message)}');\n"
        "if (await canLaunchUrl(uri)) { await launchUrl(uri); }"
    )
    sms_tbl = Table([[Paragraph(sms_code.replace('\n', '<br/>'), code_txt)]], colWidths=[516])
    sms_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#334155")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(sms_tbl)

    elements.append(Paragraph("SOS History & Forensic Audit Log:", h2))
    elements.append(Paragraph(
        "Every SOS activation creates a permanent record containing exact GPS coordinates, timestamp, and optional distress notes. "
        "Users and authorized responders can review this chronological log under the SOS history view to establish a timeline "
        "of events for legal documentation and police investigations.",
        body
    ))

    elements.append(PageBreak())

    # =========================================================================
    # PAGE 5: 4. 'ADHIRA' INTELLIGENT AI SAFETY & LEGAL ASSISTANT
    # =========================================================================
    elements.append(Paragraph("4. 'Adhira' Intelligent AI Safety & Legal Assistant", h1))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph(
        "<b>Adhira</b> is an autonomous conversational AI built into the application to serve as an empathetic first responder "
        "and legal advisor. The assistant is instructed to adopt the persona of a <i>'caring elder sister who knows the law'</i>, "
        "balancing deep emotional validation with actionable, pragmatic legal and safety instructions.",
        body
    ))

    elements.append(Paragraph("Dual-Engine Resilience & Failover Pipeline:", h2))
    elements.append(Paragraph(
        "Emergency advisory cannot tolerate API rate limit failures. The backend implements a 3-tier cascade:",
        body
    ))
    elements.append(Paragraph("• <b>Primary Engine (Groq LLaMA 3.1 8B):</b> Delivers sub-400ms streaming responses with low temperature (0.3) for concise, deterministic, and supportive guidance.", bullet))
    elements.append(Paragraph("• <b>Secondary Engine (Google Gemini Flash):</b> Automatically engages if Groq endpoints encounter rate limits, outages, or key exhaustion.", bullet))
    elements.append(Paragraph("• <b>Tertiary Deterministic Net:</b> Keyword sentiment heuristics return pre-compiled critical helpline steps if all external AI services are unreachable.", bullet))

    elements.append(Paragraph("Indian Legal Provisions & Legal Awareness Matrix:", h2))
    legal_data = [
        [Paragraph("<b>Statutory Framework</b>", tbl_hdr), Paragraph("<b>Key Provisions Covered</b>", tbl_hdr), Paragraph("<b>How Adhira Advises the User</b>", tbl_hdr)],
        [
            Paragraph("<b>Zero FIR Mandate</b>", tbl_cell_bold),
            Paragraph("Section 154 CrPC / BNSS provisions", tbl_cell),
            Paragraph("Clarifies that any police station must register an FIR for cognizable crimes regardless of jurisdiction, without redirecting the victim.", tbl_cell)
        ],
        [
            Paragraph("<b>Outrage of Modesty & Stalking</b>", tbl_cell_bold),
            Paragraph("IPC Sec 354, 354A (Harassment), 354D (Stalking) / BNS Equiv.", tbl_cell),
            Paragraph("Explains elements required to prove electronic/physical stalking, evidence gathering steps (screenshots, call logs), and non-bailable clauses.", tbl_cell)
        ],
        [
            Paragraph("<b>Domestic Violence Protections</b>", tbl_cell_bold),
            Paragraph("PWDVA Act 2005 & IPC Sec 498A (Cruelty)", tbl_cell),
            Paragraph("Outlines immediate Protection Orders, Right to Reside in shared household, and how to reach Protection Officers and recognized NGOs.", tbl_cell)
        ],
        [
            Paragraph("<b>Cyber Crimes & Anonymity</b>", tbl_cell_bold),
            Paragraph("IT Act Section 66E, 67, 67A & Cyber Crime Portal 1930", tbl_cell),
            Paragraph("Provides clear instructions on filing complaints for non-consensual image sharing, online blackmail, and reporting to National Cyber Crime portal.", tbl_cell)
        ]
    ]
    legal_tbl = Table(legal_data, colWidths=[120, 160, 236])
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

    elements.append(Paragraph("Ethical Guardrails & Tone Cleansing Engine:", h2))
    elements.append(Paragraph(
        "Trauma survivors are exceptionally vulnerable to patronizing language. A custom post-processing engine "
        "filters all AI-generated text with deterministic regex rules, stripping phrases like <i>'are you sure'</i>, "
        "<i>'big decision'</i>, or <i>'if you feel ready'</i>. Furthermore, any query matching high-distress keywords "
        "(e.g., weapon, assault, bleeding) forces mandatory insertion of national helplines: <b>Call 112</b> and <b>Women Helpline 1091</b>.",
        body
    ))

    elements.append(PageBreak())

    # =========================================================================
    # PAGE 6: 5. COMMUNITY FORUM & AI GRIEVANCE CLASSIFICATION
    # =========================================================================
    elements.append(Paragraph("5. Community Forum & AI-Powered Grievance Classification", h1))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph(
        "The Community subsystem enables women to share experiences, ask questions, and build collective resilience. "
        "To safeguard the forum against predatory content, trolls, and hate speech, every submission is analyzed by "
        "a <b>Zero-Shot Multimodal Grievance & Toxicity Moderation Framework</b> utilizing Google Gemini.",
        body
    ))

    # Grievance Pipeline Table
    grievance_data = [
        [Paragraph("<b>Evaluation Dimension</b>", tbl_hdr), Paragraph("<b>Classification Tag</b>", tbl_hdr), Paragraph("<b>System Action & Feed Behavior</b>", tbl_hdr)],
        [
            Paragraph("<b>Urgency Level</b>", tbl_cell_bold),
            Paragraph("<font color='#128751'><b>Green (Normal)</b></font>", tbl_cell),
            Paragraph("General questions, advice sharing, recovery stories. Displayed with subtle green urgency badge.", tbl_cell)
        ],
        [
            Paragraph("", tbl_cell),
            Paragraph("<font color='#D97706'><b>Yellow (Distress)</b></font>", tbl_cell),
            Paragraph("Emotional pain, anxiety, seeking advice. Prioritized on volunteer triage feeds for rapid support.", tbl_cell)
        ],
        [
            Paragraph("", tbl_cell),
            Paragraph("<font color='#DC284C'><b>Red (Crisis)</b></font>", tbl_cell),
            Paragraph("Active physical abuse, suicidal ideation, immediate danger. System triggers automated alert to user with prominent SOS button and hotline shortcuts.", tbl_cell)
        ],
        [
            Paragraph("<b>Toxicity Moderation</b>", tbl_cell_bold),
            Paragraph("<b>Low / Medium</b>", tbl_cell),
            Paragraph("Safe discourse or natural venting; passed to public feed.", tbl_cell)
        ],
        [
            Paragraph("", tbl_cell),
            Paragraph("<font color='#DC284C'><b>High (Toxic/Harmful)</b></font>", tbl_cell),
            Paragraph("<b>Automated Quarantine:</b> Post is auto-soft-deleted (<code>isDeleted: true</code>) and masked with label: <i>'Deleted due to unethical content'</i>.", tbl_cell)
        ],
        [
            Paragraph("<b>Domain Field Tagging</b>", tbl_cell_bold),
            Paragraph("<b>Domain Categories</b>", tbl_cell),
            Paragraph("Auto-categorized into: <i>Harassment, Domestic Violence, Stalking, Mental Health, Workplace Safety, Legal Support</i>.", tbl_cell)
        ]
    ]
    grievance_tbl = Table(grievance_data, colWidths=[110, 120, 286])
    grievance_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(grievance_tbl)

    elements.append(Paragraph("Anonymous Identity Mode & Rich Media Modalities:", h2))
    elements.append(Paragraph(
        "Users frequently need to disclose sensitive workplace harassment or domestic cruelty without fear of reprisal. "
        "Project Adhira incorporates a native <b>Anonymous Toggle</b> on every post and comment. When activated:",
        body
    ))
    elements.append(Paragraph("• The user's real name and profile photo are scrubbed and replaced with a generic anonymous avatar.", bullet))
    elements.append(Paragraph("• Public profile link endpoints are restricted for that post.", bullet))
    elements.append(Paragraph("• Posts support three distinct modalities: text narratives, attached photo evidence, or recorded audio voice notes.", bullet))

    elements.append(Paragraph("Peer Engagement, Reposts & Commenting:", h2))
    elements.append(Paragraph(
        "The community feed fosters supportive engagement with like counters, view metrics, nested comments, "
        "and a repost engine that amplifies critical advice and inspirational survivor accounts across the user base.",
        body
    ))

    elements.append(PageBreak())

    # =========================================================================
    # PAGE 7: 6. VERIFIED VOLUNTEER NETWORK & 1-ON-1 GUIDANCE
    # =========================================================================
    elements.append(Paragraph("6. Verified Volunteer Network & 1-on-1 Private Guidance", h1))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph(
        "A foundational differentiator of Project Adhira is its structured volunteer ecosystem. "
        "Rather than relying on anonymous forums, users can connect directly with vetted civilian advocates, "
        "social workers, and legal counselors.",
        body
    ))

    # Volunteer Workflow Table
    vol_wf = [
        [Paragraph("<b>Stage</b>", tbl_hdr), Paragraph("<b>Action & Vetting Criteria</b>", tbl_hdr), Paragraph("<b>Impact & Accountability Mechanism</b>", tbl_hdr)],
        [
            Paragraph("<b>1. Identity Onboarding</b>", tbl_cell_bold),
            Paragraph("Govt. Voter ID submission, occupation, address, phone number, languages spoken, and professional skills.", tbl_cell),
            Paragraph("Precludes impersonators; sets <code>voterIdVerified: true</code> badge on public profile.", tbl_cell)
        ],
        [
            Paragraph("<b>2. NGO Affiliation</b>", tbl_cell_bold),
            Paragraph("Verification of NGO registration name and social media credentials.", tbl_cell),
            Paragraph("Ensures formal backing from established social welfare organizations.", tbl_cell)
        ],
        [
            Paragraph("<b>3. Availability Switch</b>", tbl_cell_bold),
            Paragraph("Dashboard toggle between <b>Active</b> and <b>Inactive</b> status.", tbl_cell),
            Paragraph("Prevents distress tickets from going to offline volunteers; only active volunteers receive priority assignment.", tbl_cell)
        ],
        [
            Paragraph("<b>4. Private Sessions</b>", tbl_cell_bold),
            Paragraph("1-on-1 private messaging session spawned upon accepting a request.", tbl_cell),
            Paragraph("Provides a safe, confidential environment for sensitive case discussions.", tbl_cell)
        ],
        [
            Paragraph("<b>5. Post-Resolution Rating</b>", tbl_cell_bold),
            Paragraph("User submits 1-5 star rating, written review, hours spent, and people helped.", tbl_cell),
            Paragraph("Dynamically calculates rolling average rating and surfaces top-rated mentors.", tbl_cell)
        ]
    ]
    vol_tbl = Table(vol_wf, colWidths=[100, 186, 230])
    vol_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), ACCENT_GREEN),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('LINEBEFORE', (0,1), (0,-1), 3.5, ACCENT_GREEN),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(vol_tbl)

    elements.append(Paragraph("1-on-1 Private Counselling Architecture:", h2))
    elements.append(Paragraph(
        "When a user clicks <i>'Request Volunteer Help'</i> from the Guidance screen, they can choose a specific volunteer "
        "or broadcast to all active volunteers. Once accepted, the system establishes a private chat session "
        "(<code>PrivateChatSession</code>). Every message inside the private room is also monitored by AI for severe crisis "
        "keywords, ensuring that if a situation escalates to an acute emergency, emergency SOS procedures are immediately suggested.",
        body
    ))

    elements.append(Paragraph("Follow Requests & Mutual Privacy Controls:", h2))
    elements.append(Paragraph(
        "To prevent unwanted stalking or harassment between platform members, the application enforces a formal "
        "<b>Follow Request System</b>. Users can view followers, following counts, and accept or decline incoming follow "
        "requests. Only approved followers can view sensitive updates and non-public contact attributes.",
        body
    ))

    elements.append(PageBreak())

    # =========================================================================
    # PAGE 8: 7. DATABASE ARCHITECTURE & CORE SCHEMAS
    # =========================================================================
    elements.append(Paragraph("7. Database Architecture & Core Mongoose Schemas", h1))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph(
        "The application utilizes MongoDB via Mongoose ODM for flexible document storage and high-throughput read/write operations. "
        "The schema model comprises 8 core collections engineered for relational integrity and fast indexing:",
        body
    ))

    # Schemas Table
    sch_data = [
        [Paragraph("<b>Collection</b>", tbl_hdr), Paragraph("<b>Key Attributes & Types</b>", tbl_hdr), Paragraph("<b>Business Function & Indexing</b>", tbl_hdr)],
        [
            Paragraph("<b>User</b>", tbl_cell_bold),
            Paragraph("<code>name, email, password, googleId, role ('user'|'volunteer'), voterIdVerified, volunteerAvailability ('active'|'inactive'), emergencyContacts: [{name, phone}], ratings: [{userId, rating, review}], averageRating, followers, following, followRequests</code>", code_txt),
            Paragraph("Core identity store. Indexed on <code>email</code> and <code>googleId</code> (sparse). Handles credential verification, volunteer profiles, and mutual privacy.", tbl_cell)
        ],
        [
            Paragraph("<b>HelpRequest</b>", tbl_cell_bold),
            Paragraph("<code>requesterId (ref: User), volunteerId (ref: User), sosId (ref: SOS), message, assistanceNote, hoursSpent, peopleHelped, rating (1-5), status ('pending'|'accepted'|'rejected'|'completed')</code>", code_txt),
            Paragraph("Tracks guidance lifecycle. Indexed on <code>requesterId</code> and <code>volunteerId</code> for fast ticket dashboard rendering.", tbl_cell)
        ],
        [
            Paragraph("<b>Post</b>", tbl_cell_bold),
            Paragraph("<code>userId (ref: User), content, caption, mediaUrl, mediaType ('text'|'image'|'audio'), isAnonymous, mode ('public'|'private'), field, distressLevel, urgencyColor, toxicityLevel, isDeleted, likes, views</code>", code_txt),
            Paragraph("Community feed entries. Stores Gemini sentiment results, urgency color badges, and soft-delete flags for quarantine.", tbl_cell)
        ],
        [
            Paragraph("<b>PrivateChatSession & Message</b>", tbl_cell_bold),
            Paragraph("<code>Session: { helpSeekerId, volunteerId, originalPostId, status }</code><br/><code>Message: { sessionId, senderId, content, urgencyColor, toxicityLevel, isDeleted }</code>", code_txt),
            Paragraph("1-on-1 private guidance rooms. Captures message exchange and sentiment between matched pairs.", tbl_cell)
        ],
        [
            Paragraph("<b>SOS & SOSHistory</b>", tbl_cell_bold),
            Paragraph("<code>userId (ref: User), location: { lat: Number, lng: Number }, notes, timestamps</code>", code_txt),
            Paragraph("Permanent spatial audit log of emergency incidents for legal and responder use.", tbl_cell)
        ],
        [
            Paragraph("<b>Story</b>", tbl_cell_bold),
            Paragraph("<code>userId (ref: User), title, snippet, anonymous, likes: [{ref: User}], timestamps</code>", code_txt),
            Paragraph("Inspirational stories and survivor narratives displayed on the community tab.", tbl_cell)
        ]
    ]
    sch_tbl = Table(sch_data, colWidths=[86, 260, 170])
    sch_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_DARK),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(sch_tbl)

    elements.append(Paragraph("Security, Data Minimization & Privacy Rules:", h2))
    elements.append(Paragraph(
        "• <b>Password Security:</b> All user passwords are encrypted using Bcrypt with a salt factor of 10 before disk write.<br/>"
        "• <b>Token Authorization:</b> API requests require Bearer JWT authentication; volunteer-only endpoints strictly enforce role authorization middleware.<br/>"
        "• <b>Data Scrubbing:</b> Queries for public user profiles omit sensitive fields such as passwords, voter ID documents, and emergency contact phone numbers.",
        body
    ))

    elements.append(PageBreak())

    # =========================================================================
    # PAGE 9: 8. COMPANION ECOSYSTEM: SAFETY APPS & REAL-TIME BLOGS
    # =========================================================================
    elements.append(Paragraph("8. Companion Safety Ecosystem & Real-Time AI Search", h1))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph(
        "Recognizing that comprehensive security requires an ecosystem approach, Project Adhira integrates two "
        "valuable external resources: a curated directory of specialized companion safety apps and a real-time "
        "AI-grounded safety and legal knowledge base.",
        body
    ))

    elements.append(Paragraph("Curated Companion Safety Apps Directory:", h2))
    elements.append(Paragraph(
        "The application provides a built-in directory linking users directly to vetted Android and iOS safety applications, "
        "allowing women to select specialized tools that fit their commute or hardware preferences:",
        body
    ))

    # Safety Apps Table
    apps_data = [
        [Paragraph("<b>Application</b>", tbl_hdr), Paragraph("<b>Core Specialty & Feature Set</b>", tbl_hdr), Paragraph("<b>Platform Integration & Use Case</b>", tbl_hdr)],
        [
            Paragraph("<b>bSafe</b>", tbl_cell_bold),
            Paragraph("Personal safety with SOS trigger, live GPS location tracking, and fake incoming calls.", tbl_cell),
            Paragraph("Ideal for solo night travel and escaping uncomfortable social encounters.", tbl_cell)
        ],
        [
            Paragraph("<b>Raksha</b>", tbl_cell_bold),
            Paragraph("Volume-button hardware SOS triggering, sends location even with screen locked.", tbl_cell),
            Paragraph("Hands-free emergency activation when taking phone out is impossible.", tbl_cell)
        ],
        [
            Paragraph("<b>Himmat</b>", tbl_cell_bold),
            Paragraph("Delhi Police initiative; transmits live video, audio, and GPS directly to police control room.", tbl_cell),
            Paragraph("High-priority direct law enforcement dispatch in metropolitan zones.", tbl_cell)
        ],
        [
            Paragraph("<b>Circle of 6</b>", tbl_cell_bold),
            Paragraph("Pre-programmed discreet SMS codes sent to 6 close friends with two taps.", tbl_cell),
            Paragraph("Subtle campus and social safety communication among trusted circles.", tbl_cell)
        ],
        [
            Paragraph("<b>My Safetipin</b>", tbl_cell_bold),
            Paragraph("Crowdsourced safety audits analyzing street lighting, visibility, and foot traffic.", tbl_cell),
            Paragraph("Proactive route planning to avoid deserted or poorly-lit urban stretches.", tbl_cell)
        ],
        [
            Paragraph("<b>Shake2Safety</b>", tbl_cell_bold),
            Paragraph("Accelerometer shake gesture triggers emergency SMS and captures 4-second audio clip.", tbl_cell),
            Paragraph("Instant stealth activation without unlocking the mobile device.", tbl_cell)
        ]
    ]
    apps_tbl = Table(apps_data, colWidths=[96, 220, 200])
    apps_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_DARK),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(apps_tbl)

    elements.append(Paragraph("'Know Your Community' AI-Grounded Knowledge Hub:", h2))
    elements.append(Paragraph(
        "Static safety FAQs quickly become outdated. The 'Know Your Community' module invokes Google Gemini "
        "with <b>Google Search Tool Grounding</b> to fetch real, live articles and news reports regarding women's rights, "
        "safety reforms, and practical self-defense tips. Each article returned includes a verified source URL, category tag, "
        "concise summary, and publication date, empowering women with up-to-date legal literacy and practical knowledge.",
        body
    ))

    elements.append(PageBreak())

    # =========================================================================
    # PAGE 10: 9. SETUP, DEPLOYMENT, API REFERENCE & STRATEGIC ROADMAP
    # =========================================================================
    elements.append(Paragraph("9. Setup, Deployment, API Reference & Strategic Roadmap", h1))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph("Rapid Windows & Local Execution:", h2))
    p_code = (
        "<b># Automated Launch Script (PowerShell):</b><br/>"
        "powershell -ExecutionPolicy Bypass -File .\\run-windows.ps1 -Port 5000<br/>"
        "<b># Manual Backend Launch:</b><br/>"
        "cd Backend &amp;&amp; npm install &amp;&amp; $env:PORT=5000 &amp;&amp; npm run dev<br/>"
        "<b># Seed Default Administrator (admin / admin):</b><br/>"
        "cd Backend &amp;&amp; npm run seed:admin<br/>"
        "<b># Flutter Client Launch (Web / Chrome):</b><br/>"
        "cd frontend &amp;&amp; flutter pub get &amp;&amp; flutter run -d chrome --dart-define=API_BASE_URL=http://127.0.0.1:5000"
    )
    p_tbl = Table([[Paragraph(p_code, code_txt)]], colWidths=[516])
    p_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#334155")),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(p_tbl)

    elements.append(Paragraph("Core Backend API Reference:", h2))
    api_ref = [
        [Paragraph("<b>Route</b>", tbl_hdr), Paragraph("<b>Verb</b>", tbl_hdr), Paragraph("<b>Auth</b>", tbl_hdr), Paragraph("<b>Functionality</b>", tbl_hdr)],
        [
            Paragraph("<code>/api/auth/register, /login</code>", code_txt),
            Paragraph("POST", tbl_cell_bold),
            Paragraph("Public", tbl_cell),
            Paragraph("Registers account with role selection (user/volunteer); issues JWT token.", tbl_cell)
        ],
        [
            Paragraph("<code>/api/sos</code>", code_txt),
            Paragraph("POST/GET", tbl_cell_bold),
            Paragraph("JWT", tbl_cell),
            Paragraph("Records GPS coordinates & notes; returns user emergency incident history.", tbl_cell)
        ],
        [
            Paragraph("<code>/api/chatbot</code>", code_txt),
            Paragraph("POST", tbl_cell_bold),
            Paragraph("Public", tbl_cell),
            Paragraph("Invokes Adhira AI assistant (Groq LLaMA / Gemini) with legal & safety reasoning.", tbl_cell)
        ],
        [
            Paragraph("<code>/api/posts</code>", code_txt),
            Paragraph("GET/POST", tbl_cell_bold),
            Paragraph("JWT", tbl_cell),
            Paragraph("Community feed operations; runs Gemini zero-shot grievance & toxicity checks.", tbl_cell)
        ],
        [
            Paragraph("<code>/api/volunteers</code>", code_txt),
            Paragraph("GET", tbl_cell_bold),
            Paragraph("JWT", tbl_cell),
            Paragraph("Lists verified volunteers; supports skill/keyword and active availability filters.", tbl_cell)
        ],
        [
            Paragraph("<code>/api/private-chat/accept/:id</code>", code_txt),
            Paragraph("POST", tbl_cell_bold),
            Paragraph("Volunteer", tbl_cell),
            Paragraph("Spawns 1-on-1 private messaging room between volunteer and help seeker.", tbl_cell)
        ],
        [
            Paragraph("<code>/api/community/blogs</code>", code_txt),
            Paragraph("GET", tbl_cell_bold),
            Paragraph("JWT", tbl_cell),
            Paragraph("Fetches live safety and legal blogs via Gemini Google Search tool grounding.", tbl_cell)
        ]
    ]
    api_tbl = Table(api_ref, colWidths=[140, 48, 56, 272])
    api_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_DARK),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(api_tbl)

    elements.append(Paragraph("Strategic Future Roadmap (Version 2.0+):", h2))
    road_data = [
        [
            Paragraph("<b>Acoustic Distress & Scream Detection</b>", tbl_cell_bold),
            Paragraph("Background audio listener running on-device ML to detect scream acoustics or distress phrases (e.g. <i>'Help Adhira'</i>) to trigger hands-free SOS.", tbl_cell)
        ],
        [
            Paragraph("<b>Decentralized Mesh Networking</b>", tbl_cell_bold),
            Paragraph("Bluetooth Low Energy (BLE) peer-to-peer relaying of SOS distress beacons across nearby smartphones even when cellular data is disabled.", tbl_cell)
        ],
        [
            Paragraph("<b>Direct Police Dispatch CAD Integration</b>", tbl_cell_bold),
            Paragraph("Direct API integration with State Police Emergency Response Support Systems (ERSS 112) for automated CAD ticket creation and cruiser dispatch.", tbl_cell)
        ]
    ]
    road_tbl = Table(road_data, colWidths=[150, 366])
    road_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('LINEBEFORE', (0,0), (0,-1), 3.5, PRIMARY),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(road_tbl)

    # Build
    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"SUCCESS: Generated {filename}")

if __name__ == "__main__":
    out_name = "Women_Safety_And_Support_App_Detailed_Documentation.pdf"
    if len(sys.argv) > 1:
        out_name = sys.argv[1]
    build_pdf(out_name)
