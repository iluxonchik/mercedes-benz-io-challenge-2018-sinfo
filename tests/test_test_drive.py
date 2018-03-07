"""TestDrive class initialization tests."""
import unittest
from mbio.testdrive import TestDrive
from mbio.testdrive.excepitions import InvalidDataSetException

class TestDriveTestCase(unittest.TestCase):
    """TestDrive class initialization tests."""

    def setUp(self):
        """Set up test code for TestDriveTestCase."""
        super(TestDrive, self).setUp(self)
        self.FAULTY_DATASET_PATH = './resources/dataset_faulty.json'

    def test_testdrive_init_FAIL(self):
        """TestDrive initialized with an valid data set."""
        with self.assertRaises(InvalidDataSetException):
            td = TestDrive(self.FAULTY_DATASET_PATH)
