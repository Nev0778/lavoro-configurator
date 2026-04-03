# Lavoro Design Parametric Revit Families — Key Findings

## Desk Models (8 total)
| Model | Category | Frame Type | Height Range | Max Load | Sizes |
|---|---|---|---|---|---|
| Advance | Height Adjustable | Dual Motor | 625–1285mm | 120kg | 8 (1200x700 to 2000x800) |
| Advance Corner | Height Adjustable | Triple Motor | 625–1285mm | 160kg | 2 (1600x1600 to 1800x1600) |
| Advance Mini | Height Adjustable | Dual Motor | 625–1285mm | 120kg | 3 (1000x600 to 1200x700) |
| Duo | Height Adjustable | Quad Motor | 625–1285mm | 240kg | 6 (1200x1450 to 1600x1650) |
| Five | Height Adjustable | Cantilever | 625–1285mm | 80kg | 4 (1200x700 to 1800x700) |
| Crown | Height Adjustable | Dual Motor | 625–1285mm | 120kg | 4 (1400x800 to 2000x800) |
| Lanto | Fixed Height | 4-Leg | 730mm | 100kg | 6 (1200x700 to 1800x800) |
| Firmo | Fixed Height | 4-Leg | 730mm | 100kg | 9 (Single & Dual) |

## Type Catalogue Parameters (pre-defined per type)
- **Width** (Length) — overall tabletop width
- **Depth** (Length) — overall tabletop depth
- **Height_Max** (Length) — max height / fixed height
- **Height_Min** (Length) — min height (= Height_Max for fixed desks)
- **Frame_Colour** — Black, White, Anthracite, Raw Steel, Silver, Light Grey
- **Product_SKU** and **Product_Name** — for scheduling

## Instance Parameter (NOT in type catalogue)
- **Top_Decor** — instance parameter, set per-desk without creating new types
  - Examples: Anthracite Sherman Oak, Natural Dijon Walnut

## Dimensional Parameters in Family
- Width, Depth, Height_Max, Height_Min, Top_Thickness (25mm or 35mm)

## Frame Parameters
- Leg_Column_Width, Leg_Column_Depth, Crossbeam_Depth

## Dynamo Scripts (.dyn) — one per desk model
- Inputs: desk_width_mm, desk_depth_mm, desk_height_mm, frame_colour, top_decor, placement_x_mm, placement_y_mm
- Automatically loads family, selects correct type from catalogue, places desk, applies instance params

## Manufacturer Metadata (embedded in all families)
- Manufacturer: Lavoro Design
- Warranty: 5 Year
- Load Capacity: varies by model
- Speed: 40 mm/s (height-adjustable models)

## COMPATIBILITY NOTES FOR CONFIGURATOR
- Frame_Colour values in RFA: Black, White, Anthracite, Raw Steel, Silver, Light Grey
  - NOTE: RFA uses "Anthracite" not "Anthracite Grey" — configurator needs to map this
  - NOTE: RFA does NOT include "Dark Grey" (RAL 7022) or "White" (RAL 9016) as separate entries — check zip
- Top_Decor is an INSTANCE parameter — the configurator-generated Type Catalog does NOT need to include it
  - The bespoke Type Catalog only needs: Width, Depth, Frame_Colour, Height_Max, Height_Min
- The configurator currently generates Width + Depth dynamically — this is CORRECT
- The configurator currently passes "frame" as the frame colour — needs to match RFA Frame_Colour values exactly
