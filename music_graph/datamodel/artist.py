from dataclasses import dataclass, field
from typing import List


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
