import os
import time

# number_of_resources = 3
processing_time = 1
# interruption_time = 10

time_stamp = time.time()
our_path = os.path.abspath('.') + '\\demo\\' + str(time_stamp)
recipe_directory = our_path + '\\recipes'
rule_directory = our_path + '\\rules'
data_directory = our_path + '\\data'

initial_recipes_as_json = [
    '{\n\t"name": "first_recipe",\n\t"processing": "some processing"\n}',
    '{\n\t"name": "second_recipe",\n\t"processing": "some processing"\n}',
    '{\n\t"name": "third_recipe",\n\t"processing": "some processing"\n}'
]

initial_data = [
    'This is the initial state of the first data file.\n',
    'This is the initial state of the second data file.\n',
    'This is the initial state of the third data file.\n',
    'This is the initial state of the fourth data file.\n',
    'This is the initial state of the fifth data file.\n',
    'This is the initial state of the sixth data file.\n'
]

actions = {
    1: 'Created',
    2: 'Deleted',
    3: 'Updated',
    4: 'Renamed from something',
    5: 'Renamed to something'
}

