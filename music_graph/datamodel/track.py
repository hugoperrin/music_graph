from dataclasses import dataclass, field
from typing import List, Optional


@dataclass()
class TrackData:
    id: str
    album_id: str
    artist_ids: List[str]
    duration: int
    api_href: str
    linked_track_ids: List[str]
    uri: str
    track_number: int
    name: str
    popularity: Optional[float] = None
    preview_url: Optional[str] = None
    track_playlist_ids: List[str] = field(default_factory=list)

    @property
    def data_id(self) -> str:
        return self.id
