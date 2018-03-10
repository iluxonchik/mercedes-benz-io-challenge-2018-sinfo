"""Booking creation and cancelling tests."""
import unittest
from mbio.testdrive import TestDrive
import datetime

class BookingsTestCase(object):
    """Tests related to making and cancelling bookings."""
    #
    # When doing a booking:
    #     1. make sure vehicle_id exists (else: Exception)
    #     2. make sure delaer that has the vehicle_id (else: Exception)
    #     3. make sure vehicle is available on day/time (else: Exception)
    #             (else: Exception)
    #     4. make sure that that vehicle_id is not registered for that date already,
    #             UNLESS booking is cancelled(else: Exception)
    #     5. OK: create booking
    #

    def test_booking_success(self):
        return True
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        # reservation for April 9th at 10:00 (Tuesday)
        pikup_date = datetime.datetime(2019, 4, )
        td.create_booking(firstName='Jayceon', lastName='Taylor',
                          vehicleId='136fbb51-8a06-42fd-b839-c01ab87e2c6c',
                          pickupDate=sad)
