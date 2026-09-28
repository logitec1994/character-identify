import argparse

from .frame_provider import VideoFileFrameProvider


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video_path")
    args = parser.parse_args()

    frame_count = 0
    first_frame = None
    last_frame = None

    for frame in VideoFileFrameProvider(args.video_path):
        if first_frame is None:
            first_frame = frame
        last_frame = frame
        frame_count += 1

    first_id = first_frame.id if first_frame is not None else None
    first_timestamp = first_frame.timestamp if first_frame is not None else None
    last_id = last_frame.id if last_frame is not None else None
    last_timestamp = last_frame.timestamp if last_frame is not None else None

    print(f"Total frames: {frame_count}")
    print(f"First frame: id={first_id}, timestamp={first_timestamp}")
    print(f"Last frame: id={last_id}, timestamp={last_timestamp}")