"""Date-related tests."""
import unittest
import json
import datetime
from mbio.testdrive import TestDrive
from mbio.date.bookingdate import BookingDate, BookingResponse

class DateTimeTestCase(unittest.TestCase):
    """Tests related to the datetime.datetime wrapper."""

    def test_vehicle_reservation_is_compatible(self):
        EXPECTED_JSON_FILE_PATH  = './tests/resources/vehicle_and_bookings.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            json_dict = json.load(f)
        vehicle = json_dict['vehicle']
        bookings = json_dict['bookings']

        pickup_date = datetime.datetime(2019, 4, 9, 10, 0)

        td_booking_date = BookingDate(datetime=pickup_date)

        booking_result = td_booking_date.is_booking_possible(vehicle=vehicle, bookings=bookings)
        booking_available = booking_result.is_success
        error_code = booking_result.error_code

        self.assertIsNone(error_code, 'Error code should have been None, '
                                      'but is not.')

        self.assertTrue(booking_available, 'Booking should be available, but '
                                           'is not.')

    def test_vehicle_reservation_is_compatible_empty_booking_list(self):
        EXPECTED_JSON_FILE_PATH  = './tests/resources/vehicle_and_bookings.json'
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            json_dict = json.load(f)
        vehicle = json_dict['vehicle']
        bookings = []

        pickup_date = datetime.datetime(2019, 4, 9, 10, 0)

        td_booking_date = BookingDate(datetime=pickup_date)

        booking_result = td_booking_date.is_booking_possible(vehicle=vehicle, bookings=bookings)
        booking_available = booking_result.is_success
        error_code = booking_result.error_code

        self.assertIsNone(error_code, 'Error code should have been None, '
                                      'but is not.')

        self.assertTrue(booking_available, 'Booking should be available, but '
                                           'is not.')

    def test_vehicle_reservation_is_not_compatible_booking_exits(self):
        EXPECTED_JSON_FILE_PATH  = './tests/resources/vehicle_and_bookings.json'
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            json_dict = json.load(f)
        vehicle = json_dict['vehicle']
        bookings = json_dict['bookings']

        pickup_date = datetime.datetime(2018, 3, 5, 10, 30)

        td_booking_date = BookingDate(datetime=pickup_date)

        booking_result = td_booking_date.is_booking_possible(vehicle=vehicle, bookings=bookings)
        booking_available = booking_result.is_success
        error_code = booking_result.error_code

        self.assertEqual(error_code, BookingResponse.ERR_BOOKING_EXITS, 'Wrong error code.')

        self.assertFalse(booking_available, 'Booking should not be available, '
                                            'it is.')

    def test_vehicle_reservation_is_not_compatible_vehicle_date(self):
        EXPECTED_JSON_FILE_PATH  = './tests/resources/vehicle_and_bookings.json'
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            json_dict = json.load(f)
        vehicle = json_dict['vehicle']
        bookings = json_dict['bookings']

        pickup_date = datetime.datetime(2019, 4, 10, 10, 0)

        td_booking_date = BookingDate(datetime=pickup_date)

        booking_result = td_booking_date.is_booking_possible(vehicle=vehicle, bookings=bookings)
        booking_available = booking_result.is_success
        error_code = booking_result.error_code

        self.assertEqual(error_code, BookingResponse.ERR_CAR_DATE, 'Wrong error code.')

        self.assertFalse(booking_available, 'Booking should not be available, '
                                            'it is.')

    def test_vehicle_reservation_is_not_compatible_vehicle_time(self):
        EXPECTED_JSON_FILE_PATH = './tests/resources/vehicle_and_bookings.json'
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            json_dict = json.load(f)
        vehicle = json_dict['vehicle']
        bookings = json_dict['bookings']

        pickup_date = datetime.datetime(2019, 4, 9, 5, 0)

        td_booking_date = BookingDate(datetime=pickup_date)

        booking_result = td_booking_date.is_booking_possible(vehicle=vehicle, bookings=bookings)
        booking_available = booking_result.is_success
        error_code = booking_result.error_code

        self.assertEqual(error_code, BookingResponse.ERR_CAR_DATE, 'Wrong error code.')

        self.assertFalse(booking_available, 'Booking should not be available, '
                                            'it is.')

    def test_vehicle_cancelled_reservation_is_compatible(self):
        EXPECTED_JSON_FILE_PATH  = './tests/resources/vehicle_and_bookings_cancelled.json'
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            json_dict = json.load(f)
        vehicle = json_dict['vehicle']
        bookings = json_dict['bookings']

        pickup_date = datetime.datetime(2018, 3, 5, 10, 30)

        td_booking_date = BookingDate(datetime=pickup_date)

        booking_result = td_booking_date.is_booking_possible(vehicle=vehicle, bookings=bookings)
        booking_available = booking_result.is_success
        error_code = booking_result.error_code

        self.assertIsNone(error_code, 'Error code should have been None, '
                                      'but is not.')

        self.assertTrue(booking_available, 'Booking should be available, but '
                                           'is not.')
