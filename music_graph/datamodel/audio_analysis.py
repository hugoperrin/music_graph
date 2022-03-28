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

    def to_dict(self) -> Dict:
        return {
            "start": self.start, "end": self.end, "confidence": self.confidence,
        }


@dataclass()
class Tatum:
    """Tatum object
        Note:
        Confidence is between 0 and 1
    """

    start: float
    end: float
    confidence: float

    def to_dict(self) -> Dict:
        return {
            "start": self.start, "end": self.end, "confidence": self.confidence,
        }


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

    def to_dict(self) -> Dict:
        return {
            "start": self.start,
            "duration": self.duration,
            "confidence": self.confidence,
            "loudness": self.loudness,
            "tempo": self.tempo,
            "tempo_confidence": self.tempo_confidence,
            "key": self.key,
            "key_confidence": self.key_confidence,
            "mode": self.mode,
            "mode_confidence": self.mode_confidence,
            "time_signature": self.time_signature,
            "time_signature_confidence": self.time_signature_confidence,
        }


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

    def to_dict(self) -> Dict:
        return {
            "start": self.start,
            "duration": self.duration,
            "confidence": self.confidence,
            "loudness_start": self.loudness_start,
            "loudness_max": self.loudness_max,
            "loudness_max_time": self.loudness_max_time,
            "loudness_end": self.loudness_end,
            "pitches": self.pitches,
            "timbre": self.timbre,
        }


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

    def to_dict(self) -> Dict:
        return {
            "num_samples": self.num_samples,
            "duration": self.duration,
            "channels": self.channels,
            "loudness": self.loudness,
            "tempo": self.tempo,
            "tempo_confidence": self.tempo_confidence,
            "time_signature": self.time_signature,
            "time_signature_confidence": self.time_signature_confidence,
            "key": self.key,
            "key_confidence": self.key_confidence,
            "mode": self.mode,
            "mode_confidence": self.mode_confidence,
            "codestring": self.codestring,
            "code_version": self.code_version,
            "echoprintstring": self.echoprintstring,
            "echoprint_version": self.echoprint_version,
            "synchstring": self.synchstring,
            "synch_version": self.synch_version,
            "rhythmstring": self.rhythmstring,
            "rhythm_version": self.rhythm_version,
            "bars": [bar.to_dict() for bar in self.bars],
            "sections": [sec.to_dict() for sec in self.sections],
            "segments": [seg.to_dict() for seg in self.segments],
            "tatums": [tat.to_dict() for tat in self.tatums],
            "metadata": self.metadata,
        }
