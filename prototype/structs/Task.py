from prototype.structs.Process import Process
from prototype.global_methods.debugging import *


class Task:
    def __init__(self, pattern, recipe, task_file):
        self.pattern = pattern
        self.recipe = recipe
        self.file = task_file
        full_debug('New Task Created')
        full_debug('pattern: ' + str(self.pattern))
        full_debug('recipe: ' + str(self.recipe))
        full_debug('file: ' + str(self.file))

    def create_process(self):
        process = Process(self.recipe, self.pattern, self.file)
        return process

    def __eq__(self, other_task):
        if not isinstance(other_task, Task):
            return False

        if (self.file == other_task.file) and \
                (self.recipe.recipe == other_task.recipe.recipe) and \
                (self.pattern == other_task.pattern):
            return True
        return False
