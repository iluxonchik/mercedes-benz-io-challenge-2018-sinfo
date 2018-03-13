"""Tests for the HTTP server."""

import unittest
import threading
import json
import urllib.request
import urllib.parse
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import datetime
import uuid
from http.server import HTTPServer
from unittest.mock import patch

from mbio.server.endpoint import Endpoint
from mbio.server.server import Server

MOCKED_UUIDS = ['136fbb51-8a06-42fd-b839-d01ab87e2c6c', '136fbb51-8a06-42fd-b839-c01ab87e2c6b',
'132fbb51-8a06-42fd-b839-c01ab87e2c6c']

class TestHTTPServer(HTTPServer):

    def shutdown(self):
        super(TestHTTPServer, self).shutdown()
        self.server_close()

class MockedDateTime(datetime.datetime):
    MOCKED_DATE_VALUE = datetime.datetime(2018, 10, 3, 19, 22, 19, 92)
    @classmethod
    def today(cls):
        return cls.MOCKED_DATE_VALUE

class RESTServerTestCase(unittest.TestCase):
    SERVER_PORT = 1234

    @classmethod
    def setUpClass(cls):
        datetime.datetime = MockedDateTime

    def setUp(self):
        Server.DATASET_PATH = './tests/resources/dataset_full.json'

        server_address = ('', RESTServerTestCase.SERVER_PORT)
        self.httpd = TestHTTPServer(server_address, Server)
        self.thr = threading.Thread(target=self.httpd.serve_forever)
        self.thr.start()

    def tearDown(self):
        self.httpd.shutdown()
        self.thr.join()

    def test_server_crashes_on_invalid_dataset(self):
        with self.assertRaises(Exception):
            Server.td = None
            Server.DATASET_PATH = 'Still Dre Day'
            Server()

    def test_server_error_get_on_post(self):
        expected = {
                    "error": "This endpoint only supports the POST method."
                   }
        res = self._get_request('{}'.format(Endpoint.BOOKINGS_CREATE))
        obtained = json.loads(res)

        self.assertEqual(expected, obtained)

    def test_server_error_post_on_get(self):
        expected = {
                    "error": "This endpoint only supports the GET method."
                   }
        res = self._post_request('{}'.format(Endpoint.VEHICLES), {'a':'b'})
        obtained = json.loads(res)

        self.assertEqual(expected, obtained)

    def test_unknown_endpoint_get_error(self):
        expected =  {
                    "error": "Unknown endpoint."
                    }

        res = self._get_request('{}'.format('/the-documentary/album/'))
        obtained = json.loads(res)

        self.assertEqual(expected, obtained)

    def test_unknown_endpoint_post_error(self):
        expected =  {
                    "error": "Unknown endpoint."
                    }

        res = self._post_request('{}'.format('/the-the-chronic/album/'), {})
        obtained = json.loads(res)

        self.assertEqual(expected, obtained)

    def test_unknown_endpoint_put_error(self):
        expected =  {
                    "error": "Unknown endpoint."
                    }

        res = self._put_request('{}'.format('/the-the-chronic/album/'), {})
        obtained = json.loads(res)

        self.assertEqual(expected, obtained)

    def test_get_vehicles(self):
        EXPECTED_JSON_FILE_PATH = './tests/resources/expected_all_vehicles.json'
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            expected = json.load(f)

        res = self._get_request('{}'.format(Endpoint.VEHICLES))
        obtained = json.loads(res)

        self.assertEqual(expected, obtained)

    def test_get_specific_vehicle(self):
        EXPECTED_JSON_FILE_PATH = './tests/resources/expected_specific_vehicle.json'
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            expected = json.load(f)

        res = self._get_request('{}?model=E&fuel=electric&transmission=auto&dealer=846679bd-5831-4286-969b-056e9c89d74c'.format(Endpoint.VEHICLES))
        obtained = json.loads(res)

        self.assertEqual(expected, obtained)

    @patch.object(uuid, 'uuid4', side_effect=MOCKED_UUIDS)
    def test_create_booking(self, uuid):

        data = {
                "first_name": "Jayceon",
                "last_name": "Taylor",
                "vehicle_id": "136fbb51-8a06-42fd-b839-c01ab87e2c6c",
                "pickup_date": "2019-04-08T10:30:00"
               }

        res = self._post_request('{}'.format(Endpoint.BOOKINGS_CREATE), data)
        obtained = json.loads(res)

        expected = {
            "id": MOCKED_UUIDS[0],
            "firstName": "Jayceon",
            "lastName": "Taylor",
            "vehicleId": "136fbb51-8a06-42fd-b839-c01ab87e2c6c",
            "pickupDate": "2019-04-08T10:30:00",
            "createdAt":  MockedDateTime.MOCKED_DATE_VALUE.isoformat(),
        }

        self.assertEqual(expected, obtained)

    def test_create_booking_invalid_date(self):
        expected = {
                "error": "2019-04-08a10:30:00 is not a valid ISO date format"
        }

        data = {
                "first_name": "Jayceon",
                "last_name": "Taylor",
                "vehicle_id": "136fbb51-8a06-42fd-b839-c01ab87e2c6c",
                "pickup_date": "2019-04-08a10:30:00"
               }

        res = self._post_request('{}'.format(Endpoint.BOOKINGS_CREATE), data)
        obtained = json.loads(res)
        self.assertEqual(expected, obtained)

    def test_cancel_booking(self):
        data = {
                  "booking_id": "b00d3e76-9605-49c7-910b-03b51679f6d6",
                  "reason": "On a scale from one to ten I'm a nine, with two M's"
               }

        res = self._put_request('{}'.format(Endpoint.BOOKINGS_CANCEL), data)
        obtained = json.loads(res)

        expected = {
                    "id": "b00d3e76-9605-49c7-910b-03b51679f6d6",
                    "firstName": "Joanna",
                    "lastName": "Walker",
                    "vehicleId": "875f00fa-9f67-44ea-bb26-75ff375fdd3f",
                    "pickupDate": "2018-03-03T10:30:00",
                    "createdAt": "2018-02-26T08:42:46.298",
                    "cancelledAt": MockedDateTime.MOCKED_DATE_VALUE.isoformat(),
                    "cancelledReason": "On a scale from one to ten I'm a nine, with two M's"
                }

        self.assertEqual(expected, obtained)        

    def _get_request(self, endpoint):
        url = 'http://localhost:{}{}'.format(RESTServerTestCase.SERVER_PORT, endpoint)
        req = urllib.request.Request(url)

        try:
            with urllib.request.urlopen(req) as response:
                json_res = response.read().decode()
        except HTTPError as e:
            json_res = e.read().decode()

        return json_res

    def _post_request(self, endpoint, data):

        url = 'http://localhost:{}{}'.format(RESTServerTestCase.SERVER_PORT, endpoint)

        try:
            request = Request(url, json.dumps(data).encode())
            json_res = urlopen(request).read().decode()
        except HTTPError as e:
            json_res = e.read().decode()

        return json_res

    def _put_request(self, endpoint, data):

        url = 'http://localhost:{}{}'.format(RESTServerTestCase.SERVER_PORT, endpoint)

        try:
            request = Request(url, json.dumps(data).encode(), method='PUT')
            json_res = urlopen(request).read().decode()
        except HTTPError as e:
            json_res = e.read().decode()

        return json_res
