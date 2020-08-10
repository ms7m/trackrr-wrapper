# Trackrr.py (errors.py)
# Exceptions for the Trackrr API

class InvalidAPIKey(Exception):
    """ Exception raised when an invalid API key is given """
    pass

class InvalidParams(Exception):
    """ Exception raised when invalid param(s) are passed in a request """
    pass

class ParsingError(Exception):
    """ Exception raised when request can't be parsed """
    pass
