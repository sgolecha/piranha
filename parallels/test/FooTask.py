from parallels import parallels 

"""
This is a example of a simple task
"""

class FooTask(parallels.BaseTask):
    def __init__(self, **kwargs):
        parallels.BaseTask.__init__(self, **kwargs)
    
    def execute(self, **kwargs):
        print("Executing FooTask")
        for k,v in kwargs.items():
            print("k: {0}, v: {1}".format(k, v))
        return kwargs
