import time
import os

NONE = 0
PARTIAL = 1
FULL = 2

debug_mode = FULL

number_of_resources = 3
processing_time = 1
retry_duration = 1

recipe_flag = 'recipe'
data_flag = 'data'
pattern_flag = 'pattern'

time_stamp = str(time.time())
our_path = os.path.abspath('.') + '/demo/' + time_stamp
recipe_directory = '/' + recipe_flag + 's'
pattern_directory = '/' + pattern_flag + 's'
data_directory = '/' + data_flag
initial_data_directory = '/initial_data'
recipe_path = our_path + recipe_directory
pattern_path = our_path + pattern_directory
data_path = our_path + data_directory
initial_data_path = our_path + data_directory + initial_data_directory

recipe_extension = '.txt'
pattern_extension = '.txt.'
data_extension = '.txt'

initial_file_descriptor = "InitialFile"
