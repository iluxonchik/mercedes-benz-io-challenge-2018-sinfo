"""Listing dealers by distance tests."""

import unittest
import json
from mbio.testdrive import TestDrive


class TestListDealersByDistance(unittest.TestCase):
    """List vehicle by features tests."""

    LOC_1 = (38.187787, -8.104157)
    LOC_2 = (50.26487, 28.67669)

    def test_get_closest_dealer_no_results(self):
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        obtained = td.get_closest_dealer_with_vehicle(latitude=self.LOC_1[0],
            longitude=self.LOC_1[1], model='E', fuel='air', transmission='manual')
        self.assertIsNone(obtained, 'Dealer has been returned, when none '
                                    'should have.')

    def test_get_closest_dealer_two_matches(self):
        # REGEX: "model": "E",\n\t+"fuel": "ELECTRIC",\n\t+"transmission": "AUTO"
        EXPECTED_JSON_FILE_PATH  = './tests/resources/expected_closest_dealer_two_matches.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            dealers_list = json.load(f)
        expected = dealers_list['dealers'][0]
        obtained = td.get_closest_dealer_with_vehicle(self.LOC_1[0],
            self.LOC_1[1], 'E', 'electric', 'auto')
        self.assertEqual(expected, obtained, 'Wrong closest dealer '
                                                  'returned.')


    def test_get_closest_dealer_one_match(self):
        EXPECTED_JSON_FILE_PATH  = './tests/resources/expected_closest_dealer_two_matches.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            dealers_list = json.load(f)
        expected = dealers_list['dealers'][0]
        obtained = td.get_closest_dealer_with_vehicle(latitude=self.LOC_2[0],
            longitude=self.LOC_2[1], model='AMG', fuel='gasoline', transmission='manual')
        self.assertEqual(expected, obtained, 'Wrong closest dealer '
                                                  'returned.')

    def test_get_closest_dealer_no_attributes_used(self):
        EXPECTED_JSON_FILE_PATH  = './tests/resources/expected_closest_dealer_porto.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            dealer_dict = json.load(f)
        expected = dealer_dict['dealer']
        obtained = td.get_closest_dealer_with_vehicle(latitude=self.LOC_2[0],
            longitude=self.LOC_2[1])
        self.assertEqual(expected, obtained, 'Wrong closest dealer '
                                                  'returned.')

        # same as above, but with kwargs
        obtained = td.get_closest_dealer_with_vehicle(self.LOC_2[0],
            self.LOC_2[1], model=None, fuel=None, transmission=None)
        self.assertEqual(expected, obtained, 'Wrong closest dealer '
                                                  'returned.')

    def test_get_closest_dealer_model_only(self):
        EXPECTED_JSON_FILE_PATH  = './tests/resources/expected_closest_dealer_porto.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            dealer_dict = json.load(f)
        expected = dealer_dict['dealer']
        obtained = td.get_closest_dealer_with_vehicle(latitude=self.LOC_2[0],
            longitude=self.LOC_2[1], model='E')
        self.assertEqual(expected, obtained, 'Wrong closest dealer '
                                                  'returned.')

        # same as above, but with kwargs
        obtained = td.get_closest_dealer_with_vehicle(self.LOC_2[0],
            self.LOC_2[1], model='E', fuel=None, transmission=None)
        self.assertEqual(expected, obtained, 'Wrong closest dealer '
                                                  'returned.')

    def test_get_closest_dealer_fuel_only(self):
        EXPECTED_JSON_FILE_PATH  = './tests/resources/expected_closest_dealer_porto.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            dealer_dict = json.load(f)
        expected = dealer_dict['dealer']
        obtained = td.get_closest_dealer_with_vehicle(latitude=self.LOC_2[0],
            longitude=self.LOC_2[1], fuel='gasoline')
        self.assertEqual(expected, obtained, 'Wrong closest dealer '
                                                  'returned.')

        # same as above, but with kwargs
        obtained = td.get_closest_dealer_with_vehicle(self.LOC_2[0],
            self.LOC_2[1], model=None, fuel='gasoline', transmission=None)
        self.assertEqual(expected, obtained, 'Wrong closest dealer '
                                                  'returned.')

    def test_get_closest_dealer_transmission_only(self):
        EXPECTED_JSON_FILE_PATH  = './tests/resources/expected_closest_dealer_porto.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            dealer_dict = json.load(f)
        expected = dealer_dict['dealer']
        obtained = td.get_closest_dealer_with_vehicle(latitude=self.LOC_2[0],
            longitude=self.LOC_2[1], transmission='manual')
        self.assertEqual(expected, obtained, 'Wrong closest dealer '
                                                  'returned.')

        # same as above, but with kwargs
        obtained = td.get_closest_dealer_with_vehicle(self.LOC_2[0],
            self.LOC_2[1], model=None, fuel=None, transmission='manual')
        self.assertEqual(expected, obtained, 'Wrong closest dealer '
                                                  'returned.')

    def test_get_closest_dealer_model_and_fuel_only(self):
        EXPECTED_JSON_FILE_PATH  = './tests/resources/expected_closest_dealer_porto.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            dealer_dict = json.load(f)
        expected = dealer_dict['dealer']
        obtained = td.get_closest_dealer_with_vehicle(latitude=self.LOC_2[0],
            longitude=self.LOC_2[1], model='E', fuel='gasoline')
        self.assertEqual(expected, obtained, 'Wrong closest dealer '
                                                  'returned.')

        # same as above, but with kwargs
        obtained = td.get_closest_dealer_with_vehicle(self.LOC_2[0],
            self.LOC_2[1], model='E', fuel='gasoline', transmission=None)
        self.assertEqual(expected, obtained, 'Wrong closest dealer '
                                                  'returned.')

    def test_get_closest_dealer_model_and_transmission_only(self):
        self.maxDiff = None
        EXPECTED_JSON_FILE_PATH  = './tests/resources/expected_closest_dealer_porto.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            dealer_dict = json.load(f)
        expected = dealer_dict['dealer']
        obtained = td.get_closest_dealer_with_vehicle(latitude=self.LOC_2[0],
            longitude=self.LOC_2[1], model='E', transmission='auto')
        self.assertEqual(expected, obtained, 'Wrong closest dealer '
                                                  'returned.')

        # same as above, but with kwargs
        obtained = td.get_closest_dealer_with_vehicle(self.LOC_2[0],
            self.LOC_2[1], model='E', fuel=None, transmission='auto')
        self.assertEqual(expected, obtained, 'Wrong closest dealer '
                                                  'returned.')

    def test_get_closest_dealer_fuel_and_transmission_only(self):
        EXPECTED_JSON_FILE_PATH  = './tests/resources/expected_closest_dealer_porto.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            dealer_dict = json.load(f)
        expected = dealer_dict['dealer']
        obtained = td.get_closest_dealer_with_vehicle(latitude=self.LOC_2[0],
            longitude=self.LOC_2[1], fuel='ELECTRIC', transmission='auto')
        self.assertEqual(expected, obtained, 'Wrong closest dealer '
                                                  'returned.')

        # same as above, but with kwargs
        obtained = td.get_closest_dealer_with_vehicle(self.LOC_2[0],
            self.LOC_2[1], model=None, fuel=None, transmission='auto')
        self.assertEqual(expected, obtained, 'Wrong closest dealer '
                                                  'returned.')

    def test_get_closest_dealers_no_results(self):
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        expected = []
        obtained = td.get_closest_dealers_with_vehicle(latitude=self.LOC_1[0],
            longitude=self.LOC_1[1], model='E', fuel='air', transmission='manual')
        self.assertCountEqual(expected, obtained, 'Non-emtpy dealer list '
                                                  'returned.')

    def test_get_closest_dealers_one_match(self):
        EXPECTED_JSON_FILE_PATH  = './tests/resources/dataset_full_modified_albufeira.json'
        td = TestDrive(dataset='./tests/resources/dataset_full_modified_albufeira.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            dealers_list = json.load(f)
        expected = [dealers_list['dealers'][0]]
        obtained = td.get_closest_dealers_with_vehicle(latitude=self.LOC_2[0],
            longitude=self.LOC_2[1], model='A', fuel='B', transmission='C')
        self.assertEqual(expected, obtained, 'Wrong closest dealer '
                                                  'returned.')

    def test_get_closest_dealers_two_matches_close(self):
        # REGEX: "model": "E",\n\t+"fuel": "ELECTRIC",\n\t+"transmission": "AUTO"
        EXPECTED_JSON_FILE_PATH  = './tests/resources/dataset_full_modified_porto_albufeira.json'
        td = TestDrive(dataset='./tests/resources/dataset_full_modified_porto_albufeira.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            dealers_list = json.load(f)
        expected = [dealers_list['dealers'][0], dealers_list['dealers'][2]]
        obtained = td.get_closest_dealers_with_vehicle(self.LOC_1[0],
            self.LOC_1[1], 'A', 'B', 'C')
        self.assertEqual(expected, obtained, 'Wrong closest dealer '
                                             'returned.')

    def test_get_closest_dealers_two_matches_far_away(self):
        # REGEX: "model": "E",\n\t+"fuel": "ELECTRIC",\n\t+"transmission": "AUTO"
        EXPECTED_JSON_FILE_PATH  = './tests/resources/dataset_full_modified_porto_albufeira.json'
        td = TestDrive(dataset='./tests/resources/dataset_full_modified_porto_albufeira.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            dealers_list = json.load(f)
        expected = [dealers_list['dealers'][2], dealers_list['dealers'][0]]
        obtained = td.get_closest_dealers_with_vehicle(self.LOC_2[0],
            self.LOC_2[1], 'A', 'B', 'C')
        self.assertEqual(expected, obtained, 'Wrong closest dealer '
                                             'returned.')
