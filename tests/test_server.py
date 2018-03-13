"""Tests for the HTTP server"""
import unittest
import threading
import urllib.request
from http.server import HTTPServer
from socketserver import ThreadingMixIn

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
        print('Server is running!')

    def tearDown(self):
        self.httpd.shutdown()
        self.thr.join()

    def test_get_vehicles(self):
        print('Hello')
    def test_another_simple(self):
        print('Another hello')
