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

first_recipe_as_json = '{\n\t"name": "first_recipe",\n\t"processing": "some processing"\n}'
second_recipe_as_json = '{\n\t"name": "second_recipe",\n\t"processing": "some processing"\n}'
third_recipe_as_json = '{\n\t"name": "third_recipe",\n\t"processing": "some processing"\n}'

actions = {
    1: 'Created',
    2: 'Deleted',
    3: 'Updated',
    4: 'Renamed from something',
    5: 'Renamed to something'
}

