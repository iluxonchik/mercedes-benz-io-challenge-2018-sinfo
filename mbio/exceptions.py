class TestDriveError(Exception):
    """Basic exception for all errors raised by the TestDrive app."""
    
    def __init__(self, msg=None):
        if msg is None:
            msg = 'An error in the TestDrive app occured.'
        super(TestDriveError, self).__init__(msg)

class InvalidDataSetError(TestDriveError):
    """The provided JSON data set is invalid."""

    def __init__(self, msg=None):
        if msg is None:
            msg = 'Error loading the dataset.'
        super(InvalidDataSetError, self).__init__(msg)
