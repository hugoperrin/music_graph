from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass()
class Bar:
    """Bar object
        Note:
        Confidence is between 0 and 1
    """

    start: float
    end: float
    confidence: float


@dataclass()
class Tatum:
    """Tatum object
        Note:
        Confidence is between 0 and 1
    """

    start: float
    end: float
    confidence: float


@dataclass()
class Section:
    start: float
    duration: float
    confidence: float
    loudness: float
    tempo: float
    tempo_confidence: float
    key: int
    key_confidence: float
    mode: int
    mode_confidence: float
    time_signature: int
    time_signature_confidence: float


@dataclass()
class Segment:
    """Segment object
        Note:
            - pitches: 12 values list of normalized floats between 0 and 1
            - timbre: 12 values list of normalized floats
    """

    start: int
    duration: float
    confidence: str
    loudness_start: float
    loudness_max: float
    loudness_max_time: float
    loudness_end: float
    pitches: List[float]
    timbre: List[float]


@dataclass()
class AudioAnalysis:
    """ Audio analysis object based on Spotify data (#TODO: determine if Tidal and so on provide such data as well)
        Based on the following documentation from Spotify: https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-analysis
    """

    num_samples: int
    duration: float
    channels: int
    loudness: float
    tempo: float
    tempo_confidence: float
    time_signature: int
    time_signature_confidence: float
    key: int
    key_confidence: float
    mode: int
    mode_confidence: float
    codestring: Optional[str] = None
    code_version: Optional[int] = None
    echoprintstring: Optional[str] = None
    echoprint_version: Optional[int] = None
    synchstring: Optional[str] = None
    synch_version: Optional[int] = None
    rhythmstring: Optional[str] = None
    rhythm_version: Optional[int] = None
    bars: List[Bar] = field(default_factory=list)
    sections: List[Section] = field(default_factory=list)
    segments: List[Segment] = field(default_factory=list)
    tatums: List[Tatum] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
