class TestDriveError(Exception):
    """Basic exception for all errors raised by the TestDrive app."""
    pass

class InvalidDataSetError(TestDriveError):
    """The provided JSON data set is invalid."""
    pass
