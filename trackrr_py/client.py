
import typing
from dateutil.parser import parse
import requests
from trackrr_py.objects.song import TrackrrSong

class Trackrr(object):
    def __init__(self, api_key: str=False, version: str="v1"):
        """Initialize Trackrr Object.

        Args:
            api_key (str): The Trackrr API Requires a valid api key.
            version (str, optional): The API Version. Defaults to "v1".

        Raises:
            Exception: Returns exceptions from API.
        """

        if api_key is False:
            raise Exception("An API key is required.")
        
        self._client = requests.Session()
        self._client.headers = {
            "X-Trackrr-APIKey": api_key
        }
        self._base_api = f'https://api.trackrr.cc/{version}'

    def send_request(self, request_url: str, request_params: dict) -> dict:
        """Sends the request to the Trackrr API.
        This function will handle errors from the API.

        You do not need to call this function directly.

        Args:
            request_url (str): the request URL
            request_params (dict): the request param

        Raises:
            Exception: --

        Returns:
            dict: --
        """
        try:
            send_request = self._client.get(request_url, params=request_params)
            parse_request = send_request.json()
        except Exception:
            raise Exception("Library error with parsing request from API.")

        if send_request.status_code == 200:
            return parse_request

        if send_request.status_code == 422:
            # this is a validation error from the API. probably means you're missing a param or sent an improper param.
            #{
            #    "detail": [
            #        {
            #            "loc": [
            #                "query",
            #                "query"
            #            ],
            #            "msg": "field required",
            #            "type": "value_error.missing"
            #        }
            #    ]
            #}         
            missing_params = []
            for missing_param in parse_request['detail']:
                missing_params.append(f"{missing_param['msg']} - {missing_param['loc'][0]}")
            raise Exception(f"API Error: Improper param sent to API. {missing_params}")
                   
            
        # Standard Error Object
        # {
        #     "error_code": 400,
        #     "error_message": "Invalid service filter passed."
        # }            
        raise Exception(f"API Error ({parse_request['error_code']}): {parse_request['error_message']}")

    def search_song_by_query(self, search_query: str, filter_services: str=False) -> typing.List[TrackrrSong]:
        """ Calls the /search/song endpoint to the Trackrr API.
        This endpoint will take a string and do a search across streaming platforms..

        Args:
            search_query (str): the query to search for.
            filter_services (str, optional): Filter services to return. Syntax: 'service1,service2' . Defaults to False.

        Returns:
            typing.List[TrackrrSong]: Returns a list of TrackrrSong objects of each service.
        """
        search_song_request_url = self._base_api + "/search/song"
        search_song_params = {
            "query": search_query
        }
        if filter_services != False:
            search_song_params['filterServices'] = filter_services

        send_request = self.send_request(
            request_url=search_song_request_url,
            request_params=search_song_params
        )
        if len(send_request['meta']['servicesReturned']) == 0:
            return []
        

        items = []

        for item in send_request['meta']['servicesReturned']:
            items.append(
                TrackrrSong(
                    data=send_request['services'][item],
                    service_name=item
                )
            )
        return items