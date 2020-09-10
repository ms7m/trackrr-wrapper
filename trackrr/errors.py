# Trackrr.py (errors.py)
# Exceptions for the Trackrr API

import json
import typing

if typing.TYPE_CHECKING:
    import requests

class InvalidAPIKey(Exception):
    """ Exception raised when an invalid API key is given """
    pass

class InvalidParams(Exception):
    """ Exception raised when invalid param(s) are passed in a request """
    pass

class ParsingError(Exception):
    """ Exception raised when request can't be parsed """
    pass

class APIError(Exception):
    """ Exception raised when there was a problem with communicating with the API """
    pass

class APIReturnedError(Exception):
    """ Exception that is raised when the API returns an error object """

    # Standard Error Object
    # {
    #     "error_code": 400,
    #     "error_message": "Invalid service filter passed."
    # }   


    def __init__(self, error, request: "requests.Response"):
        self.error_code = request.status_code
        if request.text:
            if request.headers.get("Content-Type") == "application/json":
                parse_request_message = request.json()
                self.message = parse_request_message['error_message']
                self.error_code = parse_request_message['error_code']
            else:
                self.message = error
        else:
            self.message = error
        super().__init__(self.message)
    
    def __str__(self):
        return f"API Returned an Error: [{self._error_code}] - {self.message}"
        