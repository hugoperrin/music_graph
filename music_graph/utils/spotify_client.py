from typing import Dict, Optional, Tuple, Union

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

from music_graph.abstract.client import AbstractStreamingAPIClient
from music_graph.datamodel.album import AlbumData
from music_graph.datamodel.artist import ArtistData
from music_graph.datamodel.playlist import PlaylistData
from music_graph.datamodel.track import TrackData
from music_graph.datamodel.user_info import UserInfo


class SpotifyStreamingAPIClient(AbstractStreamingAPIClient):
    def __init__(self, spotify_client: spotipy.Spotify) -> None:
        self.spotify_client = spotify_client

    def get_track(self, track_id: str) -> TrackData:
        """Get track data in the TrackData format from spotify client

        Args:
            track_id (str): the id of a track

        Returns:
            TrackData: The track data

        Examples:
            >>> client = SpotifyStreamingAPIClient.from_env()
            >>> _id: str = "6rqhFgbbKwnb9MLmUQDhG6"
            >>> track_data: TrackData = client.get_track(_id)
            >>> isinstance(track_data, TrackData)
            True
            >>> track_data.id
            '6rqhFgbbKwnb9MLmUQDhG6'
        """
        track_data: Dict = self.spotify_client.track(track_id=track_id)
        audio_analysis: Dict = self.spotify_client.audio_analysis(track_id=track_id)
        return TrackData.from_spotify_dict(
            track_id=track_id, track_data=track_data, audio_analysis=audio_analysis,
        )

    def get_album(self, album_id: str) -> AlbumData:
        """Get album data in the AlbumData format from spotify client

        Args:
            album_id (str): the id of an album

        Returns:
            AlbumData: The album data

        Examples:
            >>> client = SpotifyStreamingAPIClient.from_env()
            >>> _id: str = "3a0UOgDWw2pTajw85QPMiz"
            >>> album_data: AlbumData = client.get_album(_id)
            >>> isinstance(album_data, AlbumData)
            True
            >>> album_data.id
            '3a0UOgDWw2pTajw85QPMiz'
        """
        album_data: Dict = self.spotify_client.album(album_id=album_id)
        return AlbumData.from_spotify_dict(album_id, album_data)

    def get_artist(self, artist_id: str) -> ArtistData:
        """Get artist data in the AlbumData format from spotify client

        Args:
            artist_id (str): the id of an artist

        Returns:
            ArtistData: The artist data

        Examples:
            >>> client = SpotifyStreamingAPIClient.from_env()
            >>> _id: str = "36QJpDe2go2KgaRleHCDTp"
            >>> artist_data: ArtistData = client.get_artist(_id)
            >>> isinstance(artist_data, ArtistData)
            True
            >>> artist_data.id
            '36QJpDe2go2KgaRleHCDTp'
        """
        artist_data: Dict = self.spotify_client.artist(artist_id=artist_id)
        album_data: Dict = self.spotify_client.artist_albums(artist_id=artist_id)
        top_tracks: Dict = self.spotify_client.artist_top_tracks(artist_id=artist_id)
        similar_artists: Dict = self.spotify_client.artist_related_artists(
            artist_id=artist_id
        )
        return ArtistData.from_spotify_dict(
            artist_id=artist_id,
            artist_data=artist_data,
            top_tracks=top_tracks,
            similar_artists=similar_artists,
            albums=album_data,
        )

    def get_playlist(self, playlist_id: str) -> PlaylistData:
        """Get playlist data in the PlaylistData format from spotify client

        Args:
            playlist_id (str): the id of a playlist

        Returns:
            PlaylistData: The playlist data

        Examples:
            >>> client = SpotifyStreamingAPIClient.from_env()
            >>> _id: str = "37i9dQZEVXcSOuWCN1KpTh"
            >>> playlist_data: PlaylistData = client.get_playlist(_id)
            >>> isinstance(playlist_data, PlaylistData)
            True
            >>> playlist_data.id
            '37i9dQZEVXcSOuWCN1KpTh'
        """
        playlist_data: Dict = self.spotify_client.playlist(playlist_id=playlist_id)
        return PlaylistData.from_spotify_dict(playlist_data)

    def get_user_info(self, user_id: str, is_current_user: bool = False) -> UserInfo:
        """Get playlist data in the PlaylistData format from spotify client

        Args:
            user_id (str): the id of an user

        Returns:
            UserInfo: The user data

        Examples:
            >>> client = SpotifyStreamingAPIClient.from_env()
            >>> _id: str = "21b3bhuunakbsyzphqnu4rpty"
            >>> user_info: UserInfo = client.get_user_info(_id)
            >>> isinstance(user_info, UserInfo)
            True
            >>> user_info.id
            '21b3bhuunakbsyzphqnu4rpty'
            >>> client = SpotifyStreamingAPIClient.from_env(
            ...     scope=("user-top-read", "playlist-read-private", "user-library-read", "user-follow-read")
            ... )
            >>> user_info: UserInfo = client.get_user_info(_id, is_current_user=True)
            >>> isinstance(user_info, UserInfo)
            True
            >>> user_info.id
            '21b3bhuunakbsyzphqnu4rpty'
        """
        user_data: Dict = self.spotify_client.user(user=user_id)
        if is_current_user:
            artists_data: Optional[
                Dict
            ] = self.spotify_client.current_user_followed_artists()
            playlist_data: Optional[Dict] = self.spotify_client.current_user_playlists()
            top_tracks: Optional[Dict] = self.spotify_client.current_user_top_tracks()
            saved_tracks: Optional[
                Dict
            ] = self.spotify_client.current_user_saved_tracks()
            saved_albums: Optional[
                Dict
            ] = self.spotify_client.current_user_saved_albums()
            return UserInfo.from_spotify_dict(
                user_data,
                artists_data=artists_data,
                playlist_data=playlist_data,
                top_tracks=top_tracks,
                saved_tracks=saved_tracks,
                saved_albums=saved_albums,
            )
        else:
            return UserInfo.from_spotify_dict(user_data)

    @classmethod
    def from_env(cls, scope: Optional[Union[str, Tuple]] = None):
        if scope is not None:
            spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        else:
            spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
        spotify.current_user()
        return cls(spotify)
