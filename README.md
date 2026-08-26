# KHANAN-NETRA

**AI-Powered Satellite Mining Intelligence & Surveillance** — a student-friendly, local-first prototype for mining-risk screening. It is deliberately built around **synthetic DEMO DATA** so it can be shown without cloud accounts, paid APIs, or satellite credentials.

## What it does

The dashboard simulates the workflow: satellite observations → Random Forest-ready candidate data → mining probability → boundary/permit screening → explainable risk score → field-verification report. It includes an interactive map, filters, detection evidence dialog, activity chart, alert panel, legal/protected/community overlays, PDF report generation, and KML/GPX export.

It never treats an AI score as proof of unlawful activity. The interface uses the wording “high-risk location requiring field verification.”

## Quick start (Windows / VS Code)

```powershell or vs code
cd khanan-netra
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:8000` if the browser does not open automatically. Press `Ctrl+C` to stop. The dashboard’s base map and charts use public CDN resources; all detections, boundaries and exports remain local.

## Project layout

```text
khanan-netra/
  backend/app/       FastAPI API, synthetic dataset, report/export routes
  frontend/          Responsive control-room dashboard (Leaflet + Chart.js)
  exports/           Generated reports (created on first report request)
  data/demo/         Reserved for future CSV/raster demonstration inputs
  ml/                Reserved for Random Forest training/prediction modules
  run_demo.py        One-command demo launcher
```

## API and features

- `GET /api/detections` accepts `status`, `risk`, `min_confidence`, and `min_area` filters.
- `GET /api/report` creates a PDF evidence-support report.
- `GET /api/export/kml` and `GET /api/export/gpx` export field locations.
- `GET /api/boundaries` supplies demo permit, protected and community polygons.

## Data and model path

The current dataset is generated deterministically in `backend/app/demo_data.py` and marked synthetic throughout. It models Sentinel-1/2-style confidence and surface-change fields, areas, timestamps, legal status, and history. In a production extension, ingest preprocessed Sentinel observations into SQLite, train a scikit-learn Random Forest with labelled mining/non-mining examples, replace `build_detections()`, and perform actual GeoPandas/Shapely boundary intersections. Google Earth Engine or Copernicus APIs are intentionally optional and are not required for this demo.

## Future architecture

The navigation shows intentionally non-operational placeholders for **Drone Verification — Coming Soon** and **Truck Intelligence — Coming Soon**. A future module can attach drone photos/photogrammetry/3D excavation estimates and truck GPS, RFID, e-Challan, declared/actual load and checkpoint events. The intended evidence path is: Satellite detection → drone verification → 3D excavation analysis → transport cross-check → AI evidence fusion.

## Limitations

This prototype is a decision-support demonstration, not a real monitoring service or legal determination. Its positions, boundaries, probabilities, alerts, areas, and trends are synthetic. Validate model performance and authoritative permit/protected-area sources before operational use.
