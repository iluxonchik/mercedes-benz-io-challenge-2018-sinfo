"""TestDrive class initialization tests."""
import unittest
from mbio.testdrive import TestDrive
from mbio.exceptions import InvalidDataSetError

class TestDriveTestCase(unittest.TestCase):
    """TestDrive class initialization tests."""

    def setUp(self, *args, **kwargs):
        """Set up test code for TestDriveTestCase."""
        super(TestDriveTestCase, self).setUp(*args, **kwargs)
        self.FAULTY_DATASET_PATH = './tests/resources/dataset_faulty.json'

    def test_testdrive_init_FAIL(self):
        """TestDrive initialized with an valid data set."""
        with self.assertRaises(InvalidDataSetError):
            td = TestDrive(self.FAULTY_DATASET_PATH)
