from cli.create_files import CreateOrWriteFile
from schedular.wait import set_interval
import threading

class CreateOrWriteFileClass:

    def __init__(self, taskName,taskType,  file, content):
        self.file = file
        self.content = content
        self.taskName = taskName
        self.taskType = taskType

    def CreateFile(self):
        # safer access (supports dict or object)
        file_path = self.file.get("path") if isinstance(self.file, dict) else self.file
        print(self.taskName)
        print(self.taskType)
        CreateOrWriteFile(file_path, self.content)

    
class Scheduler:

    def __init__(self, interval, function):
        self.interval = interval
        self.function = function

        self.stop_event = threading.Event()
        self.thread = None

    def start(self):
        self.thread = set_interval(
            self.function,
            self.interval,
            self.stop_event
        )
    def stop(self):
        self.stop_event.set()
    

        
    

    
        