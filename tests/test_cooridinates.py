"""Coordinates class tests."""

import unittest
from mbio.geo.coordinate import Coordinate
from mbio.geo.exceptions import NotAPolygonError

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

    def test_points_inside_of_polygon(self):
        coord_list = [
                Coordinate(31.000213,-87.584839),
                Coordinate(31.009629,-85.003052),
                Coordinate(30.726726,-84.838257),
                Coordinate(30.584962,-82.168579),
                Coordinate(30.73617,-81.476441),
                Coordinate(29.002375,-80.795288),
                Coordinate(26.896598,-79.938355),
                Coordinate(25.813738,-80.059204),
                Coordinate(24.93028,-80.454712),
                Coordinate(24.401135,-81.817017),
                Coordinate(24.700927,-81.959839),
                Coordinate(24.950203,-81.124878),
                Coordinate(26.0015,-82.014771),
                Coordinate(27.833247,-83.014527),
                Coordinate(28.8389,-82.871704),
                Coordinate(29.987293,-84.091187),
                Coordinate(29.539053,-85.134888),
                Coordinate(30.272352,-86.47522),
                Coordinate(30.281839,-87.628784),
        ]

        in_coord = Coordinate(30.82112,-87.255249)
        is_pt_inside = in_coord.is_inside_polygon(coord_list)
        self.assertTrue(is_pt_inside)


        in_coord = Coordinate(27.92065,-82.619019)
        is_pt_inside = in_coord.is_inside_polygon(coord_list)
        self.assertTrue(is_pt_inside)

        in_coord = Coordinate(25.853292,-80.223999)
        is_pt_inside = in_coord.is_inside_polygon(coord_list)
        self.assertTrue(is_pt_inside)

        in_coord = Coordinate(24.680963,-81.366577)
        is_pt_inside = in_coord.is_inside_polygon(coord_list)
        self.assertTrue(is_pt_inside)

    def test_points_outside_of_polygon(self):

        coord_list = [
                Coordinate(31.000213,-87.584839),
                Coordinate(31.009629,-85.003052),
                Coordinate(30.726726,-84.838257),
                Coordinate(30.584962,-82.168579),
                Coordinate(30.73617,-81.476441),
                Coordinate(29.002375,-80.795288),
                Coordinate(26.896598,-79.938355),
                Coordinate(25.813738,-80.059204),
                Coordinate(24.93028,-80.454712),
                Coordinate(24.401135,-81.817017),
                Coordinate(24.700927,-81.959839),
                Coordinate(24.950203,-81.124878),
                Coordinate(26.0015,-82.014771),
                Coordinate(27.833247,-83.014527),
                Coordinate(28.8389,-82.871704),
                Coordinate(29.987293,-84.091187),
                Coordinate(29.539053,-85.134888),
                Coordinate(30.272352,-86.47522),
                Coordinate(30.281839,-87.628784),
            ]

        out_coord = Coordinate(24.311058,-81.17981)
        is_pt_inside = out_coord.is_inside_polygon(coord_list)
        self.assertFalse(is_pt_inside)

        out_coord = Coordinate(29.029276,-90.805666)
        is_pt_inside = out_coord.is_inside_polygon(coord_list)
        self.assertFalse(is_pt_inside)

        out_coord = Coordinate(25.159207,-79.916382)
        is_pt_inside = out_coord.is_inside_polygon(coord_list)
        self.assertFalse(is_pt_inside)

        out_coord = Coordinate(31.319856,-84.607544)
        is_pt_inside = out_coord.is_inside_polygon(coord_list)
        self.assertFalse(is_pt_inside)

    def test_points_in_triangle(self):
        coord_list = [
                    Coordinate(37.096542, -8.473348),
                    Coordinate(37.095747, -8.470210),
                    Coordinate(37.097643, -8.470783)
        ]

        in_coord = Coordinate(37.097022, -8.471147)
        is_pt_inside = in_coord.is_inside_polygon(coord_list)
        self.assertTrue(is_pt_inside)

        out_coord = Coordinate(37.097598, -8.469701)
        is_pt_inside = out_coord.is_inside_polygon(coord_list)
        self.assertFalse(is_pt_inside)


    def test_two_points_fail(self):
        coord_list = [
                    Coordinate(37.099623, -8.469745),
                    Coordinate(37.099623, -8.469745),
        ]

        with self.assertRaises(NotAPolygonError):
            in_coord = Coordinate(37.099623, -8.46974)
            is_pt_inside = in_coord.is_inside_polygon(coord_list)

    def test_repeated_point_fail(self):
        coord_list = [
                Coordinate(31.000213,-87.584839),
                Coordinate(31.009629,-85.003052),
                Coordinate(30.726726,-84.838257),
                Coordinate(30.584962,-82.168579),
                Coordinate(30.73617,-81.476441),
                Coordinate(29.002375,-80.795288),
                Coordinate(26.896598,-79.938355),
                Coordinate(25.813738,-80.059204),
                Coordinate(24.93028,-80.454712),
                Coordinate(24.401135,-81.817017),
                Coordinate(24.700927,-81.959839),
                Coordinate(24.950203,-81.124878),
                Coordinate(26.0015,-82.014771),
                Coordinate(27.833247,-83.014527),
                Coordinate(28.8389,-82.871704),
                Coordinate(29.987293,-84.091187),
                Coordinate(29.539053,-85.134888),
                Coordinate(30.272352,-86.47522),
                Coordinate(30.281839,-87.628784),
                Coordinate(30.281839,-87.628784),
            ]
        with self.assertRaises(NotAPolygonError):
            out_coord = Coordinate(24.311058,-81.17981)
            is_pt_inside = out_coord.is_inside_polygon(coord_list)

    def test_coord_is_not_dict(self):
        coord = Coordinate(1, 2)
        d = {'a':'b'}
        self.assertNotEqual(coord, d)
