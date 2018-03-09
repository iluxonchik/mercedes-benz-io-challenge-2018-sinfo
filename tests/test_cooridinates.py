"""Coordinates class tests."""

import unittest
from mbio.geo.coordinate import Coordinate

class CoordinatesTestCase(unittest.TestCase):

    def test_distance_from_texas_to_guatemala(self):
        """Test haversine distance."""
        # Make sure that Kurupt won't get a wrong result when planning his
        #   next trip :)
        texas = Coordinate(29.7630556, -95.3630556)  # Houston
        guatemala = Coordinate(14.628434, -90.522713)

        expected = 1754.502
        obtained = texas.distance_to(guatemala)
        self.assertEqual(expected, obtained, 'Wrong distance computed.')

        # Kurupt will also have to come back from his trip
        expected = 1754.502
        obtained = guatemala.distance_to(texas)
        self.assertEqual(expected, obtained, 'Wrong distance computed.')
