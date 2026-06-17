import threading
import time

def set_interval(func, interval_seconds, stop_event, *args, **kwargs):

    def loop():
        while not stop_event.is_set():
            func(*args, **kwargs)
            time.sleep(interval_seconds)

    thread = threading.Thread(target=loop)
    thread.start()

    return thread

def SetTimeOut(func, seconds, *args, **kwargs):
    timer = threading.Timer(
        seconds,
        func,
        args=args,
        kwargs=kwargs
    )
    timer.start()
    return timer