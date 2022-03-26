from dataclasses import dataclass, field
from typing import List


@dataclass()
class PlaylistData:
    id: str
    follower_number: int
    name: str
    uri: str
    track_ids: List[str] = field(default_factory=list)

    @property
    def data_id(self) -> str:
        return self.id
