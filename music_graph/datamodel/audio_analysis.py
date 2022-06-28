from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass()
class Bar:
    """Bar object
        Note:
        Confidence is between 0 and 1
    """

    start: float
    duration: float
    confidence: float

    @staticmethod
    def from_dict(data_dict: Dict):
        return Bar(
            start=data_dict["start"],
            duration=data_dict["duration"],
            confidence=data_dict["confidence"],
        )

    def to_dict(self) -> Dict:
        return {
            "start": self.start,
            "duration": self.duration,
            "confidence": self.confidence,
        }


@dataclass()
class Tatum:
    """Tatum object
        Note:
        Confidence is between 0 and 1
    """

    start: float
    duration: float
    confidence: float

    @staticmethod
    def from_dict(data_dict: Dict):
        return Tatum(
            start=data_dict["start"],
            duration=data_dict["duration"],
            confidence=data_dict["confidence"],
        )

    def to_dict(self) -> Dict:
        return {
            "start": self.start,
            "duration": self.duration,
            "confidence": self.confidence,
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

    @staticmethod
    def from_dict(data_dict: Dict):
        return Section(
            start=data_dict["start"],
            duration=data_dict["duration"],
            confidence=data_dict["confidence"],
            loudness=data_dict["loudness"],
            tempo=data_dict["tempo"],
            tempo_confidence=data_dict["tempo_confidence"],
            key=data_dict["key"],
            key_confidence=data_dict["key_confidence"],
            mode=data_dict["mode"],
            mode_confidence=data_dict["mode_confidence"],
            time_signature=data_dict["time_signature"],
            time_signature_confidence=data_dict["time_signature_confidence"],
        )

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

    @staticmethod
    def from_dict(data_dict: Dict):
        return Segment(
            start=data_dict["start"],
            duration=data_dict["duration"],
            confidence=data_dict["confidence"],
            loudness_start=data_dict["loudness_start"],
            loudness_max=data_dict["loudness_max"],
            loudness_max_time=data_dict["loudness_max_time"],
            loudness_end=data_dict["loudness_end"],
            pitches=data_dict["pitches"],
            timbre=data_dict["timbre"],
        )

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
    """ Audio analysis object based on Spotify data
        Based on the following documentation from Spotify: https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-analysis
    """

    num_samples: int
    duration: float
    channels: Optional[int]
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

    @classmethod
    def from_dict(cls, data_dict: Dict):
        return cls(
            num_samples=data_dict["track"]["num_samples"],
            duration=data_dict["track"]["duration"],
            channels=data_dict["track"].get("channels"),
            loudness=data_dict["track"]["loudness"],
            tempo=data_dict["track"]["tempo"],
            tempo_confidence=data_dict["track"]["tempo_confidence"],
            time_signature=data_dict["track"]["time_signature"],
            time_signature_confidence=data_dict["track"]["time_signature_confidence"],
            key=data_dict["track"]["key"],
            key_confidence=data_dict["track"]["key_confidence"],
            mode=data_dict["track"]["mode"],
            mode_confidence=data_dict["track"]["mode_confidence"],
            codestring=data_dict["track"]["codestring"],
            code_version=data_dict["track"]["code_version"],
            echoprintstring=data_dict["track"]["echoprintstring"],
            echoprint_version=data_dict["track"]["echoprint_version"],
            synchstring=data_dict["track"]["synchstring"],
            synch_version=data_dict["track"]["synch_version"],
            rhythmstring=data_dict["track"]["rhythmstring"],
            rhythm_version=data_dict["track"]["rhythm_version"],
            bars=[Bar.from_dict(bar) for bar in data_dict["bars"]],
            sections=[Section.from_dict(sec) for sec in data_dict["sections"]],
            segments=[Segment.from_dict(seg) for seg in data_dict["segments"]],
            tatums=[Tatum.from_dict(tatum) for tatum in data_dict["tatums"]],
            metadata=data_dict.get("meta", {}),
        )

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
