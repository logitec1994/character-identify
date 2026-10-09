from pipewire_capture import PortalCapture, CaptureStream


class Capture:
    def __init__(self):
        self.session = None
        self.stream = None

    def start(self):
        self.session = PortalCapture().select_window()

        if self.session is None:
            raise RuntimeError("Window selection cancelled")

        self.stream = CaptureStream(
            self.session.fd,
            self.session.node_id,
            self.session.width,
            self.session.height,
        )

        self.stream.start()

    def get_frame(self):
        if self.stream is None:
            raise RuntimeError("Capture has not been started")

        return self.stream.get_frame()

    def stop(self):
        if self.stream is not None:
            self.stream.stop()
            self.stream = None

    def close(self):
        self.stop()

        if self.session is not None:
            self.session.close()
            self.session = None

