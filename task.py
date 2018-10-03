from process import Process


class Task:
    def __init__(self, pattern, recipe, file):
        self.pattern = pattern
        self.recipe = recipe
        self.file = file

    def create_process(self):
        process = Process(self.recipe, self.pattern, self.file)
        return process

    # returns task identifier. This can be improved as currently is super crude, but hey, at least its unique
    def get_task_name(self):
        return str(self.file) + str(self.recipe) + str(self.pattern)
