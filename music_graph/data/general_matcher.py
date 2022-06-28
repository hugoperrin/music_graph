from enum import Enum
from typing import List

from music_graph.abstract.client import AbstractStreamingAPIClient
from music_graph.abstract.matcher import AbstractMatcher
from music_graph.datamodel.album import AlbumData
from music_graph.datamodel.artist import ArtistData
from music_graph.datamodel.track import TrackData


class ContentTypeEnum(Enum):
    artist = "artist"
    album = "album"
    track = "track"


class GeneralMatcher(AbstractMatcher):
    def __init__(
        self,
        target_api: AbstractStreamingAPIClient,
        source_api: AbstractStreamingAPIClient,
    ) -> None:
        super().__init__()
        self.target_api: AbstractStreamingAPIClient = target_api
        self.source_api: AbstractStreamingAPIClient = source_api

    def match(self, _id: str, content_type: ContentTypeEnum) -> str:
        if content_type == ContentTypeEnum.album:
            return self.match_album(album_id=_id)
        elif content_type == ContentTypeEnum.artist:
            return self.match_artist(artist_id=_id)
        elif content_type == ContentTypeEnum.track:
            return self.match_track(track_id=_id)
        else:
            raise ValueError()

    def match_album(self, album_id: str) -> str:
        source_album: AlbumData = self.source_api.get_album(album_id=album_id)
        search_res: List = self.target_api.search(source_album.name)
        return ""

    def match_artist(self, artist_id: str) -> str:
        source_artist: ArtistData = self.source_api.get_artist(artist_id=artist_id)

        return ""

    def match_track(self, track_id: str) -> str:
        source_track: TrackData = self.source_api.get_track(track_id=track_id)

        return ""
