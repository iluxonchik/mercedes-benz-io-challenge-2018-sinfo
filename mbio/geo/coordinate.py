"""Coordinate class and distance computation."""
from math import radians, cos, sin, asin, sqrt, pi, atan2
from mbio.geo.exceptions import NotAPolygonError
from mbio.utils import are_list_items_unique


class Coordinate(object):

    EARTH_RADIUS = 6371

    def __init__(self, latitude, longitude):
        self._latitude = latitude
        self._longitude = longitude

        self._latitude_rad = radians(self.latitude)
        self._longitude_rad = radians(self.longitude)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.latitude == other.latitude and self.longitude == other.longitude
        return False

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def latitude_rad(self):
        return self._latitude_rad

    @property
    def longitude_rad(self):
        return self._longitude_rad

    def distance_to(self, other):
        """
        Compute distance from one Coordinate to another in kilometers.

        Haversine formula is used. Precision of tree points (meter precision).
        """
        dlat = self.latitude_rad - other.latitude_rad
        dlon = self.longitude_rad - other.longitude_rad
        a = sin(dlat/2)**2 + cos(self.latitude_rad) * cos(other.latitude_rad) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        distance = c * self.EARTH_RADIUS
        return round(distance, 3)

    def is_inside_polygon(self, coord_list):
        self._check_if_polygon(coord_list)

        angle = 0
        num_coords = len(coord_list)

        for i in range(num_coords):
            curr_coord = coord_list[i]
            next_coord = coord_list[(i+1)%num_coords]

            curr_pt_lat = curr_coord.latitude - self.latitude
            curr_pt_lon = curr_coord.longitude - self.longitude

            next_pt_lat = next_coord.latitude - self.latitude
            next_pt_lon = next_coord.longitude - self.longitude

            angle += self._2d_angle(curr_pt_lat, curr_pt_lon, next_pt_lat, next_pt_lon)

        if abs(angle) < pi:
            return False
        else:
            return True

    def _check_if_polygon(self, coord_list):
        if len(coord_list) < 3:
            raise NotAPolygonError('A polygon has at least 3 points.')

        all_coords_unique = are_list_items_unique(coord_list)
        if not all_coords_unique:
            raise NotAPolygonError('A polygon must have all of its points distinct.')

    def _2d_angle(self, pt1_lat, pt1_lon, pt2_lat, pt2_lon):
        theta_1 = atan2(pt1_lat, pt1_lon)
        theta_2 = atan2(pt2_lat, pt2_lon)
        dtheta = theta_2 - theta_1

        while dtheta > pi:
            dtheta -= 2*pi

        while dtheta < -pi:
            dtheta += 2*pi

        return dtheta
