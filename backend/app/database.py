"""SQLite persistence for local AOIs, analysis sessions and case records."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = ROOT / "data" / "khanan_netra.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS aoi (id INTEGER PRIMARY KEY, name TEXT, geojson TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS satellite_observations (id TEXT PRIMARY KEY, date TEXT, source TEXT, cloud_percentage REAL, aoi_id INTEGER, mode TEXT);
CREATE TABLE IF NOT EXISTS detections (id TEXT PRIMARY KEY, date TEXT, probability REAL, risk INTEGER, payload TEXT);
CREATE TABLE IF NOT EXISTS detection_polygons (id INTEGER PRIMARY KEY, detection_id TEXT, geojson TEXT);
CREATE TABLE IF NOT EXISTS permits (permit_id TEXT PRIMARY KEY, geojson TEXT, payload TEXT);
CREATE TABLE IF NOT EXISTS drone_surveys (id INTEGER PRIMARY KEY, case_id TEXT, payload TEXT);
CREATE TABLE IF NOT EXISTS drone_measurements (id INTEGER PRIMARY KEY, survey_id INTEGER, payload TEXT);
CREATE TABLE IF NOT EXISTS trucks (truck_id TEXT PRIMARY KEY, payload TEXT);
CREATE TABLE IF NOT EXISTS gps_points (id INTEGER PRIMARY KEY, truck_id TEXT, payload TEXT);
CREATE TABLE IF NOT EXISTS rfid_events (id INTEGER PRIMARY KEY, truck_id TEXT, payload TEXT);
CREATE TABLE IF NOT EXISTS challans (challan_id TEXT PRIMARY KEY, truck_id TEXT, payload TEXT);
CREATE TABLE IF NOT EXISTS weighbridge (id INTEGER PRIMARY KEY, truck_id TEXT, payload TEXT);
CREATE TABLE IF NOT EXISTS risk_cases (case_id TEXT PRIMARY KEY, detection_id TEXT, score INTEGER, status TEXT, payload TEXT);
CREATE TABLE IF NOT EXISTS alerts (id INTEGER PRIMARY KEY, case_id TEXT, level TEXT, message TEXT);
CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY, case_id TEXT, path TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
"""


def connection() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database() -> None:
    with connection() as conn:
        conn.executescript(SCHEMA)


def save_aoi(feature: dict[str, Any], name: str = "User AOI") -> dict[str, Any]:
    with connection() as conn:
        conn.execute("INSERT INTO aoi (name, geojson) VALUES (?, ?)", (name, json.dumps(feature)))
        record_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    return {"id": record_id, "name": name, "feature": feature}


def latest_aoi() -> dict[str, Any] | None:
    with connection() as conn:
        row = conn.execute("SELECT id, name, geojson, created_at FROM aoi ORDER BY id DESC LIMIT 1").fetchone()
    if not row:
        return None
    return {"id": row["id"], "name": row["name"], "feature": json.loads(row["geojson"]), "created_at": row["created_at"]}


def save_case(case_id: str, detection_id: str, risk: dict[str, Any], payload: dict[str, Any]) -> None:
    with connection() as conn:
        conn.execute("INSERT OR REPLACE INTO risk_cases (case_id, detection_id, score, status, payload) VALUES (?, ?, ?, ?, ?)", (case_id, detection_id, risk["score"], "FIELD VERIFICATION REQUIRED", json.dumps(payload)))
