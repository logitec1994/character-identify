from dataclasses import dataclass, field
from typing import Protocol

from .frame import Frame


@dataclass
class FaceDetection:
    bbox: tuple[float, float, float, float]
    confidence: float
    landmarks: list[tuple[float, float]] | None = None


@dataclass
class DetectionResult:
    timestamp: float
    faces: list[FaceDetection] = field(default_factory=list)


class FaceDetector(Protocol):
    def detect(self, frame: Frame) -> DetectionResult:
        ...
