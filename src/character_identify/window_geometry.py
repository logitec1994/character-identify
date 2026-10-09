from gi.repository import Gio, Gdk

from .config import (
    TARGET_TITLE,
    WINDOW_GEOMETRY_BUS_NAME,
    WINDOW_GEOMETRY_OBJECT_PATH,
    WINDOW_GEOMETRY_INTERFACE,
)


class WindowGeometry:
    def __init__(self):
        self.bus = Gio.bus_get_sync(
            Gio.BusType.SESSION,
            None,
        )

        self.display = Gdk.Display.get_default()

    def get_target_window(self):
        result = self.bus.call_sync(
            WINDOW_GEOMETRY_BUS_NAME,
            WINDOW_GEOMETRY_OBJECT_PATH,
            WINDOW_GEOMETRY_INTERFACE,
            "GetWindows",
            None,
            None,
            Gio.DBusCallFlags.NONE,
            -1,
            None,
        )

        windows = result.unpack()[0]

        for title, x, y, width, height in windows:
            if TARGET_TITLE in title:
                return x, y, width, height

        return None

    def get_monitors(self):
        monitors = []

        for i in range(self.display.get_n_monitors()):
            monitor = self.display.get_monitor(i)
            geometry = monitor.get_geometry()

            monitors.append((
                geometry.x,
                geometry.y,
                geometry.width,
                geometry.height,
            ))

        return monitors

    def find_monitor(self, window_rect):
        x, y, width, height = window_rect

        center_x = x + width / 2
        center_y = y + height / 2

        for monitor_rect in self.get_monitors():
            monitor_x, monitor_y, monitor_width, monitor_height = (
                monitor_rect
            )

            if (
                monitor_x <= center_x < monitor_x + monitor_width
                and
                monitor_y <= center_y < monitor_y + monitor_height
            ):
                return monitor_rect

        return None
