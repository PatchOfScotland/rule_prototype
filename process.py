
class Process:
    def __init__(self, recipe, pattern, file):
        self.processing = recipe.process_file
        self.input_file = pattern.input_directory + '\\' + file
        self.output_file = pattern.output_directory
        self.name = recipe.name

    def process_file(self):
        import time
        import variables
        exec(self.processing)

