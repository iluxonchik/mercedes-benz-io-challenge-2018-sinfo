"""Listing vehicles tests."""
import unittest
import json
from mbio.testdrive import TestDrive


class TestListVehiles(unittest.TestCase):
    """List vehicle by features tests."""

    def test_list_vehicles_by_model_no_results(self):
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        expected = []
        obtained = td.get_vehicles_by_model('Z')
        self.assertCountEqual(expected, obtained,
                              'Mismatch in expected (empty) and obtained list '
                              'of model Z vehicles query')

    def test_list_vehicles_by_model(self):
        EXPECTED_JSON_FILE_PATH = './tests/resources/expected_vehicles_model_e.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            vehicle_list = json.load(f)
        expected = vehicle_list['vehicles']
        obtained = td.get_vehicles_by_model('E')
        self.assertCountEqual(expected, obtained, 'Mismatch in obtained '
                                                  'model E vehicle listing.')

    def test_list_vehicles_by_model_case_mixture(self):
        EXPECTED_JSON_FILE_PATH = './tests/resources/expected_vehicles_model_e.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            vehicle_list = json.load(f)
        expected = vehicle_list['vehicles']
        obtained = td.get_vehicles_by_model('e')
        self.assertCountEqual(expected, obtained, 'Mismatch in obtained '
                                                  'model E vehicle listing '
                                                  'when using mixed letter '
                                                  'case.')

    def test_list_vehicles_by_fuel_type_no_results(self):
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        expected = []
        obtained = td.get_vehicles_by_fuel_type('PENAUT BUTTER')
        self.assertCountEqual(expected, obtained,
                              'Mismatch in expected (empty) and obtained list '
                              'of PENAUT BUTTER fuel type query')
