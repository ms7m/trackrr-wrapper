# Trackrr.py (song.py)
# Song object for Trackrr

# Imports
import typing
from dateutil.parser import parse

if typing.TYPE_CHECKING:
    from datetime import datetime

class Song:
    """ Represents a song object from the Trackrr API """
    def __init__(self, data, service="Default"):
        self.data = data
        self.service = service

    def __repr__(self) -> str:
        return f"<TrackrrSong {self.service.capitalize()} object>"

    @property
    def track_name(self) -> str:
        """ Returns the name of the requested song """
        return self.data["track_name"] 
    
    @property
    def track_artist(self) -> typing.List[str]:
        """ Returns the name of the requested song """
        return self.data["track_artist"]

    @property
    def track_url(self) -> str:
        """ Returns a URL for the requested song """
        return self.data["track_url"]

    @property
    def track_release_date(self) -> "datetime":
        """ Returns the release date of the requested song """
        return parse(self.data["track_release_date"])

    @property
    def track_cover_url(self) -> typing.List[str]:
        """ Returns a URL for the cover of the requested song """
        return self.data["track_cover_art"]

    @property
    def track_popularity(self) -> typing.Union[str, None]:
        """ Shows how popular a track is """
        return self.data["track_popularity"]

    @property
    def track_service_unique_id(self) -> str:
        """ Returns a unique ID of the requested song """
        return self.data["track_service_unique_id"]

    @property
    def track_isrc(self) -> str:
        return self.data["track_isrc"]

    @property
    def to_dict(self) -> dict:
        """ Returns the song object with info about the requested song """
        return self.data
