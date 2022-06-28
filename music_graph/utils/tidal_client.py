import os
from typing import Dict, List, Optional

import requests
import tidalapi as tidal
from loguru import logger

from music_graph.abstract.client import AbstractStreamingAPIClient
from music_graph.datamodel.album import AlbumData
from music_graph.datamodel.artist import ArtistData
from music_graph.datamodel.playlist import PlaylistData
from music_graph.datamodel.track import TrackData
from music_graph.datamodel.user_info import UserInfo
from music_graph.utils.converter.tidal_converter import TidalAPIConverter


class TidalStreamingAPIClient(AbstractStreamingAPIClient):
    def __init__(self, tidal_session: tidal.Session) -> None:
        self.tidal_session = tidal_session
        self.converter = TidalAPIConverter()

    def get_track(self, track_id: str) -> TrackData:
        """Get track data in the TrackData format from tidal client

        Args:
            track_id (str): the id of a track

        Returns:
            TrackData: The track data

        Examples:
            >>> client = TidalStreamingAPIClient.from_env()
            >>> _id: str = "113558924"
            >>> data: TrackData = client.get_track(_id)
            >>> isinstance(data, TrackData)
            True
            >>> data.id
            '113558924'
        """
        track_data: tidal.models.Track = self.tidal_session.get_track(track_id=track_id)
        similar_tracks: List[tidal.models.Track] = self.tidal_session.get_track_radio(
            track_id=track_id
        )
        return self.converter.track_converter(
            track_raw=track_data, similar_tracks=similar_tracks
        )

    def get_album(self, album_id: str) -> AlbumData:
        """Get album data in the AlbumData format from tidal client

        Args:
            album_id (str): the id of an album

        Returns:
            AlbumData: The album data

        Examples:
            >>> client = TidalStreamingAPIClient.from_env()
            >>> _id: str = "87642140"
            >>> data: AlbumData = client.get_album(_id)
            >>> isinstance(data, AlbumData)
            True
            >>> data.id
            '87642140'
        """
        album_data: tidal.models.Album = self.tidal_session.get_album(album_id=album_id)
        album_tracks: List[tidal.models.Track] = self.tidal_session.get_album_tracks(
            album_id=album_id
        )
        return self.converter.album_converter(
            album_raw=album_data, album_tracks=album_tracks
        )

    def get_artist(self, artist_id: str) -> ArtistData:
        """Get artist data in the ArtistData format from tidal client

        Args:
            artist_id (str): the id of an artist

        Returns:
            ArtistData: The artist data

        Examples:
            >>> client = TidalStreamingAPIClient.from_env()
            >>> _id: str = "15099025"
            >>> data: ArtistData = client.get_artist(_id)
            {"status":404,"subStatus":2001,"userMessage":"Similar artists for artist [15099025] not found"}
            >>> isinstance(data, ArtistData)
            True
            >>> data.id
            '15099025'
        """
        artist_data: tidal.models.Artist = self.tidal_session.get_artist(
            artist_id=artist_id
        )
        albums: List[tidal.models.Album] = self.tidal_session.get_artist_albums(
            artist_id=artist_id
        )
        albums += self.tidal_session.get_artist_albums_ep_singles(artist_id=artist_id)
        albums += self.tidal_session.get_artist_albums_other(artist_id=artist_id)
        try:
            similar_artists: Optional[
                List[tidal.models.Artist]
            ] = self.tidal_session.get_artist_similar(artist_id=artist_id)
        except requests.exceptions.HTTPError:
            similar_artists = None
        top_tracks: List[tidal.models.Track] = self.tidal_session.get_artist_top_tracks(
            artist_id=artist_id
        )
        return self.converter.artist_converter(
            artist_raw=artist_data,
            albums=albums,
            similar_artists=similar_artists,
            top_tracks=top_tracks,
        )

    def get_playlist(self, playlist_id: str) -> PlaylistData:
        """Get playlist data in the PlaylistData format from tidal client

        Args:
            playlist_id (str): the id of a playlist

        Returns:
            PlaylistData: The playlist data

        Examples:
            >>> client = TidalStreamingAPIClient.from_env()
            >>> _id: str = "eb1ffe34-77da-445e-814a-089957eaff4f"
            >>> data: PlaylistData = client.get_playlist(_id)
            >>> isinstance(data, PlaylistData)
            True
            >>> data.id
            'eb1ffe34-77da-445e-814a-089957eaff4f'
        """
        playlist_data: tidal.models.Playlist = self.tidal_session.get_playlist(
            playlist_id=playlist_id
        )
        playlist_tracks: List[
            tidal.models.Track
        ] = self.tidal_session.get_playlist_tracks(playlist_id=playlist_id)
        return self.converter.playlist_converter(
            playlist_raw=playlist_data, playlist_tracks=playlist_tracks,
        )

    def get_user_info(self, user_id: Optional[str] = None) -> UserInfo:
        """Get user data in the UserInfo format from tidal client

        Args:
            user_id (str): the id of a playlist

        Returns:
            UserInfo: The user data

        Examples:
            >>> client = TidalStreamingAPIClient.from_env()
            >>> _id: Optional[str] = None
            >>> data: UserInfo = client.get_user_info(_id)
            >>> isinstance(data, UserInfo)
            True
            >>> data.id == os.getenv("TIDAL_USER_ID")  # This is put as a secret as it's a secret and personnal information, can be modified in .env file
            True
        """
        if user_id is None:
            logger.warning(
                "When using Tidal, you can only get the user from the current session"
            )
            user_data: tidal.User = self.tidal_session.user
        else:
            logger.warning(
                "When using Tidal, you can only get the user from the current session, this will crash until it's fixed in tidalapi lib"
            )
            user_data = self.tidal_session.get_user(user_id=user_id)
        return self.converter.user_converter(user_data=user_data)

    def get_artist_neighbors(self, artist_id: str) -> List[str]:
        """Get similar artists

        Args:
            artist_id (str): The artist id

        Returns:
            List[str]: The list of ids

        Examples:
            >>> client = TidalStreamingAPIClient.from_env()
            >>> _id: str = "8215566"
            >>> ids: List[str] = client.get_artist_neighbors(_id)
            >>> isinstance(ids, list)
            True
            >>> ids
            ['18987650', '3575134', '4016378', '4070117', '5585406', '56351', '5664250', '6279772', '6331905', '6352481', '6381216', '7481141', '7525938', '7559542', '7650315', '7773162']
            >>> _id: str = "15099025"
            >>> ids: List[str] = client.get_artist_neighbors(_id)
            {"status":404,"subStatus":2001,"userMessage":"Similar artists for artist [15099025] not found"}
            >>> isinstance(ids, list)
            True
            >>> ids
            []
        """
        try:
            similar_artists: List = self.tidal_session.get_artist_similar(
                artist_id=artist_id,
            )
            return [str(a.id) for a in similar_artists]
        except requests.exceptions.HTTPError:
            # We can have an error 404 here whenever there are no similar artists provided by the API
            return []

    def get_album_neighbors(self, album_id: str) -> List[str]:
        """Get similar albums => like spotify cannot find a way through Tidal API to get album neighbors

        Args:
            album_id (str): The album id

        Returns:
            List[str]: The list of ids

        Examples:
            >>> client = TidalStreamingAPIClient.from_env()
            >>> _id: str = "209813264"
            >>> ids: List[str] = client.get_album_neighbors(_id)
            >>> isinstance(ids, list)
            True
            >>> ids
            [211911358, 215507618, 222716543, 198677413, 223182050, 226787144, 225753010, 204327968, 222419033, 214758264, 223177137, 216698233, 211078893, 201278522, 225274037, 212738710, 197439810, 226100090, 216868234]
        """
        similar_albums: List = self.tidal_session.get_album_similar(album_id=album_id,)
        return [alb.id for alb in similar_albums]

    @classmethod
    def from_env(cls):
        tidal_session = tidal.Session()
        first_authentication: bool = os.getenv("TIDAL_FIRST_AUTH", False)
        if first_authentication:
            # This should be run outside of tests the first time to get the tidal login page
            tidal_session.login_oauth_simple()
        else:
            TIDAL_SESSION_ID: str = os.getenv("TIDAL_SESSION_ID")
            TIDAL_TOKEN_TYPE: str = os.getenv("TIDAL_TOKEN_TYPE")
            TIDAL_ACCESS_TOKEN: str = os.getenv("TIDAL_ACCESS_TOKEN")
            TIDAL_REFRESH_TOKEN: str = os.getenv("TIDAL_REFRESH_TOKEN")
            tidal_session.load_oauth_session(
                session_id=TIDAL_SESSION_ID,
                token_type=TIDAL_TOKEN_TYPE,
                access_token=TIDAL_ACCESS_TOKEN,
                refresh_token=TIDAL_REFRESH_TOKEN,
            )
        return TidalStreamingAPIClient(tidal_session=tidal_session)
