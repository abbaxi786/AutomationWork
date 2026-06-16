from cli.create_files import GetPrintFileValue
from parsedExe.classes import Scheduler, CreateOrWriteFileClass
from parsedExe.exe_cli import CliExecution



class ParserValueConvergence:    
            
    def __init__(self, filePath):
        self.jsonData = GetPrintFileValue(filePath) 
        self.taskTypes = {"createFile" :CreateOrWriteFileClass,
                        "shell": CliExecution,
                        'schedule': Scheduler}
                     
        
    def TaskGiver(self,taskType):
        tasks = self.jsonData["tasks"]
        arrayOfFilesTypes = []
        arrayOfFilesTypes.append(list(filter(lambda x: x["task_type"] == taskType , tasks)))
        print(arrayOfFilesTypes[0])
        return arrayOfFilesTypes
    
    
    def RunningCreateFile(self,object):
         run = self.taskTypes["task_Type"] 
         run(object["task_Name"],object["task_type"],object["file"]["path"], object["file"]["content"])
        
    
    def CreateFile(self):
        sameTaskArray = self.TaskGiver('createFile')
        for i in sameTaskArray:
            ob = self.taskTypes["schedule"]
            ob(i["schedule"]["seconds"],self.RunningCreateFile(i))
        
    def RunningShell(self,object):
         run = self.taskTypes["task_Type"] 
         run(object["task_Name"],object["task_type"],object["command"])
        
    
    def RunShell(self):
        sameTaskArray = self.TaskGiver('shell')
        for i in sameTaskArray:
            ob = self.taskTypes['schedule']
            ob(i["schedule"]["seconds"],self.RunningShell(i))
            
    
    
        
        
        
def main():
    p = ParserValueConvergence('config/config.json')
    p.RunShell('shell')
    p.CreateFile('createFile')
    
if(__name__ == "__main__"):
    main()


# command for file execution py -m configParser.config_parser