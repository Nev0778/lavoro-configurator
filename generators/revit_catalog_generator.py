"""
Revit Family Type Catalog Generator for Lavoro Design
Generates a .txt Revit Type Catalog file that instructs Revit
to build the Advance desk family at bespoke dimensions.

Parameter names match the official Lavoro_Design_Advance.rfa exactly,
as defined in Lavoro_Design_Advance_Type_Catalog.txt.
Dimensions are in decimal feet (Revit's internal unit for length parameters).
"""

MM_TO_FT = 1 / 304.8  # 1mm = 1/304.8 feet


def mm_to_ft(mm: float) -> str:
    """Convert millimetres to decimal feet, formatted to 6 decimal places."""
    return f"{mm * MM_TO_FT:.6f}"


def generate_revit_catalog(width_mm: int, depth_mm: int, frame_finish: str, desktop_decor: str) -> bytes:
    """
    Generate a Revit Family Type Catalog (.txt) file.
    This companion file, when placed alongside Lavoro_Design_Advance.rfa,
    tells Revit to create a type with the specified bespoke dimensions.

    Returns the file content as bytes (UTF-16 LE, as Revit expects).
    """
    # Fixed standard values from the official Lavoro Advance catalog
    height_max_mm = 1285   # 4.215879 ft
    height_min_mm = 625    # 2.050525 ft
    top_thickness_mm = 35  # 0.114829 ft
    leg_col_w_mm = 90      # 0.295276 ft
    leg_col_d_mm = 90      # 0.295276 ft
    crossbeam_d_mm = 90    # 0.295276 ft

    # Build the type name
    type_name = f"Advance_{width_mm}x{depth_mm}_{frame_finish.replace(' ', '')}"
    product_name = f"Advance {width_mm} x {depth_mm}mm Height Adjustable Desk"
    sku = f"ADVS-{width_mm}{depth_mm}-{frame_finish[:2].upper()}"

    # Header row — parameter names and types exactly as in the official catalog
    header = (
        ","
        "Width##length##length,"
        "Depth##length##length,"
        "Height_Max##length##length,"
        "Height_Min##length##length,"
        "Top_Thickness##length##length,"
        "Leg_Column_Width##length##length,"
        "Leg_Column_Depth##length##length,"
        "Crossbeam_Depth##length##length,"
        "Frame_Colour##other##text,"
        "Product_Name##other##text,"
        "Product_SKU##other##text,"
        "Manufacturer##other##text,"
        "Desk_Type##other##text,"
        "Height_Adjustable##other##yesno,"
        "Load_Capacity_kg##other##number,"
        "Speed_mm_s##other##number,"
        "Warranty##other##text"
    )

    # Data row — bespoke width/depth, all other values from official standard
    data_row = (
        f'"{type_name}",'
        f"{mm_to_ft(width_mm)},"
        f"{mm_to_ft(depth_mm)},"
        f"{mm_to_ft(height_max_mm)},"
        f"{mm_to_ft(height_min_mm)},"
        f"{mm_to_ft(top_thickness_mm)},"
        f"{mm_to_ft(leg_col_w_mm)},"
        f"{mm_to_ft(leg_col_d_mm)},"
        f"{mm_to_ft(crossbeam_d_mm)},"
        f'"{frame_finish}",'
        f'"{product_name}",'
        f'"{sku}",'
        '"Lavoro Design",'
        '"Dual Motor",'
        "1,"
        "120,"
        "40,"
        '"5 Year"'
    )

    content = header + "\n" + data_row + "\n"
    # Revit Type Catalogs must be UTF-16 LE encoded
    return content.encode("utf-16-le")
