
class Process:
    def __init__(self, recipe, pattern, file):
        self.processing = recipe.process_file
        self.input_file = pattern.input_directory + '\\' + file
        self.output_file = pattern.output_directory + '\\' + file
        self.name = recipe.name

    def process_file(self):
        print('@@@ Starting some processing...')
        print('@@@ name: ' + str(self.name))
        print('@@@ input_file: ' + str(self.input_file))
        print('@@@ output_file: ' + str(self.output_file))
        exec(self.processing)

