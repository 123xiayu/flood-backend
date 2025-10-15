import unittest

from src.core import helpers


class TestHelpers(unittest.TestCase):
    def test_calculate_distance_zero(self):
        lat, lon = -31.9, 115.9
        self.assertAlmostEqual(
            helpers.calculate_distance(lat, lon, lat, lon),
            0.0,
            places=6,
        )

    def test_calculate_distance_symmetry(self):
        a = (-31.9, 115.9)
        b = (-32.0, 115.5)
        d1 = helpers.calculate_distance(a[0], a[1], b[0], b[1])
        d2 = helpers.calculate_distance(b[0], b[1], a[0], a[1])
        self.assertGreater(d1, 0)
        self.assertAlmostEqual(d1, d2, places=6)

    def test_load_stations_contains_perthstations(self):
        data = helpers.load_stations()
        self.assertIn("PerthStations", data)
        self.assertIsInstance(data["PerthStations"], list)
        self.assertGreater(len(data["PerthStations"]), 0)

    def test_find_nearest_station_exact_match(self):
        # Use coordinates of an existing station to expect an exact match
        stations = helpers.load_stations()["PerthStations"]
        station = stations[0]
        result = helpers.find_nearest_station(station["lat"], station["lon"])
        self.assertIsNotNone(result)
        self.assertEqual(result["station_id"], station["station_id"])


if __name__ == "__main__":
    unittest.main()

