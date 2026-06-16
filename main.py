# from cli.command import GetPrintFileValue
from schedular.wait import set_interval
import threading


def PrintValue():
    print("Program running.")


# Create stop controller
stop_event = threading.Event()

# Start interval
thread = set_interval(PrintValue, 2, stop_event)


# Let it run for some time (example)
import time
time.sleep(10)

# Stop interval
stop_event.set()



