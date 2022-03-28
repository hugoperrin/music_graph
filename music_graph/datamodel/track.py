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
