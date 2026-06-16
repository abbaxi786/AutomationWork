from datetime import datetime
from cli.create_files import GetPrintFileValue
import os


class Logging:

    def __init__(self, taskName, taskType):
        self.taskName = taskName
        self.taskType = taskType

        config = GetPrintFileValue('./config/config.json')
        self.log_file = config["settings"]["log_file"]

    def AddingLogs(self, message):

        folder = os.path.dirname(self.log_file)

        if folder:
            os.makedirs(folder, exist_ok=True)

        with open(self.log_file, "a", encoding="utf-8") as file:

            file.write(
                f"[{datetime.now()}] "
                f"[{self.taskType}] "
                f"[{self.taskName}] "
                f"{message}\n"
            )