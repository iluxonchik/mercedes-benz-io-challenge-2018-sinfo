"""Utility function tests."""
import unittest
from mbio.utils import nfdk_normalize_ignore_case, is_str_equal_ignore_case

class StringComparisonTestCase(unittest.TestCase):
    """Tests for string comparison utilities"""

    def test_nfdk_normalization(self):
        str1 = 'å'
        str2 = 'å'
        self.assertNotEqual(str1, str2)

        str1 = nfdk_normalize_ignore_case(str1)
        str2 = nfdk_normalize_ignore_case(str2)

        self.assertEqual(str1, str2)

    def test_is_equal_ignore_case(self):
        str1 = 'å'
        str2 = 'å'

        self.assertFalse(str1.lower() == str2.lower())

        self.assertTrue(is_str_equal_ignore_case(str1, str2))
