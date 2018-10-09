
class Process:
    def __init__(self, recipe, pattern, file):
        self.processing = recipe.process_file
#        print('input_file: ' + str(pattern.input_directory))
#        print('file: ' + str(file))
        self.input_file = pattern.input_directory + '\\' + file
        self.output_file = pattern.output_directory + '\\' + file
        self.name = recipe.name
        self.variables = ''
        for variable in pattern.variables:
            print('variable: ' + str(variable))
            print('value: ' + str(pattern.variables[variable]))
            variable_declaration_as_string = str(variable) + ' = ' + str(pattern.variables[variable]) + '\n'
            self.variables += variable_declaration_as_string

    def process_file(self):
#        print('@@@ Starting some processing...')
#        print('@@@ name: ' + str(self.name))
#        print('@@@ input_file: ' + str(self.input_file))
#        print('@@@ output_file: ' + str(self.output_file))
        exec(self.variables + self.processing)

