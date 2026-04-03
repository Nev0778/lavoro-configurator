"""
3D Mesh Generator for Lavoro Design
Generates OBJ and STL files of the desk with bespoke dimensions using trimesh.
The desk is modelled as separate components: desktop slab + 4 legs.
"""
import io
import numpy as np
import trimesh


# Standard base dimensions (from the existing files: 1200 x 700mm)
BASE_WIDTH  = 1200.0  # mm
BASE_DEPTH  =  700.0  # mm
BASE_HEIGHT =  950.0  # mm (height at standard position)

# Desktop slab thickness
SLAB_THICKNESS = 25.0  # mm

# Leg dimensions (each leg column)
LEG_W = 80.0   # mm
LEG_D = 80.0   # mm
LEG_H = BASE_HEIGHT - SLAB_THICKNESS  # height of legs below desktop

# Leg inset from edge
LEG_INSET = 60.0  # mm


def _make_box(width, depth, height, origin=(0, 0, 0)):
    """Create a box mesh at a given origin (x, y, z)."""
    box = trimesh.creation.box(extents=[width, depth, height])
    # trimesh centres the box at origin; shift so bottom-left-front is at origin
    box.apply_translation([
        origin[0] + width / 2,
        origin[1] + depth / 2,
        origin[2] + height / 2
    ])
    return box


def build_desk_mesh(width_mm: float, depth_mm: float) -> trimesh.Scene:
    """
    Build a parametric desk mesh with the given top dimensions.
    The desktop slab scales with width and depth.
    The legs are repositioned accordingly but keep their cross-section.
    """
    w = float(width_mm)
    d = float(depth_mm)

    meshes = []

    # ── Desktop slab ──────────────────────────────────────────────────────────
    desktop = _make_box(w, d, SLAB_THICKNESS, origin=(0, 0, LEG_H))
    meshes.append(desktop)

    # ── Four legs ─────────────────────────────────────────────────────────────
    leg_positions = [
        (LEG_INSET,              LEG_INSET),
        (w - LEG_INSET - LEG_W,  LEG_INSET),
        (LEG_INSET,              d - LEG_INSET - LEG_D),
        (w - LEG_INSET - LEG_W,  d - LEG_INSET - LEG_D),
    ]
    for lx, ly in leg_positions:
        leg = _make_box(LEG_W, LEG_D, LEG_H, origin=(lx, ly, 0))
        meshes.append(leg)

    # ── Crossbar (centre beam under desktop) ──────────────────────────────────
    bar_w = w - 2 * LEG_INSET - LEG_W
    bar_h = 40.0
    bar_d = 30.0
    bar_z = LEG_H - bar_h - 20.0
    crossbar = _make_box(bar_w, bar_d, bar_h,
                         origin=(LEG_INSET + LEG_W, d / 2 - bar_d / 2, bar_z))
    meshes.append(crossbar)

    # ── Combine into a scene ───────────────────────────────────────────────────
    scene = trimesh.scene.scene.Scene()
    for i, mesh in enumerate(meshes):
        scene.add_geometry(mesh, node_name=f"part_{i}")

    return scene


def generate_obj(width_mm: int, depth_mm: int, frame_finish: str, desktop_decor: str) -> bytes:
    """Generate an OBJ file and return as bytes."""
    scene = build_desk_mesh(width_mm, depth_mm)
    # Export as OBJ
    obj_bytes = scene.export(file_type="obj")
    if isinstance(obj_bytes, str):
        return obj_bytes.encode("utf-8")
    return obj_bytes


def generate_stl(width_mm: int, depth_mm: int, frame_finish: str, desktop_decor: str) -> bytes:
    """Generate a binary STL file and return as bytes."""
    scene = build_desk_mesh(width_mm, depth_mm)
    # Merge all meshes for STL export
    combined = trimesh.util.concatenate(list(scene.geometry.values()))
    stl_bytes = combined.export(file_type="stl")
    return stl_bytes
