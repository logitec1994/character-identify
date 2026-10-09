import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")

from gi.repository import Gtk


class Overlay(Gtk.Window):
    def __init__(self, width, height):
        super().__init__()

        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_app_paintable(True)
        self.set_default_size(width, height)

        screen = self.get_screen()
        visual = screen.get_rgba_visual()

        if visual:
            self.set_visual(visual)

        self.window_rect = None
        self.monitor_rect = None

        self.connect("draw", self.draw)
        self.connect("destroy", Gtk.main_quit)

        self.show_all()
        self.get_window().set_pass_through(True)

    def draw(self, widget, cr):
        if self.window_rect is None or self.monitor_rect is None:
            return

        window_x, window_y, width, height = self.window_rect
        monitor_x, monitor_y, _, _ = self.monitor_rect

        x = window_x - monitor_x
        y = window_y - monitor_y

        # Full window: red rectangle
        cr.set_source_rgba(1.0, 0.0, 0.0, 1.0)
        cr.set_line_width(5)
        cr.rectangle(x, y, width, height)
        cr.stroke()

        # Upper half: blue ROI rectangle
        roi_height = height // 2

        cr.set_source_rgba(0.0, 0.0, 1.0, 1.0)
        cr.set_line_width(5)
        cr.rectangle(x, y, width, roi_height)
        cr.stroke()

    def update_window(self, window_rect, monitor_rect):
        self.window_rect = window_rect

        if self.monitor_rect != monitor_rect:
            self.monitor_rect = monitor_rect

            monitor_x, monitor_y, _, _ = monitor_rect
            self.move(monitor_x, monitor_y - 20)

        self.queue_draw()
