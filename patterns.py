
class Pattern:
    def __init__(self, recipe, input_directory, output_directory):
        self.recipe = recipe
        self.input_directory = input_directory
        self.output_directory = output_directory

    def get_pattern_name(self):
        return str(self.recipe) + self.input_directory + self.output_directory
