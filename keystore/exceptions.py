class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class KeystoreInvalidError(Error):

    def __init__(self, message):
        self.message = message

class KeystoreExpiredError(Error):
    def __init__(self, message):
        self.message = message
