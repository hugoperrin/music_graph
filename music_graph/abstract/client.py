from abc import abstractmethod
from typing import List, Union

from music_graph.datamodel.album import AlbumData
from music_graph.datamodel.artist import ArtistData
from music_graph.datamodel.playlist import PlaylistData
from music_graph.datamodel.track import TrackData
from music_graph.datamodel.user_info import UserInfo


class AbstractStreamingAPIClient:
    @abstractmethod
    def get_track(self, track_id: str) -> TrackData:
        ...

    @abstractmethod
    def get_album(self, album_id: str) -> AlbumData:
        ...

    @abstractmethod
    def get_artist(self, artist_id: str) -> ArtistData:
        ...

    @abstractmethod
    def get_playlist(self, playlist_id: str) -> PlaylistData:
        ...

    @abstractmethod
    def get_user_info(self, user_id: str) -> UserInfo:
        ...

    @abstractmethod
    def get_artist_neighbors(self, artist_id: str) -> List[str]:
        ...

    @abstractmethod
    def get_playlist_neighbors(self, playlist_id: str) -> List[str]:
        ...

    @abstractmethod
    def get_track_neighbors(self, track_id: str) -> List[str]:
        ...

    @abstractmethod
    def get_album_neighbors(self, track_id: str) -> List[str]:
        ...

    def search(
        self, str_value: str, res_type: str = "track"
    ) -> List[Union[AlbumData, ArtistData, TrackData]]:
        raise NotImplementedError("Search not available with this client")
