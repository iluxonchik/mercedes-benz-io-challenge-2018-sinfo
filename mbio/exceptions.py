class TestDriveError(Exception):
    """Basic exception for all errors raised by the TestDrive app."""
    pass

class InvalidDataSetError(TestDriveError):
    """The provided JSON data set is invalid."""
    pass

class BookingError(TestDriveError):
    """Base exception for all errors raised by the booking process."""
    pass

class VehicleNotFoundError(BookingError):
    """Vehicle witht the provided id was not found"""
    pass

class VehicleNotAvailableOnDateError(BookingError):
    pass

class VehicleAlreadyBookedError(BookingError):
    pass
