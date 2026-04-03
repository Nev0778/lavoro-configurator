"""
PDF Specification Sheet Generator for Lavoro Design
Generates a bespoke spec sheet based on user-selected dimensions and finishes.
"""
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle


# Colour hex values for frame finishes
FRAME_COLOURS = {
    "Black":      "#1a1a1a",
    "Anthracite": "#3d3d3d",
    "Dark Grey":  "#555555",
    "Raw Steel":  "#7a7a7a",
    "Silver":     "#a8a8a8",
    "Light Grey": "#c8c8c8",
    "White":      "#f5f5f5",
}

# Colour hex values for desktop decors
DESKTOP_COLOURS = {
    "Black":                "#1a1a1a",
    "Soft Black":           "#2c2c2c",
    "Anthracite":           "#3d3d3d",
    "Graphite":             "#4a4a4a",
    "Stone":                "#8a8a7a",
    "Cashmere":             "#c8b89a",
    "Light Grey":           "#c8c8c8",
    "White":                "#f5f5f5",
    "Anthracite Sherman Oak":"#5a4a3a",
    "Natural Dijon Walnut": "#8b6914",
    "Grey Nebraska Oak":    "#7a7a6a",
    "Timber":               "#a0724a",
    "Beech":                "#c8a060",
    "Brown Oak":            "#7a4a20",
    "Natural Oak":          "#c8904a",
    "Maple":                "#d4a855",
    "Cascina Pine":         "#c8b080",
    "Dark Concrete":        "#6a6a6a",
    "Ferro Bronze":         "#6a5040",
    "Light Concrete":       "#b0b0a8",
}


