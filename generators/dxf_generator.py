"""
AutoCAD DXF Generator for Lavoro Design
Generates a 2D DXF drawing of the desk top-view with bespoke dimensions.
"""
import io
import ezdxf
from ezdxf import units


def generate_dxf(width_mm: int, depth_mm: int, frame_finish: str, desktop_decor: str) -> bytes:
    """
    Generate a 2D AutoCAD DXF file representing the desk top-view.
    All dimensions are in millimetres.
    Returns the DXF as bytes.
    """
    doc = ezdxf.new(dxfversion="R2010")
    doc.units = units.MM

    # ── Layers ─────────────────────────────────────────────────────────────────
    doc.layers.add("DESKTOP",    color=7)   # white/black
    doc.layers.add("FRAME",      color=8)   # dark grey
    doc.layers.add("DIMENSIONS", color=3)   # green
    doc.layers.add("TEXT",       color=7)
    doc.layers.add("CENTRE",     color=1)   # red

    msp = doc.modelspace()

    w = float(width_mm)
    d = float(depth_mm)

    # ── Desktop outline ────────────────────────────────────────────────────────
    msp.add_lwpolyline(
        [(0, 0), (w, 0), (w, d), (0, d), (0, 0)],
        dxfattribs={"layer": "DESKTOP", "lineweight": 50}
    )

    # ── Leg positions (4 legs, 80x80mm each, inset 60mm) ──────────────────────
    leg_size = 80.0
    leg_inset = 60.0
    leg_positions = [
        (leg_inset,          leg_inset),
        (w - leg_inset - leg_size, leg_inset),
        (leg_inset,          d - leg_inset - leg_size),
        (w - leg_inset - leg_size, d - leg_inset - leg_size),
    ]
    for lx, ly in leg_positions:
        msp.add_lwpolyline(
            [(lx, ly), (lx + leg_size, ly), (lx + leg_size, ly + leg_size),
             (lx, ly + leg_size), (lx, ly)],
            dxfattribs={"layer": "FRAME", "lineweight": 30}
        )

    # ── Centre lines ───────────────────────────────────────────────────────────
    # Load the CENTER linetype from the standard linetypes
    try:
        doc.linetypes.load_ltype_file("center", ezdxf.options.default_linetypes_directory)
    except Exception:
        pass  # Use default linetype if CENTER not available
    msp.add_line((w / 2, -50), (w / 2, d + 50),
                 dxfattribs={"layer": "CENTRE", "lineweight": 13})
    msp.add_line((-50, d / 2), (w + 50, d / 2),
                 dxfattribs={"layer": "CENTRE", "lineweight": 13})

    # ── Width dimension ────────────────────────────────────────────────────────
    dim_offset = -80.0
    msp.add_linear_dim(
        base=(0, dim_offset),
        p1=(0, 0),
        p2=(w, 0),
        dimstyle="EZDXF",
        dxfattribs={"layer": "DIMENSIONS"}
    ).render()

    # ── Depth dimension ────────────────────────────────────────────────────────
    msp.add_linear_dim(
        base=(w + 80, 0),
        p1=(w, 0),
        p2=(w, d),
        angle=90,
        dimstyle="EZDXF",
        dxfattribs={"layer": "DIMENSIONS"}
    ).render()

    # ── Title block text ───────────────────────────────────────────────────────
    title_y = d + 120
    msp.add_text(
        "LAVORO DESIGN - ADVANCE HEIGHT ADJUSTABLE DESK",
        dxfattribs={"layer": "TEXT", "height": 20, "insert": (0, title_y)}
    )
    msp.add_text(
        f"BESPOKE: {width_mm}mm W x {depth_mm}mm D  |  Frame: {frame_finish}  |  Desktop: {desktop_decor}",
        dxfattribs={"layer": "TEXT", "height": 12, "insert": (0, title_y - 30)}
    )
    msp.add_text(
        "TOP VIEW - ALL DIMENSIONS IN MILLIMETRES",
        dxfattribs={"layer": "TEXT", "height": 10, "insert": (0, title_y - 55)}
    )
    msp.add_text(
        "lavorodesign.com  |  0330 133 1112",
        dxfattribs={"layer": "TEXT", "height": 8, "insert": (0, title_y - 70)}
    )

    # ── Write to buffer ────────────────────────────────────────────────────────
    buffer = io.StringIO()
    doc.write(buffer)
    return buffer.getvalue().encode("utf-8")
