"""
IFC Generator for Lavoro Design
Generates an IFC 2x3 file for the bespoke desk using ifcopenshell.
"""
import io
import uuid
import time
import ifcopenshell
import ifcopenshell.api


def new_guid():
    return ifcopenshell.guid.compress(uuid.uuid4().hex)


def generate_ifc(width_mm: int, depth_mm: int, frame_finish: str, desktop_decor: str) -> bytes:
    """
    Generate an IFC 2x3 file for the bespoke Advance desk.
    Returns the IFC content as bytes.
    """
    # Convert mm to metres for IFC
    w = width_mm / 1000.0
    d = depth_mm / 1000.0
    h = 0.950  # standard height 950mm

    ifc = ifcopenshell.file(schema="IFC2X3")

    # ── Owner / Organisation ───────────────────────────────────────────────────
    person = ifc.createIfcPerson(None, "Design", "Lavoro", None, None, None, None, None)
    org    = ifc.createIfcOrganization(None, "Lavoro Design", None, None, None)
    p_and_o = ifc.createIfcPersonAndOrganization(person, org, None)
    app    = ifc.createIfcApplication(org, "1.0", "Lavoro Configurator", "LavoroConfig")
    owner  = ifc.createIfcOwnerHistory(p_and_o, app, None, "ADDED", None, p_and_o, app, int(time.time()))

    # ── Units ──────────────────────────────────────────────────────────────────
    length_unit  = ifc.createIfcSIUnit(None, "LENGTHUNIT",  None, "METRE")
    area_unit    = ifc.createIfcSIUnit(None, "AREAUNIT",    None, "SQUARE_METRE")
    volume_unit  = ifc.createIfcSIUnit(None, "VOLUMEUNIT",  None, "CUBIC_METRE")
    unit_assign  = ifc.createIfcUnitAssignment([length_unit, area_unit, volume_unit])

    # ── Geometric context ──────────────────────────────────────────────────────
    origin3d = ifc.createIfcCartesianPoint((0.0, 0.0, 0.0))
    axis2p3d = ifc.createIfcAxis2Placement3D(origin3d, None, None)
    geo_ctx  = ifc.createIfcGeometricRepresentationContext(
        None, "Model", 3, 1e-5, axis2p3d, None
    )

    # ── Project ────────────────────────────────────────────────────────────────
    project = ifc.createIfcProject(
        new_guid(), owner,
        "Lavoro Design - Advance Desk (Bespoke)", None, None, None, None,
        [geo_ctx], unit_assign
    )

    # ── Site / Building / Storey ───────────────────────────────────────────────
    site_placement  = ifc.createIfcLocalPlacement(None, axis2p3d)
    site  = ifc.createIfcSite(new_guid(), owner, None, None, None, site_placement, None, None, "ELEMENT", None, None, None, None, None)
    bldg_placement  = ifc.createIfcLocalPlacement(site_placement, axis2p3d)
    bldg  = ifc.createIfcBuilding(new_guid(), owner, None, None, None, bldg_placement, None, None, "ELEMENT", None, None, None)
    storey_placement = ifc.createIfcLocalPlacement(bldg_placement, axis2p3d)
    storey = ifc.createIfcBuildingStorey(new_guid(), owner, None, None, None, storey_placement, None, None, "ELEMENT", 0.0)

    ifc.createIfcRelAggregates(new_guid(), owner, None, None, project, [site])
    ifc.createIfcRelAggregates(new_guid(), owner, None, None, site, [bldg])
    ifc.createIfcRelAggregates(new_guid(), owner, None, None, bldg, [storey])

    # ── Desk geometry: desktop slab ────────────────────────────────────────────
    slab_t = 0.025  # 25mm in metres
    leg_h  = h - slab_t

    def make_box_shape(sx, sy, sz, tx=0.0, ty=0.0, tz=0.0):
        """Create an IfcExtrudedAreaSolid box of size sx,sy,sz at translation tx,ty,tz."""
        pt = ifc.createIfcCartesianPoint((tx, ty, tz))
        placement = ifc.createIfcAxis2Placement3D(pt, None, None)
        rect = ifc.createIfcRectangleProfileDef("AREA", None, ifc.createIfcAxis2Placement2D(
            ifc.createIfcCartesianPoint((sx / 2, sy / 2)), None
        ), sx, sy)
        direction = ifc.createIfcDirection((0.0, 0.0, 1.0))
        solid = ifc.createIfcExtrudedAreaSolid(rect, placement, direction, sz)
        return solid

    # Desktop slab
    desktop_solid = make_box_shape(w, d, slab_t, 0.0, 0.0, leg_h)
    desktop_rep = ifc.createIfcShapeRepresentation(geo_ctx, "Body", "SweptSolid", [desktop_solid])
    desktop_shape = ifc.createIfcProductDefinitionShape(None, None, [desktop_rep])

    desk_placement = ifc.createIfcLocalPlacement(storey_placement, axis2p3d)

    desk = ifc.createIfcFurnishingElement(
        new_guid(), owner,
        f"Advance {width_mm}x{depth_mm}mm Dual Motor Desk",
        f"Lavoro Design Advance - Bespoke {width_mm}mm W x {depth_mm}mm D",
        None, desk_placement, desktop_shape, None
    )

    ifc.createIfcRelContainedInSpatialStructure(
        new_guid(), owner, None, None, [desk], storey
    )

    # ── Property set: bespoke configuration ───────────────────────────────────
    props = [
        ifc.createIfcPropertySingleValue("Width_mm",       None, ifc.createIfcLengthMeasure(float(width_mm)),  None),
        ifc.createIfcPropertySingleValue("Depth_mm",       None, ifc.createIfcLengthMeasure(float(depth_mm)),  None),
        ifc.createIfcPropertySingleValue("Height_mm",      None, ifc.createIfcLengthMeasure(950.0),            None),
        ifc.createIfcPropertySingleValue("Frame_Finish",   None, ifc.createIfcLabel(frame_finish),             None),
        ifc.createIfcPropertySingleValue("Desktop_Decor",  None, ifc.createIfcLabel(desktop_decor),            None),
        ifc.createIfcPropertySingleValue("Manufacturer",   None, ifc.createIfcLabel("Lavoro Design"),          None),
        ifc.createIfcPropertySingleValue("Product_Range",  None, ifc.createIfcLabel("Advance"),                None),
        ifc.createIfcPropertySingleValue("Guarantee",      None, ifc.createIfcLabel("10 Years"),               None),
        ifc.createIfcPropertySingleValue("Load_Capacity_kg", None, ifc.createIfcReal(120.0),                   None),
    ]
    pset = ifc.createIfcPropertySet(new_guid(), owner, "Pset_LavoroAdvance", None, props)
    ifc.createIfcRelDefinesByProperties(new_guid(), owner, None, None, [desk], pset)

    # ── Serialise ──────────────────────────────────────────────────────────────
    tmp_path = f"/tmp/lavoro_advance_{width_mm}x{depth_mm}.ifc"
    ifc.write(tmp_path)
    with open(tmp_path, "rb") as f:
        return f.read()
