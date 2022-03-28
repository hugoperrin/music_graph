from dataclasses import dataclass
from typing import List


@dataclass()
class UserInfo:
    id: str
    display_name: str
    playlist_ids: List[str]
    artist_ids: List[str]
    top_track_ids: List[str]
