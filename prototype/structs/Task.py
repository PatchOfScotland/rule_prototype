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

    # returns task identifier. This can be improved as currently it is super
    # crude, but hey, at least its unique
    def get_task_name(self):
        return str(self.file) + str(self.recipe) + str(self.pattern)