def hex_to_rgb(hex_colour):
    """Convert hex colour string to RGB tuple (0-1 range for ReportLab)."""
    hex_colour = hex_colour.lstrip("#")
    r, g, b = tuple(int(hex_colour[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    return colors.Color(r, g, b)


def generate_pdf(width_mm: int, depth_mm: int, frame_finish: str, desktop_decor: str) -> bytes:
    """
    Generate a PDF specification sheet for a bespoke Advance desk.
    Returns the PDF as bytes.
    """
    buffer = io.BytesIO()
    w, h = A4  # 595 x 842 points
    c = canvas.Canvas(buffer, pagesize=A4)

    # ── Brand colours ──────────────────────────────────────────────────────────
    lavoro_dark = colors.HexColor("#1a1a1a")
    lavoro_mid  = colors.HexColor("#555555")
    lavoro_light = colors.HexColor("#f0f0f0")
    lavoro_accent = colors.HexColor("#c8a060")  # warm gold accent

    frame_col   = hex_to_rgb(FRAME_COLOURS.get(frame_finish, "#555555"))
    desktop_col = hex_to_rgb(DESKTOP_COLOURS.get(desktop_decor, "#c8a060"))

    # ── Header bar ─────────────────────────────────────────────────────────────
    c.setFillColor(lavoro_dark)
    c.rect(0, h - 60*mm, w, 60*mm, fill=1, stroke=0)

    # Logo text (stand-in for actual logo)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(20*mm, h - 35*mm, "LAVORO")
    c.setFont("Helvetica", 10)
    c.drawString(20*mm, h - 44*mm, "DESIGN")

    # Product name in header
    c.setFont("Helvetica-Bold", 18)
    c.drawRightString(w - 20*mm, h - 30*mm, "ADVANCE")
    c.setFont("Helvetica", 10)
    c.setFillColor(lavoro_accent)
    c.drawRightString(w - 20*mm, h - 40*mm, "Height Adjustable Desk")
    c.setFillColor(colors.white)
    c.drawRightString(w - 20*mm, h - 50*mm, "Bespoke Specification")

    # ── Bespoke badge ──────────────────────────────────────────────────────────
    c.setFillColor(lavoro_accent)
    c.roundRect(20*mm, h - 80*mm, 60*mm, 14*mm, 3*mm, fill=1, stroke=0)
    c.setFillColor(lavoro_dark)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(50*mm, h - 74*mm, "BESPOKE CONFIGURATION")

    # ── Desk illustration (schematic top-view) ─────────────────────────────────
    # Draw a simple top-down desk schematic scaled to proportions
    desk_area_x = 20*mm
    desk_area_y = h - 175*mm
    max_w = 120*mm
    max_d = 55*mm

    # Scale to fit the drawing area
    scale = min(max_w / width_mm, max_d / depth_mm)
    draw_w = width_mm * scale
    draw_d = depth_mm * scale

    # Desktop surface
    c.setFillColor(desktop_col)
    c.setStrokeColor(lavoro_mid)
    c.setLineWidth(1)
    c.rect(desk_area_x, desk_area_y, draw_w, draw_d, fill=1, stroke=1)

    # Leg positions (4 legs as small squares)
    leg_size = 5*mm
    leg_inset = 8*mm
    c.setFillColor(frame_col)
    c.setStrokeColor(lavoro_dark)
    c.setLineWidth(0.5)
    # Front-left, front-right, back-left, back-right
    for lx, ly in [
        (desk_area_x + leg_inset, desk_area_y + leg_inset),
        (desk_area_x + draw_w - leg_inset - leg_size, desk_area_y + leg_inset),
        (desk_area_x + leg_inset, desk_area_y + draw_d - leg_inset - leg_size),
        (desk_area_x + draw_w - leg_inset - leg_size, desk_area_y + draw_d - leg_inset - leg_size),
    ]:
        c.rect(lx, ly, leg_size, leg_size, fill=1, stroke=1)

    # Dimension annotations
    c.setStrokeColor(lavoro_mid)
    c.setFillColor(lavoro_mid)
    c.setLineWidth(0.5)
    c.setFont("Helvetica", 8)

    # Width arrow
    arr_y = desk_area_y - 8*mm
    c.line(desk_area_x, arr_y, desk_area_x + draw_w, arr_y)
    c.line(desk_area_x, arr_y - 2*mm, desk_area_x, arr_y + 2*mm)
    c.line(desk_area_x + draw_w, arr_y - 2*mm, desk_area_x + draw_w, arr_y + 2*mm)
    c.drawCentredString(desk_area_x + draw_w / 2, arr_y - 5*mm, f"{width_mm}mm")

    # Depth arrow
    arr_x = desk_area_x + draw_w + 8*mm
    c.line(arr_x, desk_area_y, arr_x, desk_area_y + draw_d)
    c.line(arr_x - 2*mm, desk_area_y, arr_x + 2*mm, desk_area_y)
    c.line(arr_x - 2*mm, desk_area_y + draw_d, arr_x + 2*mm, desk_area_y + draw_d)
    c.saveState()
    c.translate(arr_x + 5*mm, desk_area_y + draw_d / 2)
    c.rotate(90)
    c.drawCentredString(0, 0, f"{depth_mm}mm")
    c.restoreState()

    # ── Configuration summary ──────────────────────────────────────────────────
    summary_y = h - 195*mm
    c.setFillColor(lavoro_light)
    c.rect(20*mm, summary_y - 40*mm, w - 40*mm, 42*mm, fill=1, stroke=0)

    c.setFillColor(lavoro_dark)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(25*mm, summary_y - 5*mm, "YOUR CONFIGURATION")

    items = [
        ("Width",          f"{width_mm} mm"),
        ("Depth",          f"{depth_mm} mm"),
        ("Frame Finish",   frame_finish),
        ("Desktop Decor",  desktop_decor),
    ]
    col_x = [25*mm, 80*mm, 130*mm, 185*mm]
    c.setFont("Helvetica", 8)
    c.setFillColor(lavoro_mid)
    for i, (label, value) in enumerate(items):
        x = col_x[i] if i < len(col_x) else 25*mm
        c.drawString(x, summary_y - 18*mm, label.upper())
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(lavoro_dark)
        c.drawString(x, summary_y - 27*mm, value)
        c.setFont("Helvetica", 8)
        c.setFillColor(lavoro_mid)

    # Colour swatches
    swatch_y = summary_y - 34*mm
    c.setFillColor(frame_col)
    c.setStrokeColor(lavoro_mid)
    c.setLineWidth(0.5)
    c.rect(80*mm, swatch_y, 8*mm, 4*mm, fill=1, stroke=1)
    c.setFillColor(desktop_col)
    c.rect(130*mm, swatch_y, 8*mm, 4*mm, fill=1, stroke=1)

    # ── Technical specifications table ─────────────────────────────────────────
    table_y = summary_y - 50*mm

    c.setFillColor(lavoro_dark)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(20*mm, table_y, "TECHNICAL SPECIFICATIONS")

    c.setLineWidth(0.5)
    c.setStrokeColor(lavoro_light)
    c.line(20*mm, table_y - 2*mm, w - 20*mm, table_y - 2*mm)

    specs = [
        ("Desktop Width",         f"{width_mm} mm (bespoke)"),
        ("Desktop Depth",         f"{depth_mm} mm (bespoke)"),
        ("Height Range",          "625 – 1285 mm"),
        ("Frame Width Adjustment","1150 – 1740 mm"),
        ("Desktop Material",      "25mm MFC"),
        ("Desktop Edging",        "2mm ABS"),
        ("Load Capacity",         "120 kg"),
        ("Motor Type",            "Dual Motor"),
        ("Speed",                 "40 mm per second"),
        ("Standby Power",         "< 0.3W"),
        ("Max Operational Power", "300W"),
        ("Noise Level",           "< 42 dB"),
        ("Anti-Collision",        "Yes"),
        ("Guarantee",             "10 Years (frame & desktop)"),
        ("Compliance",            "UKCA & CE, FSC® Certified"),
    ]

    row_h = 7*mm
    col1_x = 20*mm
    col2_x = 110*mm
    c.setFont("Helvetica", 9)

    for i, (label, value) in enumerate(specs):
        row_y = table_y - 10*mm - i * row_h
        if row_y < 25*mm:
            break
        if i % 2 == 0:
            c.setFillColor(lavoro_light)
            c.rect(col1_x, row_y - 1*mm, w - 40*mm, row_h, fill=1, stroke=0)
        c.setFillColor(lavoro_mid)
        c.setFont("Helvetica", 8)
        c.drawString(col1_x + 3*mm, row_y + 2*mm, label)
        c.setFillColor(lavoro_dark)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(col2_x, row_y + 2*mm, value)

    # ── Footer ─────────────────────────────────────────────────────────────────
    c.setFillColor(lavoro_dark)
    c.rect(0, 0, w, 18*mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica", 7)
    c.drawString(20*mm, 10*mm, "Lavoro Design  |  lavorodesign.com  |  0330 133 1112  |  info@lavorodesign.com")
    c.setFillColor(lavoro_accent)
    c.drawRightString(w - 20*mm, 10*mm, "This document was generated with bespoke dimensions.")

    c.save()
    return buffer.getvalue()
