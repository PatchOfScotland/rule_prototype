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

# These may want to be changed later to be a more expandable system
initial_file_descriptor = 'Old'
new_file_event_descriptor = 'New'
all_files_descriptor = 'All'
pattern_events = [
    initial_file_descriptor,
    new_file_event_descriptor
]

# used to populate system with data for testing purposes
initial_recipes = [
    [
        "import time",
        "input_file = open(self.input_file, 'r')",
        "data = input_file.read()",
        "input_file.close()",
        "data += 'processed by ' + self.name + '\\n'",
        "time.sleep(processing_time)",
        "output_file = open(self.output_file, 'w')",
        "output_file.write(data)",
        "output_file.close()"
    ],
    [
        "import time",
        "input_file = open(self.input_file, 'r')",
        "data = input_file.read()",
        "input_file.close()",
        "data += 'processed by ' + self.name + '\\n'",
        "time.sleep(processing_time)",
        "output_file = open(self.output_file, 'w')",
        "output_file.write(data)",
        "output_file.close()"
    ],
    [
        "import time",
        "input_file = open(self.input_file, 'r')",
        "data = input_file.read()",
        "input_file.close()",
        "data += 'processed by ' + self.name + '\\n'",
        "data += str(var_a) + ', ' + str(var_b) + ', ' + str(var_c) + ', ' + str(var_d) +'\\n'",
        "time.sleep(processing_time)",
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
     'type_filter': [
         data_extension
        ],
     'event_filter': all_files_descriptor,
     'variables': {
         'processing_time': processing_time
        }
     },
    {'recipe': 'recipe_1',
     'input_directory': initial_data_directory,
     'output_directory': '\\pattern_1_output',
     'type_filter': [
         data_extension
        ],
     'event_filter': initial_file_descriptor,
     'variables': {
         'processing_time': processing_time
        }
     },
    {'recipe': 'recipe_2',
     'input_directory': '\\pattern_1_output',
     'output_directory': '\\pattern_2_output',
     'type_filter': [
         data_extension
        ],
     'event_filter': new_file_event_descriptor,
     'variables': {
         'processing_time': processing_time,
         'var_a': 867,
         'var_b': 1444,
         'var_c': 1936,
         'var_d': 2100
        }
     }
]

actions = {
    1: 'Created',
    2: 'Deleted',
    3: 'Updated',
    4: 'Renamed from something',
    5: 'Renamed to something'
}
