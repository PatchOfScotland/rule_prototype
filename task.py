from process import Process


class Task:
    def __init__(self, pattern, recipe, file):
        self.pattern = pattern
        self.recipe = recipe
        self.file = file

    def create_process(self):
        process = Process(self.recipe, self.pattern, self.file)
        return process
