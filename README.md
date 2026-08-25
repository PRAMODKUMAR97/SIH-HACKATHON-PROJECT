# KHANAN-NETRA

## AI-Powered Satellite Mining Intelligence & Surveillance

> **An intelligent eye for mining — detecting suspicious activity, verifying it with multiple data sources, and helping authorities prioritize field inspections.**

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Our Solution](#our-solution)
- [Objectives](#objectives)
- [Key Innovation](#key-innovation)
- [How KHANAN-NETRA Works](#how-khanan-netra-works)
- [Complete Workflow](#complete-workflow)
- [System Architecture](#system-architecture)
- [Core Modules](#core-modules)
- [Satellite Monitoring](#1-satellite-monitoring)
- [InSAR Ground Deformation](#2-insar-ground-deformation)
- [AI Mining Detection](#3-ai-mining-detection)
- [Mining Permit & Boundary Validation](#4-mining-permit--boundary-validation)
- [Drone 3D Verification](#5-drone-3d-verification)
- [Truck GPS & Transportation Monitoring](#6-truck-gps--transportation-monitoring)
- [RFID & Checkpoint Verification](#7-rfid--checkpoint-verification)
- [e-Challan & Weighbridge Verification](#8-e-challan--weighbridge-verification)
- [AI Evidence Fusion & Risk Scoring](#9-ai-evidence-fusion--risk-scoring)
- [Dashboard](#10-dashboard)
- [Alerts & Reports](#11-alerts--reports)
- [KML & GPX Export](#12-kml--gpx-export)
- [Technology Stack](#technology-stack)
- [Project Architecture](#project-architecture)
- [Data Flow](#data-flow)
- [Risk Scoring](#risk-scoring)
- [Example Scenario](#example-scenario)
- [Demo Mode](#demo-mode)
- [Real-World Data Integration](#real-world-data-integration)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Environment Variables](#environment-variables)
- [Dataset Structure](#dataset-structure)
- [API Overview](#api-overview)
- [Machine Learning Pipeline](#machine-learning-pipeline)
- [3D Reconstruction Pipeline](#3d-reconstruction-pipeline)
- [Database](#database)
- [Frontend](#frontend)
- [Backend](#backend)
- [Security & Privacy](#security--privacy)
- [Limitations](#limitations)
- [Future Scope](#future-scope)
- [Team Responsibilities](#team-responsibilities)
- [Development Guidelines](#development-guidelines)
- [Git Workflow](#git-workflow)
- [Project Status](#project-status)
- [Use Cases](#use-cases)
- [Expected Benefits](#expected-benefits)
- [Disclaimer](#disclaimer)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

# Overview

**KHANAN-NETRA** is an AI-powered mining intelligence and surveillance platform designed to help identify and prioritize potentially illegal or suspicious mining activity.

The system combines multiple sources of information instead of relying on a single detection method:

- Satellite imagery
- SAR / InSAR analysis
- Optical imagery
- Mining permit boundaries
- Digital elevation and terrain data
- Drone imagery
- Drone-derived 3D models
- Truck GPS data
- RFID/checkpoint records
- e-Challan records
- Weighbridge/load information
- Historical activity
- Machine-learning predictions

The system analyzes these sources together and produces an **explainable risk score** for each detected location or activity.

The goal is not to automatically declare a person or company guilty. Instead, KHANAN-NETRA identifies **high-risk cases that require human/field verification**.

---

# Problem Statement

Illegal and unauthorized mining can cause:

- Environmental damage
- Land degradation
- Ground instability
- Loss of government revenue
- Unauthorized mineral extraction
- Uncontrolled transportation of minerals
- Damage to protected areas
- Difficulty in monitoring remote locations

A major challenge is that mining information is often distributed across different systems.

For example:

```text
Satellite data
       +
Mining permits
       +
Truck GPS
       +
RFID
       +
e-Challan
       +
Weighbridge
       +
Historical records
```

An officer may have to examine these sources separately.

This makes it difficult to quickly identify contradictions such as:

```text
Permitted volume     = 15,000 m³
Estimated excavation = 34,200 m³
Reported transport   = 12,000 m³
GPS route             = suspicious
```

KHANAN-NETRA addresses this problem by bringing these sources together and using AI to identify anomalies and prioritize inspections.

---

# Our Solution

KHANAN-NETRA follows a multi-stage surveillance workflow:

```text
Satellite Monitoring
        ↓
Suspicious Area Detection
        ↓
InSAR / Terrain Analysis
        ↓
Mining Boundary Validation
        ↓
Drone Verification (when required)
        ↓
3D Mine Reconstruction
        ↓
Excavation Volume Estimation
        ↓
Truck GPS / RFID Analysis
        ↓
e-Challan / Weighbridge Verification
        ↓
AI Evidence Fusion
        ↓
Risk Score
        ↓
Dashboard
        ↓
Alert / Evidence Report
        ↓
Field Verification
```

---

# Objectives

The primary objectives are:

1. Detect suspicious mining activity using remote sensing.
2. Identify changes in mining areas over time.
3. Compare detected activity with legal mining boundaries.
4. Estimate excavation area, depth and volume where suitable data is available.
5. Verify suspicious locations using drone-based 3D reconstruction.
6. Monitor mineral transportation using truck GPS data.
7. Detect route deviations and checkpoint anomalies.
8. Compare declared transportation quantities with available load/weighbridge records.
9. Combine independent evidence using an AI risk engine.
10. Provide a simple dashboard for monitoring and decision support.
11. Generate evidence-support reports for field verification.
12. Reduce the amount of manual data analysis required by authorities.

---

# Key Innovation

The project is not based on the idea that satellite imagery alone can prove illegal mining.

The key concept is **multi-source evidence fusion**.

Instead of:

```text
Satellite → Mining detected
```

KHANAN-NETRA attempts to establish:

```text
Satellite
   +
InSAR
   +
Drone 3D
   +
Permit
   +
GPS
   +
RFID
   +
e-Challan
   +
Weighbridge
   +
Historical data
        ↓
  AI Evidence Fusion
        ↓
    Risk Score
```

This allows the system to identify **contradictions between physical activity, legal permissions and transportation records**.

---

# How KHANAN-NETRA Works

## Step 1 — Satellite Monitoring

Satellite imagery is used to monitor selected mining regions.

Potential sources include:

- Sentinel-1 SAR
- Sentinel-2 optical imagery
- Other compatible remote-sensing datasets

The system identifies changes that may indicate mining activity.

---

## Step 2 — InSAR Ground Deformation

SAR data can be processed using interferometric techniques to identify surface deformation.

Potential outputs include:

- Subsidence
- Uplift
- Surface displacement
- Deformation trends
- Change maps

The system uses these observations as **evidence**, not as an automatic legal conclusion.

---

## Step 3 — AI Mining Detection

Machine-learning models analyze available features and classify candidate areas.

Possible output:

```text
Mining probability: 91%
Confidence: High
Area: 2.35 ha
Risk: High
```

The model can use:

- Spectral features
- SAR features
- Texture
- Temporal change
- Terrain information
- Spatial context

The first prototype can use a lightweight model such as:

- Random Forest
- XGBoost
- Logistic Regression
- Other suitable classifiers

---

# 4. Mining Permit & Boundary Validation

Detected mining areas are compared with authorized mining polygons.

Example:

```text
Detected activity
       ↓
Inside permitted boundary?
       ↓
   ┌───┴────┐
  YES       NO
   ↓         ↓
Review     Suspicious
```

Possible classifications:

- `LEGAL_WITHIN_PERMIT`
- `SUSPICIOUS_OUTSIDE_PERMIT`
- `ILLEGAL_PROTECTED_AREA`
- `ILLEGAL_INDIGENOUS_AREA`
- `PENDING_VERIFICATION`

The exact legal interpretation depends on the jurisdiction and official datasets.

---

# 5. Drone 3D Verification

Satellite imagery provides broad-area monitoring.

For high-risk locations, a drone can be used for detailed local verification.

The drone captures multiple overlapping images from different positions and elevations.

```text
Drone
  ↓
Multiple overlapping photographs
  ↓
Photogrammetry
  ↓
Feature matching
  ↓
Point cloud
  ↓
3D mesh
  ↓
Geo-referenced 3D model
```

Potential tools include:

- OpenDroneMap
- WebODM
- Structure-from-Motion
- Photogrammetry software

The resulting model can support:

- Surface area estimation
- Excavation depth
- Terrain comparison
- Bench analysis
- Excavated-volume estimation

---

# 6. Truck GPS & Transportation Monitoring

Mining activity is also connected to mineral transportation.

KHANAN-NETRA can accept truck records containing:

- Truck ID
- Vehicle number
- Mine/source
- Destination
- GPS coordinates
- Timestamp
- Planned route
- Actual route
- Declared load
- Trip status

Example:

```text
Truck: TRK-4587

Mine A
   ↓
Checkpoint 1
   ↓
Checkpoint 2
   ↓
Unexpected deviation
   ↓
Crusher Plant A
```

The system can identify:

- Route deviation
- Unusual stops
- Unexpected destinations
- Excessive travel distance
- Missing route segments
- Unusual activity times

For the prototype, GPS data can be simulated using CSV/JSON files.

---

# 7. RFID & Checkpoint Verification

RFID/checkpoint information can be compared with GPS records.

Example:

```text
RFID:
Truck passed Checkpoint 3

GPS:
Truck was 8 km away from Checkpoint 3
```

This creates an anomaly that requires verification.

Possible statuses:

- Checkpoint verified
- Checkpoint missed
- GPS/RFID mismatch
- Unknown checkpoint
- Route anomaly

---

# 8. e-Challan & Weighbridge Verification

The system can compare:

- Declared quantity
- e-Challan quantity
- Weighbridge quantity
- Estimated excavation
- Historical transport quantity

Example:

```text
Permit:
15,000 m³

Drone estimate:
34,200 m³

Transport records:
12,000 m³

Result:
Large quantity mismatch
```

This does not automatically prove illegal extraction, but it can increase the risk score and trigger field verification.

---

# 9. AI Evidence Fusion & Risk Scoring

This is the central intelligence layer.

The AI receives multiple signals:

```text
Satellite evidence
InSAR evidence
Permit information
Drone measurements
GPS anomalies
RFID anomalies
e-Challan data
Weighbridge data
Historical activity
```

The system combines these signals.

Example:

```text
Satellite anomaly        High
Mining probability       91%
Outside permit           Yes
Volume mismatch          High
GPS deviation            Yes
RFID mismatch            Yes
Historical increase      High
```

Output:

```text
Risk Score: 91 / 100

Risk Level: HIGH

Recommended Action:
Field Verification
```

The risk engine should be explainable.

The dashboard should show **why** a location received a high score.

---

# 10. Dashboard

The KHANAN-NETRA dashboard is designed as a professional monitoring/control interface.

Main dashboard components:

### KPI cards

- Monitored Area
- Active/Tracked Trucks
- Detected Mining Sites
- High-Risk Sites
- Legal Sites
- Suspicious Sites
- Estimated Mining Volume

### Main map

The map can display:

- Mining detections
- Mining boundaries
- Protected areas
- Truck routes
- GPS locations
- Risk levels
- Detection polygons

### AI summary

Display:

- Overall risk
- High-risk count
- Medium-risk count
- Low-risk count
- Confidence distribution
- Legality distribution

### Analytics

Charts can include:

- Mining activity over time
- Area affected over time
- Detection count
- Risk trend
- Estimated volume
- Route anomalies

### Detection table

Each record can contain:

```text
Detection ID
Date
Latitude
Longitude
Area
Probability
Legal Status
Protection Status
Risk Score
Action
```

---

# 11. Alerts & Reports

The system can generate alerts such as:

- High-confidence mining detected
- Activity outside permitted boundary
- Mining near protected area
- Large volume mismatch
- Truck route deviation
- RFID/GPS mismatch
- Unusual mining activity increase

The system can also generate a PDF evidence-support report.

A report can contain:

- Monitoring period
- Location
- Satellite evidence
- Detection probability
- Area
- Legal status
- Risk score
- Historical information
- Supporting evidence
- Recommended action

---

# 12. KML & GPX Export

KHANAN-NETRA can export relevant detections and locations.

### KML

Useful for:

- Google Earth
- GIS applications
- Sharing detection locations

### GPX

Useful for:

- Field teams
- GPS devices
- Location/navigation workflows

Exports should contain appropriate metadata such as:

- Detection ID
- Coordinates
- Risk
- Confidence
- Legal status

---

# Technology Stack

## Frontend

- React
- TypeScript
- Tailwind CSS
- Leaflet
- Recharts / Plotly

## Backend

- Python
- FastAPI

## AI / ML

- scikit-learn
- Random Forest
- XGBoost (optional)
- PyTorch (optional for advanced deep-learning models)

## Geospatial

- GeoPandas
- Shapely
- Rasterio
- GDAL
- pyproj
- QGIS

## Satellite

- Sentinel-1
- Sentinel-2
- ESA SNAP
- Google Earth Engine (optional for real-data integration)

## Drone / 3D

- OpenDroneMap
- WebODM
- Photogrammetry
- Point clouds
- DSM/DTM
- 3D mesh

## Database

### Prototype

- SQLite

### Production

- PostgreSQL
- PostGIS

## Reports

- ReportLab

## Data

- CSV
- JSON
- GeoJSON
- GeoTIFF
- KML
- GPX

## Deployment

- Docker
- Docker Compose
- Cloud deployment (optional)

## Version Control

- Git
- GitHub

---

# Project Architecture

```text
                         KHANAN-NETRA
                              |
            ┌─────────────────┴─────────────────┐
            |                                   |
      GEO-SPATIAL DATA                    TRANSPORT DATA
            |                                   |
     ┌──────┼──────┐                    ┌───────┼───────┐
     |      |      |                    |       |       |
 Satellite InSAR  Drone                GPS     RFID  e-Challan
     |      |      |                    |       |       |
     └──────┼──────┘                    └───────┼───────┘
            |                                   |
            └─────────────────┬─────────────────┘
                              |
                    SPATIAL / DATA ANALYSIS
                              |
                 ┌────────────┴────────────┐
                 |                         |
           Permit Validation         Volume Analysis
                 |                         |
                 └────────────┬────────────┘
                              |
                     AI EVIDENCE FUSION
                              |
                         RISK ENGINE
                              |
                  ┌───────────┴───────────┐
                  |                       |
              Dashboard               Alerts
                  |                       |
              Analytics              PDF Report
                  |
             Field Verification
```

---

# Data Flow

```text
Satellite / Drone / GPS / RFID / e-Challan
                    ↓
               Data Ingestion
                    ↓
              Data Validation
                    ↓
             Pre-processing
                    ↓
          Geospatial Processing
                    ↓
             AI / ML Analysis
                    ↓
             Evidence Fusion
                    ↓
              Risk Scoring
                    ↓
             Dashboard / API
                    ↓
             Alert / Report
                    ↓
             Human Verification
```

---

# Risk Scoring

KHANAN-NETRA uses a risk score from 0 to 100.

Example conceptual scoring:

```text
Mining Probability       25%
Boundary Violation       20%
Volume Anomaly           20%
GPS/Route Anomaly        15%
RFID/Checkpoint Anomaly  10%
Historical Change        10%
```

The exact weights should be configurable and validated using appropriate labeled data.

Example:

```text
0–30     LOW
31–60    MEDIUM
61–80    HIGH
81–100   CRITICAL
```

These ranges are configurable and should not be interpreted as legal classifications.

---

# Example Scenario

Suppose a mining permit allows:

```text
15,000 m³
```

Satellite analysis detects significant surface changes.

The location is outside the permitted polygon.

A drone survey is requested.

The drone produces a 3D model and estimates:

```text
34,200 m³
```

Transportation records show:

```text
12,000 m³
```

Truck GPS also identifies several route deviations.

The evidence-fusion engine calculates:

```text
Risk Score: 91/100
Risk Level: HIGH
```

The dashboard displays:

```text
HIGH-RISK LOCATION

Reasons:
- High mining probability
- Outside legal boundary
- Excavation volume mismatch
- Transportation mismatch
- Route anomalies

Recommended Action:
Field verification
```

The system then generates an evidence-support report.

---

# Demo Mode

The project should support a complete offline/local demo.

Demo mode includes synthetic data for:

- Mining detections
- Satellite observations
- Legal boundaries
- Protected areas
- Trucks
- GPS routes
- RFID checkpoints
- e-Challans
- Weighbridge records
- Historical records
- Risk scores

All synthetic information must be clearly labelled as **DEMO DATA**.

The demo allows the team to demonstrate the complete workflow without requiring:

- Drone hardware
- GPS hardware
- RFID hardware
- Paid APIs
- Live government databases
- Satellite credentials

---

# Real-World Data Integration

The architecture is designed so demo data can later be replaced with real sources.

## Satellite

Possible sources:

- Sentinel-1
- Sentinel-2
- Other compatible satellite providers

## GIS

Official:

- Mining lease boundaries
- Protected-area boundaries
- Administrative boundaries

## Transport

Possible future integrations:

- GPS APIs
- RFID readers
- e-Challan systems
- Weighbridge systems

## Drone

Future integration:

```text
Drone photos
    ↓
Photogrammetry
    ↓
Point cloud
    ↓
DSM/DTM
    ↓
3D model
    ↓
Volume estimation
```

---

# Installation

## Requirements

Recommended:

- Windows 10/11, Linux or macOS
- Python 3.10+
- Node.js 18+
- npm
- Git
- VS Code (recommended)

For the prototype, SQLite should be used so a separate database server is not required.

---

# Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd khanan-netra
```

---

# Backend Setup

Create a virtual environment:

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn backend.app.main:app --reload
```

The API should become available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The dashboard will normally be available at the local address displayed by Vite.

---

# Demo Mode

If the project contains `run_demo.py`:

```bash
python run_demo.py
```

The demo should:

1. Load demo data
2. Start the backend
3. Prepare the dashboard
4. Display detections
5. Allow filtering
6. Display risk scores
7. Generate reports
8. Export KML/GPX

---

# Environment Variables

Create:

```text
.env
```

using:

```text
.env.example
```

Example:

```env
APP_ENV=development
DATABASE_URL=sqlite:///./khanan_netra.db
API_HOST=127.0.0.1
API_PORT=8000

# Optional future integrations
GEE_PROJECT_ID=
MAPBOX_TOKEN=
SATELLITE_API_KEY=
```

The basic demo should work without optional API keys.

Never commit secrets to GitHub.

---

# Dataset Structure

A suggested structure:

```text
data/
├── demo/
│   ├── detections.csv
│   ├── trucks.csv
│   ├── gps_routes.csv
│   ├── challans.csv
│   ├── weighbridge.csv
│   └── historical_activity.csv
│
├── boundaries/
│   ├── mining_permits.geojson
│   ├── protected_areas.geojson
│   └── administrative_boundaries.geojson
│
└── satellite/
    ├── sample/
    └── processed/
```

Example detection record:

```json
{
  "detection_id": "KN-0001",
  "latitude": 23.6854,
  "longitude": 86.4512,
  "area_ha": 2.35,
  "mining_probability": 0.92,
  "legal_status": "SUSPICIOUS_OUTSIDE_PERMIT",
  "risk_score": 91
}
```

---

# API Overview

Suggested endpoints:

## Health

```text
GET /api/health
```

## Detections

```text
GET /api/detections
GET /api/detections/{id}
```

## Risk

```text
GET /api/risk
GET /api/risk/{id}
```

## Satellite

```text
GET /api/satellite/detections
POST /api/satellite/analyze
```

## Mining permits

```text
GET /api/permits
```

## Trucks

```text
GET /api/trucks
GET /api/trucks/{id}
```

## Routes

```text
GET /api/routes
GET /api/routes/{truck_id}
```

## Reports

```text
POST /api/reports/generate
```

## Exports

```text
GET /api/export/kml
GET /api/export/gpx
```

---

# Machine Learning Pipeline

```text
Raw Satellite Data
       ↓
Pre-processing
       ↓
Feature Extraction
       ↓
Training Dataset
       ↓
Train Model
       ↓
Validation
       ↓
Model Evaluation
       ↓
Prediction
       ↓
Mining Probability
       ↓
Evidence Fusion
```

Possible models:

### Baseline

Random Forest

### Advanced

- XGBoost
- CNN
- U-Net
- Transformer-based remote sensing models

The first prototype should prioritize reliability and explainability over model complexity.

---

# 3D Reconstruction Pipeline

```text
Drone Flight
     ↓
Multiple Images
     ↓
Image Quality Check
     ↓
Feature Matching
     ↓
Structure-from-Motion
     ↓
Point Cloud
     ↓
Mesh Generation
     ↓
Geo-referencing
     ↓
DSM / DTM
     ↓
3D Mine Model
     ↓
Area / Depth / Volume
```

For accurate surveying, image overlap, camera calibration, flight planning and ground-control/georeferencing procedures should be handled appropriately.

---

# Database

## Prototype

SQLite is recommended because:

- No server installation
- Easy setup
- Easy backup
- Good for demonstrations

## Production

Use:

```text
PostgreSQL
+
PostGIS
```

PostGIS can support:

- Spatial polygons
- GPS coordinates
- Mining boundaries
- Spatial queries
- Geofencing
- Route analysis
- Spatial indexes

---

# Frontend

The frontend is responsible for:

- Dashboard
- Map
- Filters
- Detection table
- Risk visualization
- Charts
- Alerts
- Reports
- Detection details

Suggested components:

```text
components/
├── MapView
├── KPICards
├── RiskSummary
├── DetectionTable
├── AlertPanel
├── RiskChart
├── MiningTrendChart
├── TruckMap
├── ReportButton
└── ExportButtons
```

---

# Backend

The backend handles:

- API
- Data ingestion
- ML inference
- Geospatial processing
- Risk scoring
- Database operations
- Report generation
- Export generation

Suggested services:

```text
services/
├── satellite_service.py
├── gis_service.py
├── ml_service.py
├── risk_service.py
├── truck_service.py
├── report_service.py
└── export_service.py
```

---

# Security & Privacy

The production system should implement:

- Authentication
- Role-based access control
- Secure API keys
- Encrypted communication
- Audit logs
- Data validation
- Access restrictions
- Secure storage of sensitive location information

For the hackathon demo, authentication can remain simple.

Never commit:

- Passwords
- API keys
- Access tokens
- Private credentials
- Government/private datasets without authorization

---

# Limitations

KHANAN-NETRA is a decision-support system.

Important limitations include:

1. Satellite imagery has temporal and spatial limitations.
2. InSAR results can be affected by vegetation, atmospheric conditions and processing quality.
3. Ground deformation does not automatically prove illegal mining.
4. Drone measurements depend on image quality, flight planning and georeferencing.
5. Volume estimates depend on the quality of the reference terrain/model.
6. GPS records can be incomplete or inaccurate.
7. RFID records may contain hardware/data errors.
8. e-Challan data may contain administrative inconsistencies.
9. AI predictions can contain false positives and false negatives.
10. Legal status must ultimately be determined using official records and authorized procedures.

Therefore:

> **KHANAN-NETRA identifies suspicious/high-risk cases for verification; it does not replace legal investigation or official enforcement decisions.**

---

# Future Scope

## Phase 1 — Prototype

- Demo satellite data
- Mining detection
- Legal boundary validation
- Dashboard
- Risk score
- Reports
- KML/GPX

## Phase 2 — Advanced Satellite

- Live Sentinel integration
- Automated satellite processing
- InSAR time-series
- Improved ML models

## Phase 3 — Drone Verification

- Automated drone image upload
- Photogrammetry
- 3D mine model
- Excavation volume
- Terrain comparison

## Phase 4 — Transportation Intelligence

- Live GPS
- RFID
- e-Challan integration
- Weighbridge integration
- Route anomaly detection

## Phase 5 — Evidence Fusion

Combine:

```text
Satellite
+
Drone
+
Permit
+
GPS
+
RFID
+
e-Challan
+
Weighbridge
+
Historical Data
```

into a unified explainable risk engine.

## Phase 6 — Production Deployment

- Cloud infrastructure
- PostgreSQL/PostGIS
- Authentication
- Government API integrations
- Mobile application
- Field inspection application
- Automated monitoring
- Multi-region deployment

---

# Team Responsibilities

A possible team structure:

## AI / ML Team

Responsible for:

- Satellite classification
- Feature extraction
- Risk model
- Anomaly detection
- Model evaluation

## Geospatial Team

Responsible for:

- GIS
- InSAR processing
- Mining polygons
- Boundary validation
- Terrain analysis

## Drone / 3D Team

Responsible for:

- Drone image collection
- Photogrammetry
- 3D reconstruction
- Volume estimation

## Backend Team

Responsible for:

- FastAPI
- Database
- APIs
- Data processing
- Reports
- Exports

## Frontend Team

Responsible for:

- React
- Dashboard
- Maps
- Charts
- Alerts
- User experience

## Integration Team

Responsible for:

- Connecting AI
- GIS
- Backend
- Frontend
- Demo workflow

---

# Development Guidelines

Before adding a feature:

1. Create an issue.
2. Explain the feature.
3. Create a separate branch.
4. Implement the feature.
5. Test locally.
6. Update documentation.
7. Create a Pull Request.
8. Review the changes.
9. Merge into `main`.

Recommended branches:

```text
main
develop
feature/satellite-detection
feature/drone-3d
feature/truck-gps
feature/risk-engine
feature/dashboard
feature/reports
```

---

# Git Workflow

```bash
git checkout -b feature/your-feature
```

Make changes:

```bash
git add .
git commit -m "Add mining detection module"
git push origin feature/your-feature
```

Then create a Pull Request.

Do not directly push experimental changes to `main`.

---

# Project Status

Current development direction:

```text
[ ] Satellite data pipeline
[ ] InSAR processing
[ ] ML mining classifier
[ ] Permit boundary validation
[ ] Drone 3D reconstruction
[ ] Excavation volume estimation
[ ] Truck GPS module
[ ] RFID/checkpoint module
[ ] e-Challan module
[ ] Evidence-fusion engine
[ ] Risk scoring
[ ] Dashboard
[ ] Alerts
[ ] PDF reports
[ ] KML export
[ ] GPX export
[ ] Production deployment
```

Update this checklist as development progresses.

---

# Use Cases

KHANAN-NETRA can support:

- Mining departments
- Environmental monitoring teams
- Forest departments
- Revenue departments
- Local administration
- Field inspection teams
- Researchers
- Mining compliance teams

The actual use of the platform in government operations would require appropriate authorization, data access and legal procedures.

---

# Expected Benefits

### Faster Detection

Large areas can be screened using remote sensing instead of relying only on manual inspection.

### Better Prioritization

Field teams can focus on high-risk locations first.

### Multi-source Verification

Different data sources can be compared rather than analyzed separately.

### Transparent Decision Support

The system can display why a location was flagged.

### Resource Protection

Earlier detection can support action against potentially unauthorized extraction.

### Reduced Manual Analysis

Automated data processing can reduce repetitive monitoring work.

### Better Record Consistency

GPS, RFID, e-Challan and weighbridge information can be cross-checked.

---

# Why KHANAN-NETRA?

The name comes from:

**KHANAN** — Mining / extraction

**NETRA** — Eye / vision

Therefore:

> **KHANAN-NETRA = An intelligent eye for mining surveillance.**

The system acts as a digital monitoring layer that observes mining activity, analyzes evidence and highlights locations requiring attention.

---

# Project Vision

The long-term vision is:

```text
              KHANAN-NETRA
                    |
        ┌───────────┴───────────┐
        |                       |
    SEE THE LAND            TRACK ACTIVITY
        |                       |
    Satellite                  GPS
    InSAR                      RFID
    Drone                      e-Challan
        |                       |
        └───────────┬───────────┘
                    |
               UNDERSTAND
                    |
                  AI/ML
                    |
              EVIDENCE FUSION
                    |
               RISK SCORE
                    |
                TAKE ACTION
```

The ultimate goal is to move from:

> **Manual monitoring after suspected activity**

toward:

> **Continuous data-driven monitoring and early identification of high-risk activity.**

---

# Disclaimer

KHANAN-NETRA is a research/prototype and decision-support concept.

It does not independently establish that mining activity is illegal.

All alerts, predictions and risk scores should be treated as indicators requiring appropriate human review, official records and field verification.

Any real-world deployment must comply with applicable laws, privacy requirements, aviation/drone regulations, data licensing requirements and government procedures.

---

# Acknowledgements

KHANAN-NETRA is inspired by publicly available research and open-source technologies in:

- Remote sensing
- SAR/InSAR
- GIS
- Machine learning
- Photogrammetry
- Geospatial analytics
- Mining surveillance

The project may use open datasets and open-source libraries according to their respective licenses.

---

# License

Choose an appropriate open-source license for your team's needs.

For example:

```text
MIT License
```

If using third-party datasets, models or code, their individual licenses must also be respected.

---

# Final Concept

```text
SATELLITE
    ↓
DETECT
    ↓
INSAR / GIS ANALYSIS
    ↓
LEGAL BOUNDARY CHECK
    ↓
DRONE VERIFICATION
    ↓
3D EXCAVATION ESTIMATION
    ↓
TRUCK GPS / RFID
    ↓
e-CHALLAN / WEIGHBRIDGE
    ↓
AI EVIDENCE FUSION
    ↓
RISK SCORE
    ↓
DASHBOARD
    ↓
ALERT
    ↓
FIELD VERIFICATION
```

**KHANAN-NETRA — See the Mining. Understand the Evidence. Prioritize the Action.**
