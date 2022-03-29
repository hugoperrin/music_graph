from typing import List, Optional

import tidalapi as tidal

from music_graph.datamodel.album import AlbumData
from music_graph.datamodel.artist import ArtistData
from music_graph.datamodel.playlist import PlaylistData
from music_graph.datamodel.track import TrackData
from music_graph.datamodel.user_info import UserInfo


class TidalAPIConverter:
    def track_converter(
        self,
        track_raw: tidal.models.Track,
        similar_tracks: Optional[List[tidal.models.Track]] = None,
    ) -> TrackData:
        uri: str = f"https://tidal.com/browse/track/{track_raw.id}"
        return TrackData(
            id=str(track_raw.id),
            album_id=str(track_raw.album.id),
            artist_ids=[str(art.id) for art in track_raw.artists],
            duration=track_raw.duration,
            api_href=uri,
            linked_track_ids=[],
            uri=uri,
            track_number=track_raw.track_num,
            name=track_raw.name,
            popularity=track_raw.popularity,
            preview_url=None,  # there is no preview on tidal
            track_playlist_ids=[]
            if similar_tracks is None
            else [str(t.id) for t in similar_tracks],
            audio_analysis=None,  # there is no audio analysis on tidal
        )

    def album_converter(
        self, album_raw: tidal.models.Album, album_tracks: List[tidal.models.Track]
    ) -> AlbumData:
        uri: str = f"https://tidal.com/browse/album/{album_raw.id}"
        return AlbumData(
            id=str(album_raw.id),
            type="album",
            artist_ids=[str(art.id) for art in album_raw.artists],
            href=uri,
            name=album_raw.name,
            uri=uri,
            number_of_tracks=album_raw.num_tracks,
            track_ids=[str(t.id) for t in album_tracks],
            genres=[],  # There are no genre informations in tidal api
        )

    def artist_converter(
        self,
        artist_raw: tidal.models.Artist,
        albums: List[tidal.models.Album],
        similar_artists: Optional[List[tidal.models.Artist]],
        top_tracks: Optional[List[tidal.models.Track]],
    ) -> ArtistData:
        uri: str = f"https://tidal.com/browse/artist/{artist_raw.id}"
        return ArtistData(
            id=str(artist_raw.id),
            album_ids=[str(a.id) for a in albums],
            follower_num=-1,  # There are no follower data in tidal api
            genres=[],  # There are no genre informations in tidal api
            follower_href="",  # There are no follower data in tidal api
            href=uri,
            uri=uri,
            name=artist_raw.name,
            popularity=-1.0,  # There are no artist popularity data in tidal api
            similar_artist_ids=[]
            if similar_artists is None
            else [str(a.id) for a in similar_artists],
            top_track_ids=[] if top_tracks is None else [str(t.id) for t in top_tracks],
        )

    def playlist_converter(
        self,
        playlist_raw: tidal.models.Playlist,
        playlist_tracks: List[tidal.models.Track],
    ) -> PlaylistData:
        uri: str = f"https://tidal.com/browse/playlist/{playlist_raw.id}"
        return PlaylistData(
            id=playlist_raw.id,
            follower_number=-1,  # There are no follower data in tidal api
            name=playlist_raw.name,
            uri=uri,
            track_ids=[str(t.id) for t in playlist_tracks],
            description=playlist_raw.description,
            duration=playlist_raw.duration,
        )

    def user_converter(self, user_data: tidal.User) -> UserInfo:
        return UserInfo(
            id=str(user_data.id),
            display_name=user_data.id,
            href="",  # No uri for profiles on tidal
            uri="",  # No uri for profiles on tidal
            playlist_ids=[str(p.id) for p in user_data.playlists()],
            artist_ids=[str(a.id) for a in user_data.favorites.artists()],
            saved_album_ids=[str(a.id) for a in user_data.favorites.albums()],
            saved_track_ids=[str(t.id) for t in user_data.favorites.tracks()],
            top_track_ids=[],  # No top track per user on tidal
        )
