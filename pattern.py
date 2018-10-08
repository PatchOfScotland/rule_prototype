
class Pattern:
    def __init__(self, recipe, input_directory, output_directory, variables):
        self.recipe = recipe
        self.variables = variables
        self.input_directory = input_directory
        self.output_directory = output_directory

    # gives unique pattern name. Is currently ugly as sin, possibly come back to this and improve
    def get_pattern_name(self):
        return str(self.recipe) + self.input_directory + self.output_directory + str(self.variables)


