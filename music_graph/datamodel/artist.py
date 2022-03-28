from dataclasses import dataclass, field
from typing import Dict, List


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
    similar_playlist_ids: List[str] = field(default_factory=list)
    top_track_ids: List[str] = field(default_factory=list)

    @property
    def data_id(self) -> str:
        return self.id

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
            "similar_playlist_ids": self.similar_playlist_ids,
            "top_track_ids": self.top_track_ids,
        }
