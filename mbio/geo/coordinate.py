"""Coordinate class and distance computation."""
from math import radians, cos, sin, asin, sqrt


class Coordinate(object):

    EARTH_RADIUS = 6371

    def __init__(self, latitude, longitude):
        self._latitude = latitude
        self._longitude = longitude

        self._latitude_rad = radians(self.latitude)
        self._longitude_rad = radians(self.longitude)

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
