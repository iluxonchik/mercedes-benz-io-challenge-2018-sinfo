"""Listing vehicles tests."""
import unittest
from mbio.testdrive import TestDrive


class TestListVehiles(unittest.TestCase):
    """List vehicle by features tests."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_list_vehicles_by_model_no_results(self):
        td = TestDrive(dataset='./resources/dataset_full.json')
        expected = []
        obtained = td.get_vehicles_by_model('Z')
        self.assertCountEqual(expected, obtained,
                              'Mismatch in expected (empty) and obtained list '
                              'of model Z vehicles query')
