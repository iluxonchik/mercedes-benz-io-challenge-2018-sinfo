class TestDriveError(Exception):
    """Basic exception for all errors raised by the TestDrive app."""
    pass

class InvalidDataSetError(TestDriveError):
    """The provided JSON data set is invalid."""
    pass

class VehicleNotFoundError(TestDriveError):
    """Vehicle witht the provided id was not found"""
    pass
