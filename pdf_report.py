"""
pdf_report.py — Generate a beautiful Astro Matching PDF report
Uses ReportLab (Platypus + Canvas).
Built by Vishnuram — Software Engineer
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.graphics.shapes import Drawing, Rect, String, Circle, Line
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import renderPDF

# ─────────────────────────────────────────────────────────────
# COLOR PALETTE
# ─────────────────────────────────────────────────────────────
DARK_BG    = colors.HexColor("#0b0f1a")
DARK_CARD  = colors.HexColor("#1a1f35")
GOLD       = colors.HexColor("#FFD700")
ORANGE     = colors.HexColor("#FF6B35")
GREEN      = colors.HexColor("#00C851")
RED        = colors.HexColor("#ff4444")
AMBER      = colors.HexColor("#FF8800")
BLUE_LIGHT = colors.HexColor("#4f8ef7")
PURPLE     = colors.HexColor("#a78bfa")
TEAL       = colors.HexColor("#38bdf8")
SLATE      = colors.HexColor("#94a3b8")
SLATE_DARK = colors.HexColor("#475569")
WHITE      = colors.white
PAGE_W, PAGE_H = A4   # 595 × 842 pts


# ─────────────────────────────────────────────────────────────
# CUSTOM STYLES
# ─────────────────────────────────────────────────────────────

def build_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles["title"] = ParagraphStyle("title",
        fontName="Helvetica-Bold", fontSize=22, textColor=GOLD,
        alignment=TA_CENTER, spaceAfter=4, leading=28)

    styles["subtitle"] = ParagraphStyle("subtitle",
        fontName="Helvetica", fontSize=10, textColor=SLATE,
        alignment=TA_CENTER, spaceAfter=2)

    styles["credit"] = ParagraphStyle("credit",
        fontName="Helvetica", fontSize=8, textColor=SLATE_DARK,
        alignment=TA_CENTER, spaceAfter=8)

    styles["section_head"] = ParagraphStyle("section_head",
        fontName="Helvetica-Bold", fontSize=13, textColor=GOLD,
        spaceBefore=14, spaceAfter=6)

    styles["sub_head"] = ParagraphStyle("sub_head",
        fontName="Helvetica-Bold", fontSize=10, textColor=BLUE_LIGHT,
        spaceBefore=8, spaceAfter=4)

    styles["body"] = ParagraphStyle("body",
        fontName="Helvetica", fontSize=9, textColor=SLATE,
        spaceAfter=3, leading=14)

    styles["body_white"] = ParagraphStyle("body_white",
        fontName="Helvetica", fontSize=9, textColor=WHITE,
        spaceAfter=2, leading=13)

    styles["bold_white"] = ParagraphStyle("bold_white",
        fontName="Helvetica-Bold", fontSize=9, textColor=WHITE,
        spaceAfter=2)

    styles["label"] = ParagraphStyle("label",
        fontName="Helvetica", fontSize=8, textColor=SLATE_DARK,
        spaceAfter=1)

    styles["verdict"] = ParagraphStyle("verdict",
        fontName="Helvetica-Bold", fontSize=14,
        alignment=TA_CENTER, spaceAfter=4)

    styles["score_big"] = ParagraphStyle("score_big",
        fontName="Helvetica-Bold", fontSize=36, textColor=GOLD,
        alignment=TA_CENTER, leading=40)

    styles["small"] = ParagraphStyle("small",
        fontName="Helvetica", fontSize=7.5, textColor=SLATE_DARK,
        spaceAfter=2, leading=11)

    return styles


# ─────────────────────────────────────────────────────────────
# SCORE BAR (inline Drawing)
# ─────────────────────────────────────────────────────────────

def score_bar_drawing(pct: float, width: float = 340, height: float = 10) -> Drawing:
    d = Drawing(width, height)
    # Background
    d.add(Rect(0, 0, width, height,
               fillColor=colors.HexColor("#1e2a3a"), strokeColor=None))
    # Fill
    fill_w = max(0, min(width, width * pct / 100))
    fc = GREEN if pct >= 75 else AMBER if pct >= 50 else RED
    d.add(Rect(0, 0, fill_w, height, fillColor=fc, strokeColor=None, rx=3, ry=3))
    return d


# ─────────────────────────────────────────────────────────────
# COVER HEADER DRAWING
# ─────────────────────────────────────────────────────────────

def header_drawing() -> Drawing:
    w, h = PAGE_W - 60, 80
    d = Drawing(w, h)
    # Background rect
    d.add(Rect(0, 0, w, h, fillColor=colors.HexColor("#141928"),
               strokeColor=GOLD, strokeWidth=0.8, rx=10, ry=10))
    # Decorative circles
    d.add(Circle(30, h/2, 18, fillColor=colors.HexColor("#FF6B3522"), strokeColor=ORANGE, strokeWidth=1))
    d.add(Circle(w-30, h/2, 18, fillColor=colors.HexColor("#FFD70022"), strokeColor=GOLD, strokeWidth=1))
    # Title text
    d.add(String(w/2, h/2+14, "🌟 HOROSCOPE MATCHING REPORT",
                 fontName="Helvetica-Bold", fontSize=16,
                 fillColor=GOLD, textAnchor="middle"))
    d.add(String(w/2, h/2-4, "Tamil Jyotish · 10 Poruthams · Advanced Analysis",
                 fontName="Helvetica", fontSize=9,
                 fillColor=SLATE, textAnchor="middle"))
    d.add(String(w/2, h/2-18, "Built by Vishnuram — Software Engineer",
                 fontName="Helvetica", fontSize=8,
                 fillColor=SLATE_DARK, textAnchor="middle"))
    return d


# ─────────────────────────────────────────────────────────────
# MAIN PDF GENERATOR
# ─────────────────────────────────────────────────────────────

def generate_pdf(summary: dict, user: dict = None) -> bytes:
    """
    Generate a complete Astro Matching PDF.
    Returns bytes that can be offered as a download.

    summary: dict returned by AstroMatchingEngine.calculate_all()
    user:    dict with 'display_name', 'username' (optional)
    """
    buf    = io.BytesIO()
    doc    = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=25*mm, rightMargin=25*mm,
        topMargin=20*mm, bottomMargin=20*mm,
        title="Horoscope Matching Report",
        author="Vishnuram — Software Engineer",
    )
    S = build_styles()
    story = []

    # ── HEADER DRAWING ───────────────────────────────────────
    story.append(header_drawing())
    story.append(Spacer(1, 10))

    # ── DATE / USER LINE ────────────────────────────────────
    now = datetime.now().strftime("%d %B %Y, %I:%M %p")
    user_label = f"Prepared for: {user['display_name']} (@{user['username']})" if user else ""
    story.append(Paragraph(f"<font color='#475569'>{now}</font>", S["credit"]))
    if user_label:
        story.append(Paragraph(f"<font color='#64748b'>{user_label}</font>", S["credit"]))

    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD, spaceAfter=10))

    # ── COUPLE INFO ──────────────────────────────────────────
    story.append(Paragraph("Couple Details", S["section_head"]))

    groom = summary["groom"]
    bride = summary["bride"]
    gsi   = summary["groom_star_details"]
    bsi   = summary["bride_star_details"]
    gri   = summary["groom_rasi_details"]
    bri   = summary["bride_rasi_details"]

    def person_table(label, name, si, padham, ri, col_bg):
        data = [
            [Paragraph(f"<b><font color='#{col_bg}'>{label}</font></b>", S["body"]),
             Paragraph(f"<b><font color='white'>{name}</font></b>", S["body"])],
            ["Star (Nakshatra)", f"{si['name']} ({si['tamil']})"],
            ["Padham", f"{padham}  (Quarter)"],
            ["Rasi", f"{ri['name']} ({ri.get('english','')})"],
            ["Nakshatra Lord", si["lord"]],
            ["Gana", si["gana"]],
            ["Nadi", si["nadi"]],
            ["Yoni", si["yoni"]],
            ["Varna", si["varna"]],
            ["Element", ri.get("element","")],
        ]
        t = Table(data, colWidths=[90, 140])
        t.setStyle(TableStyle([
            ("BACKGROUND",  (0,0), (-1,0), colors.HexColor("#1a1f35")),
            ("BACKGROUND",  (0,1), (-1,-1), colors.HexColor("#111827")),
            ("TEXTCOLOR",   (0,1), (0,-1), SLATE_DARK),
            ("TEXTCOLOR",   (1,1), (1,-1), SLATE),
            ("FONTNAME",    (0,1), (0,-1), "Helvetica"),
            ("FONTNAME",    (1,1), (1,-1), "Helvetica"),
            ("FONTSIZE",    (0,0), (-1,-1), 8.5),
            ("ROWBACKGROUNDS", (0,1), (-1,-1),
             [colors.HexColor("#111827"), colors.HexColor("#0f1520")]),
            ("GRID",        (0,0), (-1,-1), 0.3, colors.HexColor("#1e293b")),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
            ("RIGHTPADDING",(0,0), (-1,-1), 8),
            ("TOPPADDING",  (0,0), (-1,-1), 5),
            ("BOTTOMPADDING",(0,0),(-1,-1), 5),
            ("SPAN",        (0,0), (0,0)),
            ("ROUNDEDCORNERS", (0,0), (-1,-1), 4),
        ]))
        return t

    couple_data = [[
        person_table("🤵  GROOM", groom["name"], gsi, groom["padham"], gri, "4f8ef7"),
        Spacer(10, 1),
        person_table("👰  BRIDE", bride["name"], bsi, bride["padham"], bri, "f472b6"),
    ]]
    couple_t = Table(couple_data, colWidths=[235, 10, 235])
    couple_t.setStyle(TableStyle([
        ("VALIGN",      (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING",(0,0), (-1,-1), 0),
    ]))
    story.append(couple_t)
    story.append(Spacer(1, 14))

    # ── OVERALL SCORE ────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD, spaceBefore=4, spaceAfter=8))
    story.append(Paragraph("Overall Match Score", S["section_head"]))

    pct = summary["final_percentage"]
    vc  = summary["verdict_color"]
    v_color_map  = {"green": GREEN, "blue": BLUE_LIGHT, "orange": AMBER, "red": RED}
    v_hex_map    = {"green": "#00C851","blue": "#4f8ef7","orange": "#FF8800","red": "#ff4444"}
    v_col        = v_color_map.get(vc, RED)
    v_hex        = v_hex_map.get(vc, "#ff4444")

    score_data = [
        [
            # Big score
            [
                Paragraph(f"{pct:.1f}%", S["score_big"]),
                Paragraph("Weighted Match Score", S["small"]),
            ],
            # Verdict + bar
            [
                Paragraph(f'<font color="{v_hex}">{summary["verdict"]}</font>', S["verdict"]),
                score_bar_drawing(pct, width=220),
                Spacer(1, 6),
                Paragraph(
                    f'Raw Score: <b>{summary["raw_score"]}/{summary["raw_max"]}</b> '
                    f'({summary["raw_percentage"]:.1f}%)  &nbsp;&nbsp; '
                    f'Doshas: <b>{summary["total_doshas"]}</b>  &nbsp;&nbsp; '
                    f'Critical: <b>{len(summary["critical_doshas"])}</b>',
                    S["body"]
                ),
            ],
        ]
    ]

    score_t = Table(score_data, colWidths=[150, 330])
    score_t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), colors.HexColor("#141928")),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 14),
        ("RIGHTPADDING",(0,0), (-1,-1), 14),
        ("TOPPADDING",  (0,0), (-1,-1), 14),
        ("BOTTOMPADDING",(0,0),(-1,-1), 14),
        ("BOX",         (0,0), (-1,-1), 0.8, GOLD),
        ("GRID",        (0,0), (-1,-1), 0.2, colors.HexColor("#1e293b")),
        ("ROUNDEDCORNERS", (0,0), (-1,-1), 6),
    ]))
    story.append(score_t)

    # Doshas summary
    if summary["critical_doshas"]:
        story.append(Spacer(1, 6))
        story.append(Paragraph(
            f'<font color="#ff4444"><b>Critical Doshas:</b></font> '
            f'<font color="#94a3b8">{", ".join(summary["critical_doshas"])}</font>',
            S["body"]
        ))
    if summary["minor_doshas"]:
        story.append(Paragraph(
            f'<font color="#FF8800"><b>Minor Doshas:</b></font> '
            f'<font color="#94a3b8">{", ".join(summary["minor_doshas"])}</font>',
            S["body"]
        ))

    story.append(Spacer(1, 16))

    # ── 10 PORUTHAM TABLE ───────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD, spaceBefore=4, spaceAfter=8))
    story.append(Paragraph("10 Porutham — Detailed Analysis", S["section_head"]))

    header_row = [
        Paragraph("<b>Porutham</b>", S["bold_white"]),
        Paragraph("<b>Tamil</b>", S["bold_white"]),
        Paragraph("<b>Category</b>", S["bold_white"]),
        Paragraph("<b>Score</b>", S["bold_white"]),
        Paragraph("<b>Match %</b>", S["bold_white"]),
        Paragraph("<b>Compatibility</b>", S["bold_white"]),
        Paragraph("<b>Status</b>", S["bold_white"]),
    ]
    table_data = [header_row]

    for r in summary["results"]:
        pct_r = r["percentage"]
        bar_c = GREEN if pct_r >= 75 else AMBER if pct_r >= 50 else RED
        status_txt = "DOSHA" if r["dosha"] else "PASS"
        status_col = RED if r["dosha"] else GREEN

        row = [
            Paragraph(r["name"], S["body_white"]),
            Paragraph(f'<font size="8">{r["tamil"]}</font>', S["body"]),
            Paragraph(r["category"], S["body"]),
            Paragraph(f'<b><font color="#{("00C851" if pct_r>=75 else "FF8800" if pct_r>=50 else "ff4444")}">{r["score"]}/{r["max_score"]}</font></b>', S["body"]),
            Paragraph(f"{pct_r:.0f}%", S["body"]),
            Paragraph(r["compatibility"], S["body"]),
            Paragraph(f'<b><font color="{"#ff4444" if r["dosha"] else "#00C851"}">{status_txt}</font></b>', S["body"]),
        ]
        table_data.append(row)

    p_table = Table(table_data, colWidths=[110, 72, 72, 40, 42, 100, 44])
    p_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0),  colors.HexColor("#1a1f35")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.HexColor("#0f1520"), colors.HexColor("#111827")]),
        ("GRID",         (0,0), (-1,-1), 0.3, colors.HexColor("#1e293b")),
        ("FONTSIZE",     (0,0), (-1,-1), 8.5),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(p_table)
    story.append(Spacer(1, 14))

    # ── PORUTHAM DETAILS (one block per porutham) ───────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD, spaceBefore=4, spaceAfter=8))
    story.append(Paragraph("Detailed Porutham Explanations", S["section_head"]))

    for r in summary["results"]:
        pct_r   = r["percentage"]
        bar_col = GREEN if pct_r >= 75 else AMBER if pct_r >= 50 else RED
        label_c = "#ff4444" if r["dosha"] else "#00C851"
        dosha_t = "⚠ DOSHA" if r["dosha"] else "✓ PASS"
        crit_t  = "  [CRITICAL]" if r["is_critical"] and r["dosha"] else ""

        row_data = [
            [
                Paragraph(
                    f'<b><font color="white">{r["name"]}</font></b>  '
                    f'<font size="8" color="#94a3b8">({r["tamil"]})</font>  '
                    f'<font size="8" color="#475569">· {r["category"]}</font>',
                    S["body"]
                ),
                Paragraph(
                    f'<b><font color="#{("00C851" if pct_r>=75 else "FF8800" if pct_r>=50 else "ff4444")}">'
                    f'{r["score"]}/{r["max_score"]}</font></b>  '
                    f'<font color="{label_c}"><b>{dosha_t}{crit_t}</b></font>',
                    S["body"]
                ),
            ],
            [
                [
                    score_bar_drawing(pct_r, width=250),
                    Spacer(1, 4),
                    Paragraph(
                        f'<b><font color="white">{r["compatibility"]}</font></b> — '
                        f'<font color="#94a3b8">{r["details"]}</font>',
                        S["small"]
                    ),
                ],
                Paragraph(f"<b>{pct_r:.0f}%</b>", S["body"]),
            ],
        ]

        detail_t = Table(row_data, colWidths=[370, 110])
        detail_t.setStyle(TableStyle([
            ("BACKGROUND",  (0,0), (-1,-1), colors.HexColor("#0f1520")),
            ("BOX",         (0,0), (-1,-1), 0.4, colors.HexColor("#1e293b")),
            ("LEFTBORDER",  (0,0), (0,-1),  3,   bar_col),
            ("LEFTPADDING", (0,0), (-1,-1), 10),
            ("RIGHTPADDING",(0,0), (-1,-1), 8),
            ("TOPPADDING",  (0,0), (-1,-1), 7),
            ("BOTTOMPADDING",(0,0),(-1,-1), 7),
            ("VALIGN",      (0,0), (-1,-1), "TOP"),
            # Thicker left border using LINEAFTER on col -1 left
            ("LINEBEFORE",  (0,0), (0,-1),  4, bar_col),
        ]))
        story.append(KeepTogether([detail_t, Spacer(1, 6)]))

    # ── PADHAM & NAVAMSA ────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD, spaceBefore=8, spaceAfter=8))
    story.append(Paragraph("Padham & Navamsa Analysis", S["section_head"]))

    pa = summary["padham_analysis"]
    padham_data = [
        [Paragraph("<b>Detail</b>", S["bold_white"]),
         Paragraph("<b>Groom</b>", S["bold_white"]),
         Paragraph("<b>Bride</b>", S["bold_white"])],
        ["Padham", str(pa.get("groom_padham", "")), str(pa.get("bride_padham", ""))],
        ["Navamsa Rasi", pa.get("groom_navamsa",""), pa.get("bride_navamsa","")],
        ["Navamsa Compatibility", pa.get("navamsa_lord_compatibility",""), ""],
    ]
    pt = Table(padham_data, colWidths=[150, 175, 155])
    pt.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#1a1f35")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#0f1520"),colors.HexColor("#111827")]),
        ("TEXTCOLOR",    (0,1), (-1,-1), SLATE),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("GRID",         (0,0), (-1,-1), 0.3, colors.HexColor("#1e293b")),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("SPAN",         (1,3), (2,3)),
    ]))
    story.append(pt)
    story.append(Spacer(1, 14))

    # ── REMEDIES (if doshas exist) ───────────────────────────
    all_doshas = summary["critical_doshas"] + summary["minor_doshas"]
    if all_doshas:
        story.append(HRFlowable(width="100%", thickness=0.5, color=AMBER, spaceBefore=6, spaceAfter=8))
        story.append(Paragraph("Traditional Remedies (Pariharams)", S["section_head"]))

        REMEDIES = {
            "Nadi Porutham":  "Nadi Dosha Nivarana Puja at a Shiva temple. Gifting gold to a priest on wedding day. 1,08,000 Maha Mrityunjaya Japa.",
            "Rajju Porutham": "Rajju Dosha Parihara Puja. Sacred Raksha thread ceremony with mantras. Seek blessings of 7 Sumangalis.",
            "Gana Porutham":  "Shiva-Parvathi Puja for 21 Mondays. Offer bilva leaves and light camphor.",
            "Yoni Porutham":  "Ashta Mangala Puja. Kula Devata worship. Offer coconuts and bananas.",
            "Vedha Porutham": "Navagraha Shanti Puja. Light sesame oil lamps for 45 consecutive days.",
            "Varna Porutham": "Seek blessings of elders. Saraswati Puja for spiritual harmony.",
            "Stree Deerga":   "Lakshmi Puja and Suhasini blessings ceremony on an auspicious day.",
        }
        rem_data = [[
            Paragraph("<b>Dosha</b>", S["bold_white"]),
            Paragraph("<b>Remedy</b>", S["bold_white"])
        ]]
        for d in all_doshas:
            if d in REMEDIES:
                dc = "#ff4444" if d in summary["critical_doshas"] else "#FF8800"
                rem_data.append([
                    Paragraph(f'<font color="{dc}"><b>{d}</b></font>', S["body"]),
                    Paragraph(REMEDIES[d], S["body"]),
                ])
        rem_t = Table(rem_data, colWidths=[140, 340])
        rem_t.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#1a1f35")),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#0f1520"),colors.HexColor("#111827")]),
            ("GRID",         (0,0), (-1,-1), 0.3, colors.HexColor("#1e293b")),
            ("FONTSIZE",     (0,0), (-1,-1), 8.5),
            ("LEFTPADDING",  (0,0), (-1,-1), 8),
            ("TOPPADDING",   (0,0), (-1,-1), 5),
            ("BOTTOMPADDING",(0,0), (-1,-1), 5),
            ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ]))
        story.append(rem_t)
        story.append(Spacer(1, 8))
        story.append(Paragraph(
            "⚠ These are traditional suggestions. Always consult a qualified Vedic astrologer for personalized guidance.",
            S["small"]
        ))

    # ── FOOTER ──────────────────────────────────────────────
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=0.5, color=SLATE_DARK, spaceAfter=6))
    story.append(Paragraph(
        f'Generated on {now}  &nbsp;|&nbsp;  '
        f'Built by <b>Vishnuram</b> — Software Engineer  &nbsp;|&nbsp;  '
        f'Tamil Jyotish · 10 Poruthams Calculator',
        S["credit"]
    ))

    # ── BUILD ───────────────────────────────────────────────
    doc.build(story)
    return buf.getvalue()
