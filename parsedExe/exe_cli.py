import subprocess

class CliExecution:
    def __init__(self ,task_name, task_type, command):
        self.command = command  
        self.task_name = task_name
        self.task_type = task_type      
    
    def Process(self):
        print(self.task_name)
        print(self.task_type)
        result = subprocess.run(self.command, shell=True, capture_output = True , text= True)
        print(result)
        return result
        
    