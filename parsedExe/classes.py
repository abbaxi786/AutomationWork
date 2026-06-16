from cli.create_files import CreateOrWriteFile
from schedular.wait import set_interval
import threading

class CreateOrWriteFileClass:

    def __init__(self, taskName, taskType, file, content):
        self.file = file
        self.content = content
        self.taskName = taskName
        self.taskType = taskType

    def CreateFile(self):

        file_path = self.file["path"] if isinstance(self.file, dict) else self.file

        print(f"[TASK] {self.taskName}")
        print(f"[TYPE] {self.taskType}")

        CreateOrWriteFile(file_path, self.content)

    
import threading
import time

class Scheduler:

    def __init__(self, interval, function):
        self.interval = interval
        self.function = function

        self.stop_event = threading.Event()
        self.thread = None

    # FIX: proper start method
    def start(self):

        def loop():
            while not self.stop_event.is_set():
                self.function()
                time.sleep(self.interval)

        # FIX: NOT daemon → prevents shutdown crash
        self.thread = threading.Thread(target=loop)
        self.thread.start()

        return self.thread

    # FIX: safe stop
    def stop(self):
        self.stop_event.set()

        if self.thread:
            self.thread.join()

        
    

    
        