"""GeoJSON validation and lightweight polygon calculations.

For a hackathon demo this avoids requiring a native GIS installation. Production
deployments can replace these routines with GeoPandas/Shapely/Rasterio without
changing the API contract.
"""
from __future__ import annotations

from math import cos, radians
from typing import Any


class GeoJSONValidationError(ValueError):
    pass


def polygon_coordinates(feature_or_geometry: dict[str, Any]) -> list[list[float]]:
    geometry = feature_or_geometry.get("geometry", feature_or_geometry)
    if geometry.get("type") != "Polygon":
        raise GeoJSONValidationError("AOI must be a GeoJSON Polygon.")
    rings = geometry.get("coordinates")
    if not isinstance(rings, list) or not rings or not isinstance(rings[0], list):
        raise GeoJSONValidationError("AOI polygon coordinates are missing.")
    ring = rings[0]
    if len(ring) < 4:
        raise GeoJSONValidationError("AOI polygon needs at least three vertices.")
    clean: list[list[float]] = []
    for point in ring:
        if not isinstance(point, list) or len(point) < 2:
            raise GeoJSONValidationError("Each coordinate must contain longitude and latitude.")
        lon, lat = point[0], point[1]
        if not isinstance(lon, (int, float)) or not isinstance(lat, (int, float)) or not -180 <= lon <= 180 or not -90 <= lat <= 90:
            raise GeoJSONValidationError("AOI contains an invalid longitude or latitude.")
        clean.append([float(lon), float(lat)])
    if clean[0] != clean[-1]:
        clean.append(clean[0])
    if abs(signed_area(clean)) < 1e-12:
        raise GeoJSONValidationError("AOI must have a non-zero area.")
    return clean


def signed_area(ring: list[list[float]]) -> float:
    return sum(ring[index][0] * ring[index + 1][1] - ring[index + 1][0] * ring[index][1] for index in range(len(ring) - 1)) / 2


def polygon_area_ha(feature_or_geometry: dict[str, Any]) -> float:
    ring = polygon_coordinates(feature_or_geometry)
    mean_lat = sum(point[1] for point in ring[:-1]) / (len(ring) - 1)
    # Equirectangular local approximation: accurate enough for the small AOIs
    # accepted by this prototype and deterministic for the bundled demo.
    x_scale = 111_320 * cos(radians(mean_lat))
    y_scale = 110_574
    area_m2 = abs(sum((ring[i][0] * x_scale) * (ring[i + 1][1] * y_scale) - (ring[i + 1][0] * x_scale) * (ring[i][1] * y_scale) for i in range(len(ring) - 1)) / 2)
    return round(area_m2 / 10_000, 3)


def bounds(feature_or_geometry: dict[str, Any]) -> tuple[float, float, float, float]:
    ring = polygon_coordinates(feature_or_geometry)
    lons, lats = zip(*ring)
    return min(lons), min(lats), max(lons), max(lats)


def bounds_overlap(first: dict[str, Any], second: dict[str, Any]) -> bool:
    a, b = bounds(first), bounds(second)
    return not (a[2] < b[0] or a[0] > b[2] or a[3] < b[1] or a[1] > b[3])


def _inside(point: list[float], edge_start: list[float], edge_end: list[float], orientation: float) -> bool:
    cross = (edge_end[0] - edge_start[0]) * (point[1] - edge_start[1]) - (edge_end[1] - edge_start[1]) * (point[0] - edge_start[0])
    return cross >= -1e-12 if orientation >= 0 else cross <= 1e-12


def _intersection(start: list[float], end: list[float], clip_start: list[float], clip_end: list[float]) -> list[float]:
    x1, y1 = start; x2, y2 = end; x3, y3 = clip_start; x4, y4 = clip_end
    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denominator) < 1e-12:
        return end
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
    return [x1 + t * (x2 - x1), y1 + t * (y2 - y1)]


def intersection_polygon(subject: dict[str, Any], clip: dict[str, Any]) -> dict[str, Any] | None:
    """Return intersection when the clip polygon is convex (permits are here)."""
    subject_ring = polygon_coordinates(subject)[:-1]
    clip_ring = polygon_coordinates(clip)
    output = subject_ring
    orientation = signed_area(clip_ring)
    for index in range(len(clip_ring) - 1):
        if not output:
            return None
        edge_start, edge_end = clip_ring[index], clip_ring[index + 1]
        input_points = output
        output = []
        previous = input_points[-1]
        for current in input_points:
            current_inside = _inside(current, edge_start, edge_end, orientation)
            previous_inside = _inside(previous, edge_start, edge_end, orientation)
            if current_inside:
                if not previous_inside:
                    output.append(_intersection(previous, current, edge_start, edge_end))
                output.append(current)
            elif previous_inside:
                output.append(_intersection(previous, current, edge_start, edge_end))
            previous = current
    if len(output) < 3:
        return None
    output.append(output[0])
    return {"type": "Polygon", "coordinates": [output]}


def overlap_area_ha(subject: dict[str, Any], clip: dict[str, Any]) -> float:
    if not bounds_overlap(subject, clip):
        return 0.0
    overlap = intersection_polygon(subject, clip)
    return polygon_area_ha(overlap) if overlap else 0.0


def feature_collection(items: list[dict[str, Any]]) -> dict[str, Any]:
    return {"type": "FeatureCollection", "features": items}
