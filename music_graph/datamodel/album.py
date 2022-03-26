from dataclasses import dataclass, field
from typing import List


@dataclass()
class AlbumData:
    id: str
    type: str
    artist_ids: List[str]
    genres: List[str]
    href: str
    name: str
    uri: str
    number_of_tracks: int
    track_ids: List[str] = field(default_factory=list)

    @property
    def data_id(self) -> str:
        return self.id
