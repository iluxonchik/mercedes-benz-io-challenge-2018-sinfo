"""BookingDate class implementation."""
from collections import defaultdict
from mbio.date.utils import isoformat_to_datetime

class BookingResponse(object):
    """Response to the request of the booking availability."""
    ERR_CAR_DATE = 0
    ERR_BOOKING_EXITS = 1

    def __init__(self, is_success, error_code=None):
        self._is_success = is_success
        self._error_code = error_code

    @property
    def is_success(self):
        return self._is_success

    @property
    def error_code(self):
        return self._error_code

class BookingDate(object):
    """Wrapper around datetime.datetime that abstracts booking availability checking."""

    DATE_MAP = {
                'monday': 0,
                'tuesday': 1,
                'wednesday': 2,
                'thursday': 3,
                'friday': 4,
                'saturday': 5,
                'sunday': 6
                }

    def __init__(self, datetime):
        self._datetime = datetime

    def is_booking_possible(self, vehicle, bookings=[]):
        """
        1. make sure vehicle is available on day/time
        2. make sure that that vehicle_id is not registered for that date already,
              UNLESS booking is cancelled
        """
        vehicle_availability = self._parse_availability(vehicle['availability'])
        is_vehicle_compatible = self._is_vehicle_availabile(self._datetime, vehicle_availability, bookings)
        return is_vehicle_compatible


    def _is_vehicle_availabile(self, datetime, vehicle_availability, bookings):
        booking_day = datetime.weekday()
        bookin_hour = datetime.hour
        booking_minute = datetime.minute
        booking_time_tuple = (bookin_hour, booking_minute)

        # make sure that the vehicle is available on a cerntain date/time
        available_hours = vehicle_availability[booking_day]
        if not booking_time_tuple in available_hours:
            return BookingResponse(False, BookingResponse.ERR_CAR_DATE)


        booking_datetimes = []
        for booking in bookings:
            if 'cancelledAt' in booking:
                # ignore cancelled bookings
                continue
            booking_datetime_str = booking['pickupDate']
            booking_datetime = isoformat_to_datetime(booking_datetime_str)
            booking_datetimes.append(booking_datetime)

        if self._datetime in booking_datetimes:
            return BookingResponse(False, BookingResponse.ERR_BOOKING_EXITS)

        return BookingResponse(True)

    def _parse_availability(self, availability):
        res = defaultdict(list)
        for day, time in availability.items():
            for t in time:
                hour = int(t[0:2])
                minute = int(t[2:4])
                day_integer = self.DATE_MAP[day.lower()]
                res[day_integer].append((hour, minute))
        return res
