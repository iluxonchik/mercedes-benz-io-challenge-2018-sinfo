"""Booking creation and cancelling tests."""
import unittest
from unittest.mock import patch
from mbio.testdrive import TestDrive
import datetime
import uuid

MOCKED_UUIDS = ['136fbb51-8a06-42fd-b839-d01ab87e2c6c', '136fbb51-8a06-42fd-b839-c01ab87e2c6b',
'132fbb51-8a06-42fd-b839-c01ab87e2c6c']

class MockedDateTime(datetime.datetime):
    MOCKED_DATE_VALUE = datetime.datetime(2018, 10, 3, 19, 22, 19, 92)
    @classmethod
    def today(cls):
        return cls.MOCKED_DATE_VALUE

class BookingsTestCase(unittest.TestCase):
    """Tests related to making and cancelling bookings."""
    #
    # When doing a booking:
    #     1. make sure vehicle_id exists (else: Exception)
    #     ------- Below handeled by BookingDate Class ----
    #     2. make sure vehicle is available on day/time (else: Exception)
    #             (else: Exception)
    #     3. make sure that that vehicle_id is not registered for that date already,
    #             UNLESS booking is cancelled(else: Exception)
    #     4. OK: create booking
    #

    @classmethod
    def setUpClass(cls):
        datetime.datetime = MockedDateTime

    @patch.object(uuid, 'uuid4', side_effect=MOCKED_UUIDS)
    def test_booking_success(self, uuid):
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        vehicle_id = '136fbb51-8a06-42fd-b839-c01ab87e2c6c'
        # reservation for April 9th at 10:00 (Tuesday)
        pickup_date = datetime.datetime(2019, 4, 9, 10, 00)
        result = td.create_booking(first_name='Jayceon', last_name='Taylor',
                          vehicle_id=vehicle_id,
                          pickup_date=pickup_date)

        # now, make sure that a booking object was created and added
        UUID_stub = MOCKED_UUIDS[0]

        expected_booking = {
                    		"id": UUID_stub,
                    		"firstName": "Jayceon",
                    		"lastName": "Taylor",
                    		"vehicleId": vehicle_id,
                    		"pickupDate": pickup_date.isoformat(),
                    		"createdAt": MockedDateTime.MOCKED_DATE_VALUE
                    }
        obtained_booking = result
        self.assertIsNotNone(obtained_booking, 'No booking returned')
        self.assertEqual(expected_booking, obtained_booking,
                         'Erroneous booking obtained.')
        dataset = td._dataset
        bookings = dataset['bookings']
        self.assertTrue(obtained_booking in bookings, 'New booking was not '
                        'added to the dataset.')
