import sys
from parallels import parallels 

"""
append the location of this task to sys.path so that the executor can 
find it
"""
sys.path.append("/Users/sgolecha/Projects/github/piranha/parallels/test")

"""
This is an example of a simple task
"""
class PrintTask(parallels.BaseTask):
    def __init__(self, **kwargs):
        parallels.BaseTask.__init__(self, **kwargs)
    
    def execute(self, **kwargs):
        print("Executing print task")
        for k,v in kwargs.items():
            print("k: {0}, v: {1}".format(k, v))
        return kwargs


if __name__ == "__main__":
    #create the TaskManager
    taskManager = parallels.TaskManager("./tasks.yaml", "./results.yaml")
    
    #parse the task.yaml
    taskManager.parseTaskFile()
    
    #parse the results.yaml file (only if you dont want a task that has been
    #successful executed to be executed again)
    taskManager.parseResultsFile()
    
    #submit the tasks to execute
    taskManager.submitTasks()
