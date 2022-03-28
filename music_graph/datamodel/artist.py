from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass()
class ArtistData:
    id: str
    album_ids: List[str]
    follower_num: int
    follower_href: str
    genres: List[str]
    href: str
    name: str
    popularity: float
    uri: str
    similar_artist_ids: List[str] = field(default_factory=list)
    top_track_ids: List[str] = field(default_factory=list)

    @property
    def data_id(self) -> str:
        return self.id

    @classmethod
    def from_spotify_dict(
        cls,
        artist_id: str,
        artist_data: Dict,
        top_tracks: Optional[Dict] = None,
        similar_artists: Optional[Dict] = None,
        albums: Optional[Dict] = None,
    ):
        return cls(
            id=artist_id,
            popularity=artist_data["popularity"],
            uri=artist_data["uri"],
            name=artist_data["name"],
            href=artist_data["href"],
            follower_href=artist_data["followers"]["href"],
            follower_num=artist_data["followers"]["total"],
            album_ids=[] if albums is None else [a["id"] for a in albums["items"]],
            genres=artist_data["genres"],
            similar_artist_ids=[]
            if similar_artists is None
            else [p["id"] for p in similar_artists["artists"]],
            top_track_ids=[]
            if top_tracks is None
            else [t["id"] for t in top_tracks["tracks"]],
        )

    def to_dict(self) -> Dict:
        return {
            "data_id": self.data_id,
            "popularity": self.popularity,
            "uri": self.uri,
            "name": self.name,
            "href": self.href,
            "follower_num": self.follower_num,
            "album_ids": self.album_ids,
            "genres": self.genres,
            "similar_artist_ids": self.similar_artist_ids,
            "top_track_ids": self.top_track_ids,
        }
