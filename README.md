# KHANAN-NETRA

**Satellite Mining Intelligence** is a local-first FastAPI prototype for triaging mining-related land-change evidence. It is designed for a 3–5 minute hackathon walkthrough while being candid about its data and model limitations.

It does **not** claim that satellite or AI output proves illegal mining. It presents a mining-related change, spatial permit screening, and evidence-fusion score that require field verification.

## What is implemented

- Satellite-first Leaflet workspace with Satellite, Streets, and Terrain base layers.
- Search for a place, district, state, mining demo location, or `latitude, longitude`; a local Sikkim fallback works offline.
- Draw a rectangle or polygon AOI, calculate area/centre, validate it, and store it in local SQLite.
- 30/60/90-day monitoring, cloud filtering, time slider, play/pause, and earliest-vs-latest comparison.
- Geographic mining/change **polygons** instead of synthetic point dots, permit/protected overlay, calculated overlap, and careful wording such as “potentially unauthorized / requires verification.”
- Configurable, explainable risk engine that fuses mining probability, change, permit/protected overlap, area, history, demo drone mismatch, and simulated transport anomalies.
- Working investigation case view, sample Three.js mine model, drone-image upload validation, truck route map, RFID, e-Challan, and weighbridge evidence.
- PDF evidence report plus KML, GPX, GeoJSON, and CSV exports.
- Data Mode that searches the free public Sentinel-2 Planetary Computer STAC catalogue. It returns only genuine catalogue metadata and deliberately does **not** invent model polygons when raster assets are unavailable.

## Fast start on Windows

From this folder:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run_demo.py
```

Open `http://127.0.0.1:8000`. If PowerShell blocks activation, use:

```powershell
.\.venv\Scripts\python.exe run_demo.py
```

The API can also be started with:

```powershell
uvicorn backend.app.main:app --reload
```

`run.py` remains as a compatibility launcher.

## Suggested demonstration

1. Start the app; the dashboard loads the clearly labelled **DEMO DATA** workspace.
2. Search `Mining Area, Sikkim, India`.
3. Draw an AOI, or choose **Use sample AOI** for a repeatable offline walk-through.
4. Select **90 days** and **Run analysis**.
5. Play the observation timeline and select **Compare 90 days**.
6. Inspect mining/change polygons against permit and sensitive-zone layers.
7. Open the highest-risk case. Explain the scoring breakdown and the verification wording.
8. Open **Drone verification** for the labelled sample 3D survey and volume comparison.
9. Open **Truck intelligence** to inspect planned versus actual route and missing checkpoint.
10. Generate the PDF report or export KML / GPX / GeoJSON / CSV.

## Data modes and transparency

| Feature | Demo Mode | Data Mode |
|---|---|---|
| Satellite observations | Bundled deterministic fixtures, labelled `DEMO DATA` | Public Sentinel-2 catalogue metadata, labelled `REAL CATALOGUE DATA` |
| Detection polygons | Precomputed local demonstration output | Withheld until actual cached raster features are processed |
| Permit/protected boundaries | `DEMO DATA`, not official | Replace with authoritative GeoJSON before operational use |
| Drone | `SAMPLE / DEMO DATA` | Uploaded images are stored for review; no false live photogrammetry claim |
| Truck/GPS/RFID | `SIMULATED` / `DEMO DATA` | Adapter-ready local evidence API |

Offline networking failures are handled in the interface. Select **Demo Mode** and the full walkthrough still works without a satellite API, geocoder, drone processor, or GPS feed.

## Satellite and ML workflow

```text
AOI → observation/date/cloud filter → AOI clip + features → probability mask
    → connected regions → GeoJSON polygons → permit/protected screening
    → evidence fusion → field-verification case
```

The lightweight ML baseline is a documented scikit-learn Random Forest. Train it with labelled raster-derived samples:

```powershell
python ml/train.py --input data/demo/training_samples.csv
python ml/predict.py --features '{"blue":0.14,"green":0.18,"red":0.22,"nir":0.19,"swir1":0.36,"ndvi":-0.07,"ndwi":-0.11,"bare_soil":0.74,"temporal_difference":0.42,"sar_change":1.8,"slope":13}'
```

`data/demo/training_samples.csv` is intentionally tiny and only demonstrates the expected schema. It is not scientifically sufficient training data. For real deployments, derive features from cloud-masked Sentinel-2 (and optionally Sentinel-1/SAR) rasters, retain reproducible observation IDs/AOIs, calibrate the model, validate against held-out regional labels, and use Rasterio/GDAL/GeoPandas for production raster-to-vector processing.

## API

- `GET /api/health`, `GET /api/config`, `GET/POST /api/aoi`, `GET /api/geocode`
- `GET /api/satellite/observations`, `POST /api/satellite/analyze`
- `GET /api/detections`, `GET /api/detections/{id}`, `GET /api/permits`
- `GET /api/cases`, `POST /api/cases`, `GET /api/cases/{id}`, `GET /api/risk/{case_id}`
- `GET /api/drone/{case_id}`, `POST /api/drone/upload`
- `GET /api/trucks`, `GET /api/trucks/{id}/route`, `GET /api/rfid`, `GET /api/challans`, `GET /api/weighbridge`
- `GET /api/alerts`, `POST /api/reports/generate`
- `GET /api/export/kml`, `/gpx`, `/geojson`, `/csv`

## Layout

```text
backend/app/
  main.py                  FastAPI routes and evidence report
  database.py              SQLite schema/AOI/case persistence
  demo_data.py             Explicit, labelled offline fixtures
  services/                GIS, satellite, risk and truck services
data/
  boundaries/              Demo permit and sensitive-zone GeoJSON
  demo/                    Training samples
  drone/uploads/           Validated local review uploads (runtime)
ml/                        Random Forest training/prediction baseline
frontend/                  Satellite intelligence workspace
tests/                     AOI/GIS, filtering, risk and route checks
```

## Tests

```powershell
python -m unittest discover -s tests -v
```

Tests cover AOI validation and area, permit intersection, date/cloud filtering, risk bounds/breakdown, route deviation, and RFID/transport evidence. Run the app endpoints for an end-to-end report/export smoke test.

## Limitations and next steps

This is a decision-support prototype. Demo locations, observations, detections, permit boundaries, drone survey, and transport records are not real. Data Mode supports free public catalogue discovery but does not download large imagery or claim raster ML results. Before operational use, add authoritative permit/protected-area sources, a secure identity/audit layer, calibrated regional training data, proper raster processing, storage policy, and a human review process.
