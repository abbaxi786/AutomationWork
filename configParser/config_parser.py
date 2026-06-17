from fileOps.create_files import GetPrintFileValue
from parsedExe.classes import Scheduler, CreateOrWriteFileClass
from parsedExe.exe_cli import CliExecution
from logger.log import Logging
from send_email.email import Email


class ParserValueConvergence:

    def __init__(self, filePath):
        self.jsonData = GetPrintFileValue(filePath)
        
        self.schedulers = []

        self.taskTypes = {
            "createFile": CreateOrWriteFileClass,
            "shell": CliExecution,
            "schedule": Scheduler,
            "log": Logging,
            "email": Email
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
            
            if(task["schedule"]["type"] == "interval"):

                s = scheduler(
                task["schedule"]["seconds"],
                lambda t=task: self.RunningCreateFile(t)
                )
                s.start()
                self.schedulers.append(s)
            elif(task["schedule"]["type"] == "timeout"):
                s = scheduler(
                task["schedule"]["seconds"],
                lambda t=task: self.RunningCreateFile(t)
                )
                s.set_timeout()
                self.schedulers.append(s)
                

            

    
    def RunShell(self):

        tasks = self.TaskGiver("shell")

        for task in tasks:

            scheduler = self.taskTypes["schedule"]
            
            if(task["schedule"]["type"] == "interval"):
                
                s = scheduler(
                task["schedule"]["seconds"],
                lambda t=task: self.RunningShell(t)
                )
                s.start()
                self.schedulers.append(s)
                
            elif(task["schedule"]["type"] == "timeout"):
                s = scheduler(
                    task["schedule"]["seconds"],
                    lambda t=task: self.RunningShell(t)
                )
                s.set_timeout()
                self.schedulers.append(s)
                

    
    def RunningLog(self, task):

        logger = Logging(task["task_name"], task["task_type"])

        message = task["log"]["messages"]
        for key ,values in message.items():
            print(f"message have beed added:  {key} : {values}")

            logger.AddingLogs(f"{message[key]}")

    def RunLog(self):

        tasks = self.TaskGiver("log")
        
        print(tasks)
        
        for task in tasks:

            scheduler = self.taskTypes["schedule"]
            if(task["schedule"]["type"] == "interval"):
                s = scheduler(
                task["schedule"]["seconds"],
                lambda t=task: self.RunningLog(t)
                )

                s.start()
                self.schedulers.append(s)
            elif(task["schedule"]["type"] == "timeout"):
                    s= scheduler(
                    task["schedule"]["seconds"],
                    lambda t=task: self.RunningLog(t)
                    )
                    s.set_timeout()
                    self.schedulers.append(s)
                    
    def EmailSender(self, task):

        logger = Logging(task["task_name"], task["task_type"])
        logger.AddingLogs("Task started")

        try:
            run_class = self.taskTypes["email"]

            obj = run_class(
                task["task_name"],
                task["task_type"],
                task["email"]["to"],        # FIX
                task["email"]["subject"],   # FIX
                task["email"]["body"]       # FIX
            )

            obj.send_email()

            logger.AddingLogs("Email sent successfully")

        except Exception as e:
            print(f"The email issue : {str(e)}")
            logger.AddingLogs(f"Error: {str(e)}")
                    
    def RunEmail(self):
        tasks = self.TaskGiver("email");
        
        for task in tasks:
            scheduler = self.taskTypes["schedule"]
            if(task["schedule"]["type"] == "interval"):
                s = scheduler(
                task["schedule"]["seconds"],
                lambda t=task: self.EmailSender(t)
                )

                s.start()
                self.schedulers.append(s)
            elif(task["schedule"]["type"] == "timeout"):
                    s=scheduler(
                    task["schedule"]["seconds"],
                    lambda t=task: self.EmailSender(t)
                    )
                    s.set_timeout()
                    self.schedulers.append(s)
                    
    def StopAll(self):

            print("Stopping all schedulers...")

            for scheduler in self.schedulers:
                scheduler.stop()

            self.schedulers.clear()

            print("All schedulers stopped.")
                    
    def __del__(self):
        self.StopAll()
        print("Parser destroyed")
        



def main():

    p = ParserValueConvergence('config/config.json')

    p.RunShell()
    p.CreateFile()
    p.RunLog()
    p.RunEmail()

    import time
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
    
    # py -m configParser.config_parser