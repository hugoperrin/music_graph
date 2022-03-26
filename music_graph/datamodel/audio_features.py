from dataclasses import dataclass


@dataclass()
class AudioFeatures:
    acousticness: float
    danceability: float
    duration_ms: float
    energy: float
    instrumentalness: float
    key: int
    liveness: float
    loudness: float
    mode: int
    speechiness: float
    tempo: float
    time_signature: int
    uri: str
    valence: float
