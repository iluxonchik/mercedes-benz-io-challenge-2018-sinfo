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
        self.assertCountEqual(expected, obtained, 'Wrong closest dealer '
                                                  'returned.')


    def test_get_closest_dealer_one_match(self):
        EXPECTED_JSON_FILE_PATH  = './tests/resources/expected_closest_dealer_two_matches.json'
        td = TestDrive(dataset='./tests/resources/dataset_full.json')
        with open(EXPECTED_JSON_FILE_PATH, 'r') as f:
            dealers_list = json.load(f)
        expected = dealers_list['dealers'][0]
        obtained = td.get_closest_dealer_with_vehicle(latitude=self.LOC_2[0],
            longitude=self.LOC_2[1], model='AMG', fuel='gasoline', transmission='manual')
        self.assertCountEqual(expected, obtained, 'Wrong closest dealer '
                                                  'returned.')
