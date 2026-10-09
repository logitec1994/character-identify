import cv2

from .config import (
    ROI_X_RATIO,
    ROI_Y_RATIO,
    ROI_WIDTH_RATIO,
    ROI_HEIGHT_RATIO,
    ROI_SCALE,
)


def extract_roi(frame):
    """Extract an ROI from a frame using relative coordinates."""

    frame_height, frame_width = frame.shape[:2]

    x1 = int(frame_width * ROI_X_RATIO)
    y1 = int(frame_height * ROI_Y_RATIO)

    x2 = int(frame_width * (ROI_X_RATIO + ROI_WIDTH_RATIO))
    y2 = int(frame_height * (ROI_Y_RATIO + ROI_HEIGHT_RATIO))

    # Keep coordinates within the frame.
    x1 = max(0, min(x1, frame_width))
    y1 = max(0, min(y1, frame_height))
    x2 = max(0, min(x2, frame_width))
    y2 = max(0, min(y2, frame_height))

    if x2 <= x1 or y2 <= y1:
        raise ValueError("ROI has zero or negative dimensions")

    return frame[y1:y2, x1:x2].copy()


def prepare_detector_input(roi):
    """Resize the ROI before passing it to a detector."""

    if ROI_SCALE <= 0:
        raise ValueError("ROI_SCALE must be greater than zero")

    if ROI_SCALE == 1.0:
        return roi.copy()

    height, width = roi.shape[:2]

    new_width = max(1, round(width * ROI_SCALE))
    new_height = max(1, round(height * ROI_SCALE))

    interpolation = (
        cv2.INTER_CUBIC
        if ROI_SCALE > 1.0
        else cv2.INTER_AREA
    )

    return cv2.resize(
        roi,
        (new_width, new_height),
        interpolation=interpolation,
    )
