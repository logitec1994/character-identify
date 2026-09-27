from collections.abc import Iterator
from pathlib import Path
from typing import Protocol

import cv2

from .frame import Frame


class FrameProvider(Protocol):
    def __iter__(self) -> Iterator[Frame]:
        ...


class VideoFileFrameProvider:
    def __init__(self, video_path: str | Path) -> None:
        self.video_path = str(video_path)

    def __iter__(self) -> Iterator[Frame]:
        capture = cv2.VideoCapture(self.video_path)
        fps = capture.get(cv2.CAP_PROP_FPS)
        frame_id = 0

        try:
            while True:
                success, image = capture.read()
                if not success:
                    break

                yield Frame(
                    id=frame_id,
                    timestamp=frame_id / fps,
                    image=image,
                )
                frame_id += 1
        finally:
            capture.release()
