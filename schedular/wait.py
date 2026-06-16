import threading
import time

def set_interval(func, interval_seconds, stop_event, *args, **kwargs):
    """
    Run a function repeatedly every X seconds until stop_event is set.
    """

    def loop():
        while not stop_event.is_set():
            func(*args, **kwargs)
            time.sleep(interval_seconds)

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()

    return thread