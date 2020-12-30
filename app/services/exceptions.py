class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class DuplicateError(Error):
    def __init__(self,message):
        self.message = message

class UserNotExistError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class AuthenticationError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class ExistError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        
class FoundMultipleError(Error):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super(MultipleException, self).__init__(message)

        # Now for your custom code...
        self.errors = errors

