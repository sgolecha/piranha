parallels/taskexecutor is module that helps execute multiple tasks parallely. One can create dependencies between tasks, such that the dependent task will only be executed after all the dependencies are satisfied (i.e. all the dependencies are successfully executed). All the tasks are executed in a separate process.  

The module use use two configuration files - tasks.yaml and results.yaml. The tasks.yaml file specifies the tasks, its dependencies and any args that the task needs. The results.yaml contains the status of the task, the last execution time etc. Note that if you run the taskexecutor multiple times, a task that has successfully run previsouly will not be executed again.

For an example, see the test directory.
