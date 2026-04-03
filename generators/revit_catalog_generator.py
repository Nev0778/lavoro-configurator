"""
Revit Family Type Catalog Generator for Lavoro Design
Generates a .txt Revit Type Catalog file that instructs Revit
to build the Advance desk family at bespoke dimensions.
"""


def generate_revit_catalog(width_mm: int, depth_mm: int, frame_finish: str, desktop_decor: str) -> bytes:
    """
    Generate a Revit Family Type Catalog (.txt) file.
    This companion file, when placed alongside the .rfa file,
    tells Revit to create a type with the specified bespoke dimensions.

    Returns the file content as bytes (UTF-16 LE, as Revit expects).
    """
    height_mm = 950  # standard height
    depth_slab = 25  # desktop thickness mm

    type_name = f"Advance {width_mm}x{depth_mm}mm - {frame_finish} Frame - {desktop_decor} Top"

    # Revit Type Catalog format:
    # First line = header row with parameter names and types
    # Subsequent lines = type name followed by parameter values
    header = (
        "##TYPECATALOG\t"
        "Width##LENGTH##millimeters\t"
        "Depth##LENGTH##millimeters\t"
        "Height##LENGTH##millimeters\t"
        "Desktop_Thickness##LENGTH##millimeters\t"
        "Frame_Finish##OTHER##\t"
        "Desktop_Decor##OTHER##"
    )

    data_row = (
        f"{type_name}\t"
        f"{width_mm}\t"
        f"{depth_mm}\t"
        f"{height_mm}\t"
        f"{depth_slab}\t"
        f"{frame_finish}\t"
        f"{desktop_decor}"
    )

    content = header + "\n" + data_row + "\n"

    # Revit Type Catalogs are UTF-16 LE encoded
    return content.encode("utf-16-le")
