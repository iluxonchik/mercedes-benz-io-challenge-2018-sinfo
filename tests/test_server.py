"""Tests for the HTTP server."""

import unittest
import threading
import json
import urllib.request
from http.server import HTTPServer

from mbio.server.endpoint import Endpoint
from mbio.server.server import Server
from http.server import HTTPServer


class TestHTTPServer(HTTPServer):

    def shutdown(self):
        super(TestHTTPServer, self).shutdown()
        self.server_close()


class RESTServerTestCase(unittest.TestCase):
    SERVER_PORT = 1234

    def setUp(self):
        Server.DATASET_PATH = './tests/resources/dataset_full.json'

        server_address = ('', RESTServerTestCase.SERVER_PORT)
        self.httpd = TestHTTPServer(server_address, Server)
        self.thr = threading.Thread(target=self.httpd.serve_forever)
        self.thr.start()

    def tearDown(self):
        self.httpd.shutdown()
        self.thr.join()

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

    def _get_request(self, endpoint):
        url = 'http://localhost:{}{}'.format(RESTServerTestCase.SERVER_PORT, endpoint)
        req = urllib.request.Request(url)

        with urllib.request.urlopen(req) as response:
            res = response.read()

        res = res.decode('utf-8')
        return res
