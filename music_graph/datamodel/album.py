from dataclasses import dataclass, field
from typing import Dict, List


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

    @classmethod
    def from_spotify_dict(cls, track_id: str, album_data: Dict):
        return cls(
            id=track_id,
            type=album_data["type"],
            uri=album_data["uri"],
            name=album_data["name"],
            href=album_data["href"],
            number_of_tracks=album_data["total_tracks"],
            artist_ids=[d["id"] for d in album_data["artists"]],
            genres=album_data.get("genres", []),
            track_ids=[d["id"] for d in album_data["tracks"]["items"]],
        )

    def to_dict(self) -> Dict:
        return {
            "data_id": self.data_id,
            "type": self.type,
            "uri": self.uri,
            "name": self.name,
            "href": self.href,
            "number_of_tracks": self.number_of_tracks,
            "artist_ids": self.artist_ids,
            "genres": self.genres,
            "track_ids": self.track_ids,
        }
