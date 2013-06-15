class Error(Exception):
    """
    Base class for exceptions.
    """
    pass

class EmailerError(Error):
    """
    Exception raised for errors in the email module.
    """

    def __init__(self, msg):
        self.msg = msg
