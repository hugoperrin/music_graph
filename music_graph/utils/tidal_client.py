from music_graph.abstract.client import AbstractStreamingAPIClient
from music_graph.datamodel.album import AlbumData
from music_graph.datamodel.artist import ArtistData
from music_graph.datamodel.playlist import PlaylistData
from music_graph.datamodel.track import TrackData
from music_graph.datamodel.user_info import UserInfo


class TidalStreamingAPIClient(AbstractStreamingAPIClient):
    def get_track(self, track_id: str) -> TrackData:
        # TODO: do track fetching and abstraction to track data
        ...

    def get_album(self, album_id: str) -> AlbumData:
        # TODO: do track fetching and abstraction to album data
        ...

    def get_artist(self, artist_id: str) -> ArtistData:
        # TODO: do track fetching and abstraction to artist data
        ...

    def get_playlist(self, playlist_id: str) -> PlaylistData:
        # TODO: do track fetching and abstraction to playlist data
        ...

    def get_user_info(self, user_id: str) -> UserInfo:
        # TODO: do the fetching of an user information
        ...
