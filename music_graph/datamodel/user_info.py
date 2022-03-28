from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass()
class UserInfo:
    id: str
    display_name: str
    href: str
    uri: str
    playlist_ids: List[str]
    artist_ids: List[str]
    top_track_ids: List[str]
    saved_track_ids: List[str]
    saved_album_ids: List[str]

    @classmethod
    def from_spotify_dict(
        cls,
        user_data: Dict,
        artists_data: Optional[Dict] = None,
        playlist_data: Optional[Dict] = None,
        top_tracks: Optional[Dict] = None,
        saved_tracks: Optional[Dict] = None,
        saved_albums: Optional[Dict] = None,
    ):
        return cls(
            id=user_data["id"],
            display_name=user_data["display_name"],
            href=user_data["href"],
            uri=user_data["uri"],
            playlist_ids=[]
            if playlist_data is None
            else [p["id"] for p in playlist_data["items"]],
            artist_ids=[]
            if artists_data is None
            else [a["id"] for a in artists_data["artists"]["items"]],
            top_track_ids=[]
            if top_tracks is None
            else [t["id"] for t in top_tracks["items"]],
            saved_track_ids=[]
            if saved_tracks is None
            else [t["track"]["id"] for t in saved_tracks["items"]],
            saved_album_ids=[]
            if saved_albums is None
            else [a["album"]["id"] for a in saved_albums["items"]],
        )
