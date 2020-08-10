# Trackrr.py (client.py)
# Trackrr's API Client

# Imports
import aiohttp
from typing import List
from trackrr.ext.song import Song
from trackrr.errors import ParsingError
from trackrr.errors import InvalidAPIKey
from trackrr.errors import InvalidParams

class Trackrr:
    """ Represents a client used for requests 
    
    Args:
        api_key (str): Required key to interact with the Trackrr API
        version (str, optional): The API version. Default value is "v1"

    Raises:
        InvalidAPIKey (Exception): Raised when an API key is invalid/missing  
    """
    def __init__(self, api_key: str=None, version: str="v1"):
        if api_key is None:
            raise InvalidAPIKey("An API was not given/is required")

        self.session = None
        self.headers = { "X-Trackrr-APIKey": api_key }
        self.base_url = f"https://api.trackrr.cc/{version}"

    async def create_session(self):
        """ Creates an aiohttp session """
        # Creating a session under an async function is recommended
        self.session = aiohttp.ClientSession()

    async def send_request(self, url: str, params: dict) -> dict:
        """ Sends a request to the Trackrr API 
        This function will handle errors for the API

        You do not need to call this function directly

        Args:
            url (str): The request URL
            params (dict): Parameters given to the request

        Raises:
            ParsingError (Exception): Raised when a request can't be parsed

        Returns:
            dict: The contents of the request
        """
        if self.session is None:
            # Create a session if one doesn't exist
            await self.create_session()

        async with self.session.get(url, params=params, headers=self.headers) as resp:
            # Make sure that the response of the request
            # returns code 200. Something wrong happened if it doesn't
            if not (300 > resp.status >= 200):
                # Raise an error if the status code isn't 200
                raise ParsingError(f"Library error parsing request from API: {str(resp.status)}")

            try:
                # We attempt to return the contents
                # of the request in JSON format
                response = await resp.json()
                if resp.status >= 400:
                    # This is a validation error from the API
                    # Likely has to do with missing/improper params
                    missing_params = list()
                    for param in response["detail"]:
                        missing_params.append(f"{param['msg']} - {param['loc'][0]}")
                    raise InvalidParams(f"Impropert params in given request: {missing_params}")
            # If that fails, simply return the contents of the request
            # without ant kind of formatting (aka just read it)
            except aiohttp.ClientResponseError:
                raise ParsingError("Could not return contents from the request")

        # Return the respose from the request, if any
        return response

    async def search_song(self, search: str, filter_services: str=False):
        """ Calls the search/song endpoint of the Trackrr API 
        This endpoint will take a query and do a search across streaming platforms

        Args:
            query (str): Search query used to search streaming platforms
            filter_services (str, optional): Filter services to return. Syntax: 'service1,service2' . Defaults to False.

        Returns:
            typing.List[Song]: Returns a list of Song objects for each obtained service
        """
        requestURL = f"{self.base_url}/search/song"
        songParams = { "query": search }
        # Check if services are filtered
        if filter_services != False:
            songParams["filterServices"] = filter_services

        # Get the contents of the request
        results = await self.send_request(requestURL, songParams)
        # Check to see if results were returned
        if len(results["meta"]["servicesReturned"]) == 0:
            return []

        # Send the contents of request, if any
        items = []
        for item in results["meta"]["servicesReturned"]:
            items.append(Song(results["services"][item], item))
        # Return a list of fetched results
        return items
    
    async def close(self):
        """ Closes the aiohttp session """
        # This essensially stops self.session from running
        if self.session is not None:
            # Close the session, or aiohttp complains
            await self.session.close()
            # Set our session back to its default value
            self.session = None
