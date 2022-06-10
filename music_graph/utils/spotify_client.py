from typing import Dict, List, Optional, Tuple, Union

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

    def get_artist_neighbors(self, artist_id: str) -> List[str]:
        """Get similar artists

        Args:
            artist_id (str): The artist id

        Returns:
            List[str]: The list of ids

        Examples:
            >>> client = SpotifyStreamingAPIClient.from_env()
            >>> _id: str = "36QJpDe2go2KgaRleHCDTp"
            >>> ids: List[str] = client.get_artist_neighbors(_id)
            >>> isinstance(ids, list)
            True
            >>> ids
            ['568ZhdwyaiCyOGJRtNYhWf', '776Uo845nYHJpNaStv1Ds4', '22WZ7M8sxp5THdruNY3gXt', '74oJ4qxwOZvX6oSsu1DGnw', '4MVyzYMgTwdP7Z49wAZHx0', '67ea9eGLXYMsO2eYQRui3w', '0qEcf3SFlpRcb3lK3f2GZI', '2AM4ilv6UzW0uMRuqKtDgN', '00tVTdpEhQQw1bqdu8RCx2', '5M52tdBnJaKSvOpJGz8mfZ', '1OwarW4LEHnoep20ixRA0y', '1WRM9i067hd2ujxxi8FI3m', '5krkohEVJYw0qoB5VWwxaC', '6biWAmrHyiMkX49LkycGqQ', '2e53aHBQdCMKWqHDuyJsjC', '6QtGlUje9TIkLrgPZrESuk', '21ysNsPzHdqYN2fQ75ZswG', '22bE4uQ6baNwSHPVcDxLCe', '4wQ3PyMz3WwJGI5uEqHUVR', '2lxX1ivRYp26soIavdG9bX']
        """
        similar_artists: Dict = self.spotify_client.artist_related_artists(
            artist_id=artist_id
        )
        return [a["id"] for a in similar_artists["artists"]]

    def get_playlist_neighbors(self, playlist_id: str) -> List[str]:
        raise NotImplementedError(
            "Spotify does not allow getting similar playlists from playlists"
        )

    def get_album_neighbors(self, album_id: str) -> List[str]:
        """Get similar albums => Spotify does not support similar albums => returns empty list all the time

        Args:
            album_id (str): The album id

        Returns:
            List[str]: The list of ids

        Examples:
            >>> client = SpotifyStreamingAPIClient.from_env()
            >>> _id: str = "36QJpDe2go2KgaRleHCDTp"
            >>> ids: List[str] = client.get_album_neighbors(_id)
            >>> isinstance(ids, list)
            True
            >>> ids
            []
        """
        return []

    def get_track_neighbors(self, track_id: str) -> List[str]:
        """Get similar tracks

        Args:
            track_id (str): The track id

        Returns:
            List[str]: The list of ids

        Examples:
            >>> client = SpotifyStreamingAPIClient.from_env()
            >>> _id: str = "6rqhFgbbKwnb9MLmUQDhG6"
            >>> ids: List[str] = client.get_track_neighbors(_id)
            >>> isinstance(ids, list)
            True
            >>> for _id in ids:
            ...     assert(isinstance(_id, str))
            """
        similar_track_data: Dict = self.spotify_client.recommendations(
            seed_tracks=[track_id]
        )
        return [t["id"] for t in similar_track_data["tracks"]]

    def search(
        self, str_value: str, search_limit: int = 10, res_type: str = "track",
    ) -> List[Union[AlbumData, ArtistData, TrackData]]:
        """Performs a search on a string

        Args:
            str_value (str): the string to search
            search_limit (int, optional): The number of results to return. Defaults to 10.

        Returns:
            List: The list of the converted to datamodel results

        Examples:
            >>> client = SpotifyStreamingAPIClient.from_env()
            >>> type_res: str = "track"
            >>> search_str: str = "In the end"
            >>> res = client.search(search_str, res_type=type_res)
            >>> isinstance(res, list)
            True
            >>> type_res = "album"
            >>> search_str = "Hybrid Theory"
            >>> res = client.search(search_str, res_type=type_res)
            >>> isinstance(res, list)
            True
            >>> type_res = "artist"
            >>> search_str = "Linkin Park"
            >>> res = client.search(search_str, res_type=type_res)
            >>> isinstance(res, list)
            True
        """
        res: List = self.spotify_client.search(
            str_value, limit=search_limit, type=res_type,
        )
        formatted_res: List[Union[ArtistData, AlbumData, TrackData]] = []
        for r in res:
            converted: Union[AlbumData, ArtistData, TrackData] = self.convert(r)
            formatted_res.append(converted)
        return formatted_res

    def convert(self, r: Dict) -> Union[AlbumData, ArtistData, TrackData]:
        data = None
        return data

    @classmethod
    def from_env(cls, scope: Optional[Union[str, Tuple]] = None):
        if scope is not None:
            spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        else:
            spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
        spotify.current_user()
        return cls(spotify)
