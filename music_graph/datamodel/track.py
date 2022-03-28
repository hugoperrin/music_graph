from dataclasses import dataclass, field
from typing import Dict, List, Optional

from music_graph.datamodel.audio_analysis import AudioAnalysis


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
    audio_analysis: Optional[AudioAnalysis] = None

    @property
    def data_id(self) -> str:
        return self.id

    @classmethod
    def from_spotify_dict(
        cls, track_id: str, track_data: Dict, audio_analysis: Optional[Dict] = None
    ):
        return cls(
            id=track_id,
            album_id=track_data["album"]["id"],
            artist_ids=[artist_dict["id"] for artist_dict in track_data["artists"]],
            duration=track_data["duration_ms"],
            api_href=track_data["href"],
            linked_track_ids=[],
            uri=track_data["uri"],
            track_number=track_data["track_number"],
            name=track_data["name"],
            popularity=track_data["popularity"],
            preview_url=track_data["preview_url"],
            track_playlist_ids=[],
            audio_analysis=audio_analysis
            if audio_analysis is None
            else AudioAnalysis.from_dict(audio_analysis),
        )

    def to_dict(self) -> Dict:
        audio_analysis: Optional[Dict] = None
        if self.audio_analysis:
            audio_analysis = self.audio_analysis.to_dict()
        return {
            "data_id": self.data_id,
            "popularity": self.popularity,
            "uri": self.uri,
            "name": self.name,
            "album_id": self.album_id,
            "duration": self.duration,
            "api_href": self.api_href,
            "track_number": self.track_number,
            "preview_url": self.preview_url,
            "artist_ids": self.artist_ids,
            "linked_track_ids": self.linked_track_ids,
            "track_playlist_ids": self.track_playlist_ids,
            "audio_analysis": audio_analysis,
        }
