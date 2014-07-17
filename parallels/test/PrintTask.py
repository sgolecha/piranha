import sys
from parallels import parallels 

sys.path.append("/Users/sgolecha/Projects/github/piranha/parallels/test")

class PrintTask(parallels.BaseTask):
    def __init__(self, **kwargs):
        parallels.BaseTask.__init__(self, **kwargs)
    
    def execute(self, **kwargs):
        print("Executing print task")
        for k,v in kwargs.items():
            print("k: {0}, v: {1}".format(k, v))
        return kwargs


if __name__ == "__main__":
    taskManager = parallels.TaskManager("./tasks.yaml", "./results.yaml")
    taskManager.parseTaskFile()
    taskManager.parseResultsFile()
    taskManager.submitTasks()
