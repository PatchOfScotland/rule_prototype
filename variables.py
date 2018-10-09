import os
import time

number_of_resources = 3
# note that if this is set to zero then events start getting lost. This may be caused by the operating system overwriting events if they occur to close together, or may be something else entirely.
processing_time = 1
retry_duration = 1

time_stamp = str(time.time())
our_path = os.path.abspath('.') + '\\demo\\' + time_stamp
recipe_directory = '\\recipes'
pattern_directory = '\\patterns'
data_directory = '\\data'
initial_data_directory = '\\initial_data'
recipe_path = our_path + recipe_directory
pattern_path = our_path + pattern_directory
data_path = our_path + data_directory
initial_data_path = our_path + data_directory + initial_data_directory

recipe_extension = '.txt'
pattern_extension = '.txt.'
data_extension = '.txt'

# used to populate system with data for testing purposes
initial_recipes = [
    [
        "import time",
        "import variables",
        "input_file = open(self.input_file, 'r')",
        "data = input_file.read()",
        "input_file.close()",
        "data += 'processed by ' + self.name + '\\n'",
        "time.sleep(variables.processing_time)",
        "output_file = open(self.output_file, 'w')",
        "output_file.write(data)",
        "output_file.close()"
    ],
    [
        "import time",
        "import variables",
        "input_file = open(self.input_file, 'r')",
        "data = input_file.read()",
        "input_file.close()",
        "data += 'processed by ' + self.name + '\\n'",
        "time.sleep(variables.processing_time)",
        "output_file = open(self.output_file, 'w')",
        "output_file.write(data)",
        "output_file.close()"
    ],
    [
        "import time",
        "import variables",
        "input_file = open(self.input_file, 'r')",
        "data = input_file.read()",
        "input_file.close()",
        "data += 'processed by ' + self.name + '\\n'",
        "time.sleep(variables.processing_time)",
        "output_file = open(self.output_file, 'w')",
        "output_file.write(data)",
        "output_file.close()"
    ]
]

# used to populate system with data for testing purposes
initial_data = [
    'This is the initial state of the first data file.\n',
    'This is the initial state of the second data file.\n',
    'This is the initial state of the third data file.\n',
    'This is the initial state of the fourth data file.\n',
    'This is the initial state of the fifth data file.\n',
    'This is the initial state of the sixth data file.\n'
]

# used to populate system with data for testing purposes
initial_patterns = [
    {'recipe': 'recipe_0',
     'input_directory': initial_data_directory,
     'output_directory': '\\pattern_0_output',
     'variables': '{}'
     },
    {'recipe': 'recipe_1',
     'input_directory': initial_data_directory,
     'output_directory': '\\pattern_1_output',
     'variables': '{}'
     },
    {'recipe': 'recipe_2',
     'input_directory': '\\pattern_1_output',
     'output_directory': '\\pattern_2_output',
     'variables': '{}'
     }
]

actions = {
    1: 'Created',
    2: 'Deleted',
    3: 'Updated',
    4: 'Renamed from something',
    5: 'Renamed to something'
}
