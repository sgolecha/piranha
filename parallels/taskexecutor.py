from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import os
import sys
import time
import imp
import yaml

class TaskStatus(object):
    INIT=0
    READY=1
    ENQUEUED=2
    FAILED=3
    SUCCESSFUL=4

def warning(*objs):
    print("WARNING: ", *objs, file=sys.stderr)


class BaseTask(object):
    """
    This a base task object. Every task is expected to inherit from this
    task object and implement the execute method
    """

    def __init__(self, **kwargs):
        self.status = TaskStatus.INIT
        self.name = kwargs['Name']
        self.args = []
        self.deps = []

        if 'Args' in kwargs:
            self.args = {'Args': kwargs['Args']}
        if 'Dependency' in kwargs:
            self.deps = kwargs['Dependency']

    def execute(self, **kwargs):
        """
        Every task should implement this method. The framework will pass the args 
        specified in the tasks.yaml file as a dict
        """
        pass

def execute(fn, **kwargs):
    taskName = kwargs['Name']
    result = {'Name': taskName, 'Result': TaskStatus.SUCCESSFUL}
    try:
        fn(Args=kwargs['Args'])
    except Exception as e:
        print("Task {0} threw Exception: {1}".format(taskName, e))

        result['Result'] = TaskStatus.FAILED
    
    return result    


class TaskManager(object):

    def __init__(self, taskFile, resultsFile):
        self.taskFile = taskFile
        self.resultsFile = resultsFile
        self.workers = 5
        self.graph = None
        self.tasks = []
        self.results = {}

    def findTask(self, taskName):
        try:
            taskFile, taskFilePath, taskDesc = imp.find_module(taskName)
            taskModule = imp.load_module(taskName, taskFile, taskFilePath, taskDesc)
            targetClass = getattr(taskModule, taskName)
        finally:
            if taskFile is not None:
                taskFile.close()

        return targetClass


    def parseTaskFile(self):
        print("parsing tasking file")
        with open(self.taskFile, 'r') as f:
            cfg = yaml.load(f)
            taskList = cfg['Tasks']
            for task in taskList:
                #targetClass = getattr(sys.modules[__name__], task['Name'])
                #targetClass = getattr(taskModule, task['Name'])
                targetClass = self.findTask(task['Name'])
                classInstance = targetClass(**task)
                self.tasks.append(classInstance)

    def parseResultsFile(self):
        if self.resultsFile is None:
            return

        print("parsing results file")
        try:
            with open(self.resultsFile, 'r') as f:
                resultDict = yaml.load(f)
                for taskName, taskStatus in resultDict.items():
                    if taskStatus['Result'] == TaskStatus.SUCCESSFUL:
                        try:
                            task = self.getTask(taskName)
                            print("updating status of {} from results".format(taskName))
                            task.status = TaskStatus.SUCCESSFUL
                        except Exception as e:
                            pass
        except FileNotFoundError:
            print("results file not found..assuming it does not exist")

    def submitTasks(self):
        print("submitting tasks to executor")
        futuresList = [] 
        with ProcessPoolExecutor(max_workers=self.workers) as executor:
            for t in self.tasks:
                if self.isRunnable(t):
                    print("enqueue task: {0}".format(t))
                    future = executor.submit(execute, getattr(t, 'execute'), Name=t.name, Args=t.args)
                    future.add_done_callback(self.onCompletionCb)
                    futuresList.append(future)

        if len(futuresList) == 0:
            print("done")
                
    def onCompletionCb(self, future):
        try:
            result = future.result()
            taskName = result['Name']
            now = time.time()
            self.getTask(taskName).status = result['Result']
            print("Job {0} complete - Result: {1}".format(taskName, result['Result']))
            self.results[taskName] = { 'Result': result['Result'], 'LastExecutionTime': time.time() }    
            if self.resultsFile is not None:
                with open(self.resultsFile, 'w') as f:
                    f.write(str(self.results))

            self.submitTasks()
        
        except Exception as e:
            print("Unexpected exception raised: {0}".format(e))
                
        
    def isRunnable(self, task):
        if task.status != TaskStatus.INIT:
            return False

        if len(task.deps) == 0:
            return True

        for depTaskName in task.deps:
            depTask = self.getTask(depTaskName)
            if depTask.status != TaskStatus.SUCCESSFUL:
                return False

        return True


    def getTask(self, taskName):
        for task in self.tasks:
            if task.name == taskName:
                return task
        raise Exception("Task not found")


if __name__ == "__main__":
    taskManager = TaskManager("test/tasks.yaml", None)
    taskManager.parseTaskFile()
    taskManager.parseResultsFile()
    taskManager.submitTasks()
