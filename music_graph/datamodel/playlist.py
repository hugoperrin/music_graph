from dataclasses import dataclass, field
from typing import Dict, List


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

    @classmethod
    def from_spotify_dict(cls, playlist_data: Dict):
        return cls(
            id=playlist_data["id"],
            follower_number=playlist_data["followers"]["total"],
            uri=playlist_data["uri"],
            name=playlist_data["name"],
            track_ids=[t["track"]["id"] for t in playlist_data["tracks"]["items"]],
        )

    def to_dict(self) -> Dict:
        return {
            "data_id": self.data_id,
            "follower_number": self.follower_number,
            "uri": self.uri,
            "name": self.name,
            "track_ids": self.track_ids,
        }
