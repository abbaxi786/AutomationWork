from cli.create_files import GetPrintFileValue
from parsedExe.classes import Scheduler, CreateOrWriteFileClass
from parsedExe.exe_cli import CliExecution


class ParserValueConvergence:

    def __init__(self, filePath):
        self.jsonData = GetPrintFileValue(filePath)

        self.taskTypes = {
            "createFile": CreateOrWriteFileClass,
            "shell": CliExecution,
            "schedule": Scheduler
        }

    def TaskGiver(self, taskType):

        tasks = self.jsonData["tasks"]

        return [
            task
            for task in tasks
            if task["task_type"] == taskType
        ]

   
    def RunningCreateFile(self, task):

       
        run_class = self.taskTypes["createFile"]

        obj = run_class(task["task_name"],task["task_type"],
            task["file"]["path"],
            task["file"]["content"]
        )

        obj.CreateFile()

    
    def RunningShell(self, task):

        # FIX: wrong "task_Type" fixed
        run_class = self.taskTypes["shell"]

        obj = run_class(task["task_name"],task["task_type"],task["command"])
        obj.Process()

    
    def RunShell(self):

        tasks = self.TaskGiver("shell")

        for task in tasks:

            scheduler = self.taskTypes["schedule"]

            scheduler(
                task["schedule"]["seconds"],
                lambda t=task: self.RunningShell(t)
            ).start()

    
    def CreateFile(self):

        tasks = self.TaskGiver("createFile")

        for task in tasks:

            scheduler = self.taskTypes["schedule"]

            scheduler(
                task["schedule"]["seconds"],
                lambda t=task: self.RunningCreateFile(t)
            ).start()



def main():

    p = ParserValueConvergence('config/config.json')

    p.RunShell()
    p.CreateFile()


if __name__ == "__main__":
    main()
    
    
    # py -m configParser.config_parser