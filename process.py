from methods import full_debug


class Process:
    def __init__(self, recipe, pattern, file):
        self.processing = recipe.process_file
        full_debug('input_file: ' + str(pattern.input_directory))
        full_debug('file: ' + str(file))
        self.input_file = pattern.input_directory + '\\' + file
        self.output_file = pattern.output_directory + '\\' + file
        self.name = recipe.name
        self.variables = ''
        for variable in pattern.variables:
            full_debug('variable: ' + str(variable))
            full_debug('value: ' + str(pattern.variables[variable]))
            variable_declaration_as_string = str(variable) + ' = ' + str(pattern.variables[variable]) + '\n'
            self.variables += variable_declaration_as_string

    def process_file(self):
        full_debug('@@@ Starting some processing...')
        full_debug('@@@ name: ' + str(self.name))
        full_debug('@@@ input_file: ' + str(self.input_file))
        full_debug('@@@ output_file: ' + str(self.output_file))
        exec(self.variables + self.processing)

