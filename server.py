"""
Lavoro Design - Bespoke File Generator API
FastAPI backend that generates customised CAD/BIM/PDF files on demand.
"""
import os
import io
import zipfile
import tempfile
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Add generators directory to path
import sys
sys.path.insert(0, os.path.dirname(__file__))

from generators.pdf_generator import generate_pdf
from generators.dxf_generator import generate_dxf
from generators.mesh_generator import generate_obj, generate_stl
from generators.ifc_generator import generate_ifc
from generators.revit_catalog_generator import generate_revit_catalog

app = FastAPI(title="Lavoro Design File Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (the demo page)
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main demo page."""
    html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    with open(html_path, "r") as f:
        return HTMLResponse(content=f.read())


@app.get("/generate/pdf")
async def get_pdf(
    width:   int = Query(1400, ge=800, le=2400, description="Desktop width in mm"),
    depth:   int = Query(700,  ge=600, le=900,  description="Desktop depth in mm"),
    frame:   str = Query("Black",       description="Frame finish colour"),
    desktop: str = Query("Natural Oak", description="Desktop decor"),
):
    """Generate and return a bespoke PDF specification sheet."""
    pdf_bytes = generate_pdf(width, depth, frame, desktop)
    filename = f"Lavoro-Advance-{width}x{depth}-Spec.pdf"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@app.get("/generate/dxf")
async def get_dxf(
    width:   int = Query(1400, ge=800, le=2400),
    depth:   int = Query(700,  ge=600, le=900),
    frame:   str = Query("Black"),
    desktop: str = Query("Natural Oak"),
):
    """Generate and return a bespoke AutoCAD DXF file (2D top view)."""
    dxf_bytes = generate_dxf(width, depth, frame, desktop)
    filename = f"Lavoro-Advance-{width}x{depth}-AutoCAD-2D.dxf"
    return StreamingResponse(
        io.BytesIO(dxf_bytes),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@app.get("/generate/obj")
async def get_obj(
    width:   int = Query(1400, ge=800, le=2400),
    depth:   int = Query(700,  ge=600, le=900),
    frame:   str = Query("Black"),
    desktop: str = Query("Natural Oak"),
):
    """Generate and return a bespoke OBJ 3D model."""
    obj_bytes = generate_obj(width, depth, frame, desktop)
    filename = f"Lavoro-Advance-{width}x{depth}-3D.obj"
    return StreamingResponse(
        io.BytesIO(obj_bytes),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@app.get("/generate/stl")
async def get_stl(
    width:   int = Query(1400, ge=800, le=2400),
    depth:   int = Query(700,  ge=600, le=900),
    frame:   str = Query("Black"),
    desktop: str = Query("Natural Oak"),
):
    """Generate and return a bespoke STL 3D model."""
    stl_bytes = generate_stl(width, depth, frame, desktop)
    filename = f"Lavoro-Advance-{width}x{depth}-3D.stl"
    return StreamingResponse(
        io.BytesIO(stl_bytes),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@app.get("/generate/ifc")
async def get_ifc(
    width:   int = Query(1400, ge=800, le=2400),
    depth:   int = Query(700,  ge=600, le=900),
    frame:   str = Query("Black"),
    desktop: str = Query("Natural Oak"),
):
    """Generate and return a bespoke IFC BIM file."""
    ifc_bytes = generate_ifc(width, depth, frame, desktop)
    filename = f"Lavoro-Advance-{width}x{depth}-BIM.ifc"
    return StreamingResponse(
        io.BytesIO(ifc_bytes),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@app.get("/generate/revit-catalog")
async def get_revit_catalog(
    width:   int = Query(1400, ge=800, le=2400),
    depth:   int = Query(700,  ge=600, le=900),
    frame:   str = Query("Black"),
    desktop: str = Query("Natural Oak"),
):
    """Generate a bespoke Revit Type Catalog and bundle it with the RFA in a ZIP."""
    txt_bytes = generate_revit_catalog(width, depth, frame, desktop)
    rfa_path = os.path.join(os.path.dirname(__file__), "static", "Lavoro_Design_Advance.rfa")
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"Lavoro_Design_Advance_{width}x{depth}_TypeCatalog.txt", txt_bytes)
        zf.write(rfa_path, "Lavoro_Design_Advance.rfa")
    zip_buffer.seek(0)
    filename = f"Lavoro-Advance-{width}x{depth}-Revit.zip"
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@app.get("/generate/all")
async def get_all_files(
    width:   int = Query(1400, ge=800, le=2400),
    depth:   int = Query(700,  ge=600, le=900),
    frame:   str = Query("Black"),
    desktop: str = Query("Natural Oak"),
):
    """Generate all file types and return as a ZIP archive."""
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        # PDF
        zf.writestr(f"Lavoro-Advance-{width}x{depth}-Spec.pdf",
                    generate_pdf(width, depth, frame, desktop))
        # DXF
        zf.writestr(f"Lavoro-Advance-{width}x{depth}-AutoCAD-2D.dxf",
                    generate_dxf(width, depth, frame, desktop))
        # OBJ
        zf.writestr(f"Lavoro-Advance-{width}x{depth}-3D.obj",
                    generate_obj(width, depth, frame, desktop))
        # STL
        zf.writestr(f"Lavoro-Advance-{width}x{depth}-3D.stl",
                    generate_stl(width, depth, frame, desktop))
        # IFC
        zf.writestr(f"Lavoro-Advance-{width}x{depth}-BIM.ifc",
                    generate_ifc(width, depth, frame, desktop))
        # Revit type catalog + RFA family file
        zf.writestr(f"Lavoro_Design_Advance_{width}x{depth}_TypeCatalog.txt",
                    generate_revit_catalog(width, depth, frame, desktop))
        rfa_path = os.path.join(os.path.dirname(__file__), "static", "Lavoro_Design_Advance.rfa")
        zf.write(rfa_path, "Lavoro_Design_Advance.rfa")

    zip_buffer.seek(0)
    filename = f"Lavoro-Advance-{width}x{depth}-BespokeFiles.zip"
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
