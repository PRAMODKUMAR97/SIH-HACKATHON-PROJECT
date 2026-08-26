import unittest

from backend.app.demo_data import DEMO_AOI, PERMITS
from backend.app.services.gis_service import GeoJSONValidationError, intersection_polygon, overlap_area_ha, polygon_area_ha, polygon_coordinates


class GISServiceTests(unittest.TestCase):
    def test_aoi_is_valid_and_has_area(self):
        self.assertGreater(polygon_area_ha(DEMO_AOI), 0)
        self.assertEqual(len(polygon_coordinates(DEMO_AOI)), 5)

    def test_unclosed_polygon_is_closed(self):
        ring = polygon_coordinates({"type": "Polygon", "coordinates": [[[88.5, 27.1], [88.6, 27.1], [88.6, 27.2], [88.5, 27.2]]]})
        self.assertEqual(ring[0], ring[-1])

    def test_invalid_coordinates_are_rejected(self):
        with self.assertRaises(GeoJSONValidationError):
            polygon_coordinates({"type": "Polygon", "coordinates": [[[190, 0], [0, 1], [1, 0], [190, 0]]]})

    def test_permit_intersection_has_area(self):
        overlap = intersection_polygon(DEMO_AOI["geometry"], PERMITS["features"][0]["geometry"])
        self.assertIsNotNone(overlap)
        self.assertGreater(overlap_area_ha(DEMO_AOI["geometry"], PERMITS["features"][0]["geometry"]), 0)


if __name__ == "__main__":
    unittest.main()
