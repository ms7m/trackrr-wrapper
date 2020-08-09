
# Song Object from Trackrr

#{
#    "track_name": "The Adventures of Moon Man & Slim Shady (with Eminem)",
#    "track_artist": [
#        "Kid Cudi",
#        "Eminem"
#    ],
#    "track_url": "https://open.spotify.com/track/38iBrrbbXyWaSPkmuDNgjZ",
#    "track_cover_art": [
#        "https://i.scdn.co/image/ab67616d0000b27355dfd42001dbc79e5552c82c",
#        "https://i.scdn.co/image/ab67616d00001e0255dfd42001dbc79e5552c82c",
#        "https://i.scdn.co/image/ab67616d0000485155dfd42001dbc79e5552c82c"
#    ],
#    "track_release_date": "2020-07-10T00:00:00+00:00",
#    "track_album": "The Adventures of Moon Man & Slim Shady (with Eminem)",
#    "track_popularity": 81,
#    "track_service_unique_id": "38iBrrbbXyWaSPkmuDNgjZ",
#    "track_isrc": "USUM72013649"
#}


import dateutil.parser
import typing

if typing.TYPE_CHECKING:
    from datetime import datetime


class TrackrrSong(object):
    def __init__(self, data, service_name="Default"):
        self._data = data
        self._service_name = service_name


    def __repr__(self) -> str:
        return f"<TrackrrSong {self._service_name.capitalize()} object>"
    

    @property
    def track_name(self) -> str:
        return self._data['track_name']

    @property
    def track_artist(self) -> typing.List[str]:
        return self._data['track_artist']
    
    @property
    def track_url(self) -> str:
        return self._data['track_url']
    
    @property
    def track_cover_art(self) -> typing.List[str]:
        return self._data['track_cover_art']

    @property
    def track_release_date(self) -> "datetime":
        return dateutil.parser.parse(self._data['track_release_date'])

    @property
    def track_popularity(self) -> typing.Union[str, None]:
        return self._data['track_popularity']
    
    @property
    def track_service_unique_id(self) -> str:
        return self._data['track_service_unique_id']
    
    @property
    def track_isrc(self) -> str:
        return self._data['track_isrc']

    @property
    def to_dict(self):
        return self._data