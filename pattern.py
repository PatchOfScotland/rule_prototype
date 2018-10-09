
class Pattern:
    def __init__(self, recipe, input_directory, output_directory, file_type_filter, event_filter, variables):
        self.recipe = recipe
        self.variables = variables
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.file_type_filter = file_type_filter
        self.event_filter = event_filter

    # gives unique pattern name. Is currently ugly as sin, possibly come back to this and improve
    def get_pattern_name(self):
        return str(self.recipe) + self.input_directory + self.output_directory + str(self.variables)


