import os
import time

# number_of_resources = 3
processing_time = 1
# interruption_time = 10

time_stamp = time.time()
our_path = os.path.abspath('.') + '\\demo\\' + str(time_stamp)
recipe_directory = our_path + '\\recipes'
pattern_directory = our_path + '\\patterns'
data_directory = our_path + '\\data'
initial_data_directory = data_directory + '\\initial_data'

initial_recipes = [
    [
        "input_file = open(self.input_file, 'r')",
        "data = input_file.read()",
        "input_file.close()",
        "data += 'processed by ' + self.name + '\\n'",
        "time.sleep(variables.processing_time)",
        "output_file = open(self.output_file, 'w')",
        "output_file.write(data)",
        "output_file.close()",
    ],
    [
        "input_file = open(self.input_file, 'r')",
        "data = input_file.read()",
        "input_file.close()",
        "data += 'processed by ' + self.name + '\\n'",
        "time.sleep(variables.processing_time)",
        "output_file = open(self.output_file, 'w')",
        "output_file.write(data)",
        "output_file.close()",
    ],
    [
        "input_file = open(self.input_file, 'r')",
        "data = input_file.read()",
        "input_file.close()",
        "data += 'processed by ' + self.name + '\\n'",
        "time.sleep(variables.processing_time)",
        "output_file = open(self.output_file, 'w')",
        "output_file.write(data)",
        "output_file.close()",
    ]
]

initial_data = [
    'This is the initial state of the first data file.\n',
    'This is the initial state of the second data file.\n',
    'This is the initial state of the third data file.\n',
    'This is the initial state of the fourth data file.\n',
    'This is the initial state of the fifth data file.\n',
    'This is the initial state of the sixth data file.\n'
]

initial_patterns = [
    ('recipe_0', initial_data_directory, data_directory + '\\pattern_1_output'),
    ('recipe_1', initial_data_directory, data_directory + '\\pattern_2_output'),
    ('recipe_2', data_directory + '\\pattern_2_output', data_directory + '\\pattern_3_output'),
]

actions = {
    1: 'Created',
    2: 'Deleted',
    3: 'Updated',
    4: 'Renamed from something',
    5: 'Renamed to something'
}

