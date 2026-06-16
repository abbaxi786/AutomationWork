from cli.create_files import GetPrintFileValue
from parsedExe.classes import Scheduler, CreateOrWriteFileClass
from parsedExe.exe_cli import CliExecution
from logger.log import Logging


class ParserValueConvergence:

    def __init__(self, filePath):
        self.jsonData = GetPrintFileValue(filePath)

        self.taskTypes = {
            "createFile": CreateOrWriteFileClass,
            "shell": CliExecution,
            "schedule": Scheduler,
            "log": Logging
        }

   
    def TaskGiver(self, taskType):

        tasks = self.jsonData["tasks"]

        return [
            task
            for task in tasks
            if task["task_type"] == taskType
        ]

    
    def RunningCreateFile(self, task):

        logger = Logging(task["task_name"], task["task_type"])
        logger.AddingLogs("Task started")

        try:
            run_class = self.taskTypes["createFile"]

            obj = run_class(
                task["task_name"],
                task["task_type"],
                task["file"]["path"],
                task["file"]["content"]
            )

            obj.CreateFile()

            logger.AddingLogs("Task completed successfully")

        except Exception as e:
            logger.AddingLogs(f"Error: {str(e)}")

    
    def RunningShell(self, task):

        logger = Logging(task["task_name"], task["task_type"])
        logger.AddingLogs("Task started")

        try:
            run_class = self.taskTypes["shell"]

            obj = run_class(
                task["task_name"],
                task["task_type"],
                task["command"]
            )

            obj.Process()

            logger.AddingLogs("Task completed successfully")

        except Exception as e:
            logger.AddingLogs(f"Error: {str(e)}")

    
    def CreateFile(self):

        tasks = self.TaskGiver("createFile")

        for task in tasks:

            scheduler = self.taskTypes["schedule"]

            scheduler(
                task["schedule"]["seconds"],
                lambda t=task: self.RunningCreateFile(t)
            ).start()

    
    def RunShell(self):

        tasks = self.TaskGiver("shell")

        for task in tasks:

            scheduler = self.taskTypes["schedule"]

            scheduler(
                task["schedule"]["seconds"],
                lambda t=task: self.RunningShell(t)
            ).start()

    
    def RunningLog(self, task):

        logger = Logging(task["task_name"], task["task_type"])

        message = task["log"]["messages"]["start"]

        logger.AddingLogs(message)

    def RunLog(self):

        tasks = self.TaskGiver("log")

        for task in tasks:

            scheduler = self.taskTypes["schedule"]

            scheduler(
                task["schedule"]["seconds"],
                lambda t=task: self.RunningLog(t)
            ).start()



def main():

    p = ParserValueConvergence('config/config.json')

    p.RunShell()
    p.CreateFile()
    p.RunLog()

    import time
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()