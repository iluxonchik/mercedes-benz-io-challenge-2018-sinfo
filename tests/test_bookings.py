"""Booking creation and cancelling tests."""
import copy
import uuid
import datetime
import unittest
from unittest.mock import patch
from mbio.testdrive import TestDrive
from mbio.exceptions import (VehicleNotFoundError, VehicleAlreadyBookedError,
                             VehicleNotAvailableOnDateError, BookingError,
                             BookingAlreadyCancelledError, BookingDoesNotExistError)
from mbio.date.bookingdate import BookingResponse

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
                    		"id": str(UUID_stub),
                    		"firstName": "Jayceon",
                    		"lastName": "Taylor",
                    		"vehicleId": vehicle_id,
                    		"pickupDate": pickup_date.isoformat(),
                    		"createdAt": MockedDateTime.MOCKED_DATE_VALUE.isoformat()
                    }
        obtained_booking = result
        self.assertIsNotNone(obtained_booking, 'No booking returned')
        self.assertEqual(expected_booking, obtained_booking,
                         'Erroneous booking obtained.')
        dataset = td._dataset
        bookings = dataset['bookings']
        self.assertTrue(obtained_booking in bookings, 'New booking was not '
                        'added to the dataset.')

    def test_booking_booking_exists_fail(self):
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        vehicle_id = '136fbb51-8a06-42fd-b839-c01ab87e2c6c'
        # reservation for April 9th at 10:00 (Tuesday)
        pickup_date = datetime.datetime(2018, 3, 5, 10, 00)
        with self.assertRaises(VehicleAlreadyBookedError):
            result = td.create_booking(first_name='Jayceon', last_name='Taylor',
                          vehicle_id=vehicle_id,
                          pickup_date=pickup_date)

    def test_booking_unavailable_datetime_fail(self):
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        vehicle_id = '136fbb51-8a06-42fd-b839-c01ab87e2c6c'
        original_dataset = copy.deepcopy(td._dataset)
        # reservation for April 9th at 10:00 (Tuesday)
        pickup_date = datetime.datetime(2018, 3, 5, 10, 2)
        with self.assertRaises(VehicleNotAvailableOnDateError):
            result = td.create_booking(first_name='Jayceon', last_name='Taylor',
                          vehicle_id=vehicle_id,
                          pickup_date=pickup_date)
        # make sure dataset was not modified
        self.assertEqual(original_dataset, td._dataset, 'Dataset has been changed.')

    def test_booking_vehicle_does_not_exist_fail(self):
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        vehicle_id = '136fbb51-8a06-42fd-1992-c01ab87e2c6c'
        original_dataset = copy.deepcopy(td._dataset)
        # reservation for April 9th at 10:00 (Tuesday)
        pickup_date = datetime.datetime(2018, 3, 5, 10, 0)
        with self.assertRaises(VehicleNotFoundError):
            result = td.create_booking(first_name='Jayceon', last_name='Taylor',
                          vehicle_id=vehicle_id,
                          pickup_date=pickup_date)
        # make sure dataset was not !modified
        self.assertEqual(original_dataset, td._dataset, 'Dataset has been changed.')

    @patch.object(BookingResponse, 'error_code')
    def test_booking_error_code_failure_fail(self, br):
        """Emulates what would happen if the error code was set to something
        unexpected"""
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        vehicle_id = '136fbb51-8a06-42fd-b839-c01ab87e2c6c'
        original_dataset = copy.deepcopy(td._dataset)
        # reservation for April 9th at 10:00 (Tuesday)
        pickup_date = datetime.datetime(2018, 3, 6, 10, 0)
        with self.assertRaises(BookingError):
            result = td.create_booking(first_name='Jayceon', last_name='Taylor',
                          vehicle_id=vehicle_id,
                          pickup_date=pickup_date)
        # make sure dataset was not modified
        self.assertEqual(original_dataset, td._dataset, 'Dataset has been changed.')

    @patch.object(uuid, 'uuid4', side_effect=MOCKED_UUIDS)
    def test_double_booking_fail(self, uuid):
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
                    		"id": str(UUID_stub),
                    		"firstName": "Jayceon",
                    		"lastName": "Taylor",
                    		"vehicleId": vehicle_id,
                    		"pickupDate": pickup_date.isoformat(),
                    		"createdAt": MockedDateTime.MOCKED_DATE_VALUE.isoformat()
                    }
        obtained_booking = result
        self.assertIsNotNone(obtained_booking, 'No booking returned')
        self.assertEqual(expected_booking, obtained_booking,
                         'Erroneous booking obtained.')
        dataset = td._dataset
        bookings = dataset['bookings']
        self.assertTrue(obtained_booking in bookings, 'New booking was not '
                        'added to the dataset.')

        with self.assertRaises(VehicleAlreadyBookedError):
            result = td.create_booking(first_name='Jayceon', last_name='Taylor',
                                      vehicle_id=vehicle_id,
                                      pickup_date=pickup_date)
        # make sure booking is still there
        dataset = td._dataset
        bookings = dataset['bookings']
        self.assertTrue(obtained_booking in bookings, 'New booking was not '
                        'added to the dataset.')

    def test_cancel_booking_success(self):
        booking_id = '184b5438-35dc-49c4-aab0-e6cf62285aa6'
        reason = "Can't bang Dr.Dre with good enough sound quality."
        td = TestDrive(dataset='./tests/resources/dataset_full.json')

        original = {
			"id": "184b5438-35dc-49c4-aab0-e6cf62285aa6",
			"firstName": "Marcus",
			"lastName": "Cruz",
			"vehicleId": "44a36bfa-ec8f-4448-b4c2-809203bdcb9e",
			"pickupDate": "2018-03-04T10:30:00",
			"createdAt": "2018-02-26T08:42:46.291"
		}

        self.assertIn(original, td._dataset['bookings'])

        obtained = td.cancel_booking(booking_id, reason=reason)
        expected = {
			"id": "184b5438-35dc-49c4-aab0-e6cf62285aa6",
			"firstName": "Marcus",
			"lastName": "Cruz",
			"vehicleId": "44a36bfa-ec8f-4448-b4c2-809203bdcb9e",
			"pickupDate": "2018-03-04T10:30:00",
			"createdAt": "2018-02-26T08:42:46.291",
            "cancelledAt": MockedDateTime.MOCKED_DATE_VALUE.isoformat(),
            "cancelledReason": reason,
    	}

        self.assertEqual(expected, obtained)
        # make sure booking was removed from the dataset
        self.assertNotIn(original, td._dataset['bookings'])
        # make sure cancelled booking has been added to the dataset
        self.assertIn(expected, td._dataset['bookings'])

    def test_double_cancel_booking_fail(self):
        booking_id = '184b5438-35dc-49c4-aab0-e6cf62285aa6'
        reason = "Can't bang Dr.Dre with good enough sound quality."
        td = TestDrive(dataset='./tests/resources/dataset_full.json')

        original = {
			"id": "184b5438-35dc-49c4-aab0-e6cf62285aa6",
			"firstName": "Marcus",
			"lastName": "Cruz",
			"vehicleId": "44a36bfa-ec8f-4448-b4c2-809203bdcb9e",
			"pickupDate": "2018-03-04T10:30:00",
			"createdAt": "2018-02-26T08:42:46.291"
		}

        self.assertIn(original, td._dataset['bookings'])

        obtained = td.cancel_booking(booking_id, reason=reason)
        expected = {
			"id": "184b5438-35dc-49c4-aab0-e6cf62285aa6",
			"firstName": "Marcus",
			"lastName": "Cruz",
			"vehicleId": "44a36bfa-ec8f-4448-b4c2-809203bdcb9e",
			"pickupDate": "2018-03-04T10:30:00",
			"createdAt": "2018-02-26T08:42:46.291",
            "cancelledAt": MockedDateTime.MOCKED_DATE_VALUE.isoformat(),
            "cancelledReason": reason,
    	}

        # make sure cancelled booking has been added to the dataset
        self.assertIn(expected, td._dataset['bookings'])

        new_reason = 'Would you do it if my name was Dre?'
        not_expected = {
			"id": "184b5438-35dc-49c4-aab0-e6cf62285aa6",
			"firstName": "Marcus",
			"lastName": "Cruz",
			"vehicleId": "44a36bfa-ec8f-4448-b4c2-809203bdcb9e",
			"pickupDate": "2018-03-04T10:30:00",
			"createdAt": "2018-02-26T08:42:46.291",
            "cancelledAt": MockedDateTime.MOCKED_DATE_VALUE.isoformat(),
            "cancelledReason": new_reason,
    	}


        with self.assertRaises(BookingAlreadyCancelledError):
            td.cancel_booking(booking_id, reason=new_reason)

        self.assertIn(expected, td._dataset['bookings'])
        self.assertNotIn(new_reason, td._dataset['bookings'])

    def test_double_cancel_booking_does_not_exit_fail(self):
        booking_id = "The product of Gin and Juice inside of my baby bottle."
        reason = "Can't bang Dr.Dre with good enough sound quality."
        td = TestDrive(dataset='./tests/resources/dataset_full.json')

        with self.assertRaises(BookingDoesNotExistError):
            td.cancel_booking(booking_id, 'I Grew Up On Wu-Tang')

    def test_cancel_booking_then_reserve_for_that_date(self):
        # TODO
        pass
