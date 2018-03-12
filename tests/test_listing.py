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

    def test_list_vehicles_by_model_mixed_case(self):
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
                              'of PENAUT BUTTER fuel type query.')

    def test_list_vehicles_by_fuel_type_electric(self):
        self.maxDiff = None
        EXPECTED_JSON_FILE_PATH = './tests/resources/expected_vehicles_fuel_type_electric.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            vehicle_list = json.load(f)
        expected = vehicle_list['vehicles']
        obtained = td.get_vehicles_by_fuel_type('ELECTRIC')
        self.assertCountEqual(expected, obtained, 'Mismatch in obtained '
                                                  'ELECTRIC fuel type vehicle '
                                                  'listing.')

    def test_list_vehicles_by_fuel_type_electric_mixed_case(self):
        EXPECTED_JSON_FILE_PATH = './tests/resources/expected_vehicles_fuel_type_electric.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            vehicle_list = json.load(f)
        expected = vehicle_list['vehicles']
        obtained = td.get_vehicles_by_fuel_type('EleCtRIc')
        self.assertCountEqual(expected, obtained, 'Mismatch in obtained '
                                                  'ELECTRIC fuel type vehicle '
                                                  'listing when using mixed '
                                                  'case.')

    def test_list_vehicles_by_transmission_no_results(self):
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        expected = []
        obtained = td.get_vehicles_by_transmission('THE DOCUMENTARY')
        self.assertCountEqual(expected, obtained,
                              'Mismatch in expected (empty) and obtained list '
                              'of MANUAL transmission query.')

    def test_list_vehicles_by_transmission_manual(self):
        self.maxDiff = None
        EXPECTED_JSON_FILE_PATH = './tests/resources/expected_vehicles_transmission_manual.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            vehicle_list = json.load(f)
        expected = vehicle_list['vehicles']
        obtained = td.get_vehicles_by_transmission('MANUAL')
        self.assertCountEqual(expected, obtained, 'Mismatch in obtained '
                                                  'MANUAL transmission vehicle '
                                                  'listing.')

    def test_list_vehicles_by_transmission_manual_mixed_case(self):
        self.maxDiff = None
        EXPECTED_JSON_FILE_PATH = './tests/resources/expected_vehicles_transmission_manual.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            vehicle_list = json.load(f)
        expected = vehicle_list['vehicles']
        obtained = td.get_vehicles_by_transmission('mANUAl')
        self.assertCountEqual(expected, obtained, 'Mismatch in obtained '
                                                  'MANUAL transmission vehicle'
                                                  ' listing when using mixed '
                                                  'case.')

    def test_list_vehicles_by_dealer_no_results(self):
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        expected = []
        obtained = td.get_vehicles_by_dealer('Carvoeiro')
        self.assertCountEqual(expected, obtained,
                              'Mismatch in expected (empty) and obtained list '
                              'of Carvoeiro deler query.')

    def test_list_vehicles_by_dealer_mb_albufeira(self):
        self.maxDiff = None
        EXPECTED_JSON_FILE_PATH = './tests/resources/expected_vehicles_dealer_mb_albufeira.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            vehicle_list = json.load(f)
        expected = vehicle_list['vehicles']
        obtained = td.get_vehicles_by_dealer('MB Albufeira')
        self.assertCountEqual(expected, obtained, 'Mismatch in obtained '
                                                  'MB Albufeira dealer '
                                                  'vehicles listing.')

    def test_list_vehicles_by_dealer_mb_albufeira_mixed_case(self):
        self.maxDiff = None
        EXPECTED_JSON_FILE_PATH = './tests/resources/expected_vehicles_dealer_mb_albufeira.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            vehicle_list = json.load(f)
        expected = vehicle_list['vehicles']
        obtained = td.get_vehicles_by_dealer('Mb AlBuFeiRa')
        self.assertCountEqual(expected, obtained, 'Mismatch in obtained '
                                                  'MB Albufeira dealer '
                                                  'vehicles listing when '
                                                  'using mixed case.')

    # Tests for general get_vehicles_by_attributes() method
    def test_attr_list_vehicles_by_model_no_results(self):
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        expected = []
        obtained = td.get_vehicles_by_attributes(model='Z')
        self.assertCountEqual(expected, obtained,
                              'Mismatch in expected (empty) and obtained list '
                              'of model Z vehicles query')

    def test_attr_list_vehicles_by_model(self):
        EXPECTED_JSON_FILE_PATH = './tests/resources/expected_vehicles_model_e.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            vehicle_list = json.load(f)
        expected = vehicle_list['vehicles']
        obtained = td.get_vehicles_by_attributes(model='E')
        self.assertCountEqual(expected, obtained, 'Mismatch in obtained '
                                                  'model E vehicle listing.')

    def test_attr_list_vehicles_by_fuel_type_no_results(self):
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        expected = []
        obtained = td.get_vehicles_by_attributes(fuel='PENAUT BUTTER')
        self.assertCountEqual(expected, obtained,
                              'Mismatch in expected (empty) and obtained list '
                              'of PENAUT BUTTER fuel type query.')

    def test_attr_list_vehicles_by_fuel_type_electric(self):
        EXPECTED_JSON_FILE_PATH = './tests/resources/expected_vehicles_fuel_type_electric.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            vehicle_list = json.load(f)
        expected = vehicle_list['vehicles']
        obtained = td.get_vehicles_by_attributes(fuel='ELECTRIC')
        self.assertCountEqual(expected, obtained, 'Mismatch in obtained '
                                                  'ELECTRIC fuel type vehicle '
                                                  'listing.')

    def test_attr_list_vehicles_by_fuel_type_electric_mixed_case(self):
        EXPECTED_JSON_FILE_PATH = './tests/resources/expected_vehicles_fuel_type_electric.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            vehicle_list = json.load(f)
        expected = vehicle_list['vehicles']
        obtained = td.get_vehicles_by_attributes(fuel='EleCtRIc')
        self.assertCountEqual(expected, obtained, 'Mismatch in obtained '
                                                  'ELECTRIC fuel type vehicle '
                                                  'listing when using mixed '
                                                  'case.')

    def test_attr_list_vehicles_by_transmission_no_results(self):
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        expected = []
        obtained = td.get_vehicles_by_attributes(transmission='THE DOCUMENTARY')
        self.assertCountEqual(expected, obtained,
                              'Mismatch in expected (empty) and obtained list '
                              'of MANUAL transmission query.')

    def test_attr_list_vehicles_by_transmission_manual(self):
        self.maxDiff = None
        EXPECTED_JSON_FILE_PATH = './tests/resources/expected_vehicles_transmission_manual.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            vehicle_list = json.load(f)
        expected = vehicle_list['vehicles']
        obtained = td.get_vehicles_by_attributes(transmission='MANUAL')
        self.assertCountEqual(expected, obtained, 'Mismatch in obtained '
                                                  'MANUAL transmission vehicle '
                                                  'listing.')

    def test_attr_list_vehicles_by_dealer_no_results(self):
        self.maxDiff = None
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        expected = []
        obtained = td.get_vehicles_by_attributes(dealer='Carvoeiro')
        self.assertCountEqual(expected, obtained,
                              'Mismatch in expected (empty) and obtained list '
                              'of Carvoeiro deler query.')

        obtained = td.get_vehicles_by_attributes(dealer='Carvoeiro', model='E')
        self.assertCountEqual(expected, obtained,
                            'Mismatch in expected (empty) and obtained list '
                            'of Carvoeiro deler query.')


    def test_attr_list_vehicles_by_dealer_mb_albufeira(self):
        self.maxDiff = None
        EXPECTED_JSON_FILE_PATH = './tests/resources/expected_vehicles_dealer_mb_albufeira.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            vehicle_list = json.load(f)
        expected = vehicle_list['vehicles']
        obtained = td.get_vehicles_by_attributes(dealer='MB Albufeira')
        self.assertCountEqual(expected, obtained, 'Mismatch in obtained '
                                                  'MB Albufeira dealer '
                                                  'vehicles listing.')
