import threading
import time

from gi.repository import GLib, Gtk

from .capture import Capture
from .window_geometry import WindowGeometry
from .overlay import Overlay
from .roi import extract_roi, prepare_detector_input
from .diagnostics import Diagnostics


FRAME_DELAY = 0.05  # Примерно 20 кадров в секунду


def main():
    capture = Capture()
    geometry = WindowGeometry()
    diagnostics = Diagnostics()

    stop_event = threading.Event()
    worker = None
    gtk_started = False

    try:
        # 1. Запускаем захват выбранного окна.
        capture.start()

        overlay = Overlay(
            capture.session.width,
            capture.session.height,
        )

        # 2. Обрабатываем кадр в главном GTK-потоке.
        def update_ui(frame, roi, detector_input, window_rect, monitor_rect):
            if window_rect is not None and monitor_rect is not None:
                overlay.update_window(window_rect, monitor_rect)

            diagnostics.show(frame, roi, detector_input)
            return False  # Одноразовый callback GLib

        # 3. Получаем и обрабатываем кадры в отдельном потоке.
        def capture_loop():
            try:
                while not stop_event.is_set():
                    frame = capture.get_frame()

                    if frame is None:
                        time.sleep(0.01)
                        continue

                    # Получаем геометрию целевого окна.
                    window_rect = geometry.get_target_window()
                    monitor_rect = (
                        geometry.find_monitor(window_rect)
                        if window_rect is not None
                        else None
                    )

                    # Выделяем ROI и подготавливаем вход детектора.
                    roi = extract_roi(frame)
                    detector_input = prepare_detector_input(roi)

                    # Передаём изображения главному потоку для отображения.
                    GLib.idle_add(
                        update_ui,
                        frame.copy(),
                        roi,
                        detector_input,
                        window_rect,
                        monitor_rect,
                    )

                    time.sleep(FRAME_DELAY)

            except Exception as exc:
                print(f"Ошибка обработки кадров: {exc}")
                GLib.idle_add(Gtk.main_quit)

        # 4. Периодически обрабатываем события окон OpenCV.
        def poll_diagnostics():
            key = diagnostics.poll_events()

            if key == 27:  # Escape
                Gtk.main_quit()
                return False

            return True

        GLib.timeout_add(10, poll_diagnostics)

        worker = threading.Thread(
            target=capture_loop,
            daemon=True,
        )
        worker.start()

        # 5. Запускаем цикл обработки событий GTK.
        gtk_started = True
        Gtk.main()

    except KeyboardInterrupt:
        print("Остановка по Ctrl+C")

    finally:
        stop_event.set()
        capture.close()

        if worker is not None:
            worker.join(timeout=1)

        diagnostics.close()


if __name__ == "__main__":
    main()
