from pathlib import Path

import cv2

from .config import (
    SHOW_DIAGNOSTICS,
    SAVE_DIAGNOSTIC_IMAGES,
    DIAGNOSTICS_DIR,
)


class Diagnostics:
    def __init__(self):
        self.enabled = SHOW_DIAGNOSTICS
        self.save_images = SAVE_DIAGNOSTIC_IMAGES
        self.output_dir = Path(DIAGNOSTICS_DIR)

        if self.save_images:
            self.output_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

    def show(self, frame, roi, detector_input):
        """Display the original frame, ROI, and detector input."""

        if not self.enabled:
            return

        cv2.imshow("1 - Captured frame", frame)
        cv2.imshow("2 - ROI", roi)
        cv2.imshow("3 - Detector input", detector_input)

        if self.save_images:
            self.save(
                frame,
                roi,
                detector_input,
            )

    def save(self, frame, roi, detector_input):
        """Save diagnostic images to disk."""

        cv2.imwrite(
            str(self.output_dir / "captured_frame.png"),
            frame,
        )

        cv2.imwrite(
            str(self.output_dir / "roi.png"),
            roi,
        )

        cv2.imwrite(
            str(self.output_dir / "detector_input.png"),
            detector_input,
        )

    def poll_events(self):
        """Process OpenCV window events."""

        if self.enabled:
            return cv2.waitKey(1) & 0xFF

        return -1

    def close(self):
        cv2.destroyAllWindows()
