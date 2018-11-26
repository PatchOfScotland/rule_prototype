from debugging import *


class Pattern:
    def __init__(
            self,
            recipes,
            input_directories,
            output_directory,
            file_type_filter,
            variables
    ):
        self.recipes = recipes
        self.variables = variables
        self.input_directories = input_directories
        self.output_directory = output_directory
        self.file_type_filter = file_type_filter
        full_debug('Creating new pattern')
        full_debug('Input directories:' + str(self.input_directories))
        full_debug('Output directory:' + str(self.output_directory))

    def __eq__(self, other):
        if not isinstance(other, Pattern):
            return False

        if (self.recipes == other.recipes) and \
            (self.input_directories == other.input_directories) and \
            (self.output_directory == other.output_directory) and \
            (self.file_type_filter == other.file_type_filter) and \
            (self.variables == other.variables):
            return True
        return False


    # gives unique pattern name. Is currently ugly as sin, possibly come back
    # to this and improve
    def get_pattern_name(self):
        return str(self.recipes) + \
               str(self.input_directories) + \
               self.output_directory + \
               str(self.variables)
