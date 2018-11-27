from prototype.global_methods.debugging import *


class Process:
    def __init__(self, recipe, pattern, process_file):
        self.processing = recipe.recipe
        self.input_file = process_file
        file_name = process_file[process_file.rfind('/'):]
        self.input_directory = process_file.replace(file_name, '')
        self.output_directory = pattern.output_directory
        self.output_file = \
            pattern.output_directory + process_file[process_file.rfind('/'):]
        self.name = recipe.name
        self.variables = ''
        full_debug('input_file: ' + str(pattern.input_directories))
        full_debug('input_directory: ' + str(self.input_directory))
        full_debug('file: ' + str(process_file))

        for variable in pattern.variables:
            full_debug('variable: ' + str(variable))
            full_debug('value: ' + str(pattern.variables[variable]))
            variable_declaration_as_string = \
                str(variable) + ' = ' + str(pattern.variables[variable]) + '\n'
            self.variables += variable_declaration_as_string

    def process_file(self):
        full_debug('@@@ Starting some processing...')
        full_debug('@@@ input_file: ' + str(self.input_file))
        full_debug('@@@ output_file: ' + str(self.output_file))
        exec(self.variables + self.processing)
