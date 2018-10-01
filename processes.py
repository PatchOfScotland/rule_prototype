import win32file
import win32con
import os
import variables
from recipes import Recipe
from patterns import Pattern
from pycsp.parallel import *


# @process
# def rule_changer(to_rule_monitor):
#     time.sleep(variables.interruption_time)
#     print('Rule changer sending interruption')
#     to_rule_monitor(0)
#     print('Rule changer sent interruption')
#
#
# @process
# def resource(to_scheduler, from_scheduler):
#     while True:
#         to_scheduler(0)
#         input_process = from_scheduler()
#         input_process.process_file()
#
#
# @process
# def scheduler(from_monitor, from_resources, to_resources):
#     buffer = []
#     pre_conditions = [False] * len(from_resources)
#     # This is for the monitor, should always be True
#     pre_conditions.append(True)
#     input_guards = []
#     for from_resource in from_resources:
#         input_guards.append(InputGuard(from_resource))
#     input_guards.append(InputGuard(from_monitor))
#     while True:
#         pre_conditioned = []
#         for i, guard in enumerate(input_guards):
#             if pre_conditions[i]:
#                 pre_conditioned.append(guard)
#         channel_index, message = PriSelect(
#             pre_conditioned
#         )
#         if channel_index == from_monitor:
#             replace_previous_entry = False
#             # If there is already a scheduled process identical to this, then replace that one
#             for index, element in enumerate(buffer):
#                 if element.get_process_name() == message.get_process_name():
#                     buffer[index] = message
#                     replace_previous_entry = True
#             if not replace_previous_entry:
#                 buffer.append(message)
#             for x in range(len(from_resources)):
#                 pre_conditions[x] = True
#         # Input message came from a resource looking for a process. Can ignore empty input
#         else:
#             i = -1
#             for a in range(len(from_resources)):
#                 if from_resources[a] == channel_index:
#                     i = a
#
#             to_resources[i](buffer[0])
#             del buffer[0]
#             if len(buffer) == 0:
#                 for x in range(len(from_resources)):
#                     pre_conditions[x] = False
#


@process
def directory_monitor(directory_to_monitor, to_handler_processor):

    print('monitoring :' + directory_to_monitor)

    file_list_directory = 0x0001

    handle = win32file.CreateFile(
        directory_to_monitor,
        file_list_directory,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )

    for file in os.listdir(directory_to_monitor):
        print('Discovered initial file and sending it on to handler: ' + file)
        to_handler_processor((directory_to_monitor, file))

    while True:
        results = win32file.ReadDirectoryChangesW(
            handle,
            1024,
            True,
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
            win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
            win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
            win32con.FILE_NOTIFY_CHANGE_SIZE |
            win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
            win32con.FILE_NOTIFY_CHANGE_SECURITY,
            None,
            None
        )
        for action, file in results:
            if action in variables.actions:
                print('Seen an event and sending it on to the handler: ' + file)
                to_handler_processor((directory_to_monitor, file))
#                rule_monitor_to_scheduler(rule.task.create_process(file, path_to_watch, path_to_write))


@process
def data_handler(from_directory_monitor, to_scheduler):
    while True:
        data_input = from_directory_monitor()
        print('Data handler received input: ' + data_input[1])


@process
def pattern_handler(from_directory_monitor, to_scheduler):
    all_patterns = {}
    while True:
        pattern_input = from_directory_monitor()
        print('Pattern handler received input: ' + pattern_input[1])
        with open(pattern_input[0] + '\\' + pattern_input[1]) as input_file:
            pattern = input_file.read()
        try:
            pattern_as_tuple = eval(pattern)
            pattern = Pattern(pattern_as_tuple[0], pattern_as_tuple[1], pattern_as_tuple[2])
            if pattern.get_pattern_name() not in all_patterns:
                print('Creating new pattern')
                all_patterns[pattern.get_pattern_name()] = pattern
            else:
                print('Replacing existing pattern')
                all_patterns[pattern.get_pattern_name()] = pattern
        except:
            print('Something went wrong with parsing the pattern')


@process
def recipe_handler(from_directory_monitor, to_scheduler):
    all_recipes = {}
    while True:
        recipe_input = from_directory_monitor()
        print('Recipe handler received input: ' + recipe_input[1])
        complete_process = ''
        with open(recipe_input[0] + '\\' + recipe_input[1]) as input_file:
            for line in input_file:
                complete_process += line
        try:
            recipe = Recipe(recipe_input, complete_process)
            if recipe.name not in all_recipes:
                print('Creating new recipe')
                all_recipes[recipe.name] = recipe
            else:
                print('Replacing existing recipe')
                all_recipes[recipe.name] = recipe
        except:
            print('Something went wrong with parsing the recipe')


# TODO take input from the handlers and maintain a dictionary of patterns and recipes, and to schedule new processes with data once they are added or updated. The dictionaries in the relevant
# handlers should also be removed as otherwise its just replicating data. Possibly the handlers in their entirety could be removed as I'm not sure if they're adding anything individually.
@process
def scheduler(from_data_handler, from_pattern_handler, from_recipe_handler):
    pass


#
# @process
# def rule_monitor(
#         rule,
#         repeat_on_rule_change,
#         repeat_on_data_change,
#         apply_post_facto,
#         rule_monitor_to_scheduler,
#         changer_to_monitor):
#     actions = {
#         1: 'Created',
#         2: 'Deleted',
#         3: 'Updated',
#         4: 'Renamed from something',
#         5: 'Renamed to something'
#     }
#
#     file_list_directory = 0x0001
#
#     our_path = os.path.abspath('.')
#
#     directory_to_watch = rule.input_directory
#     path_to_watch = our_path + directory_to_watch
#     print("Watching: " + path_to_watch)
#
#     directory_to_write = rule.output_directory
#     path_to_write = our_path + directory_to_write
#     print("Writing to: " + path_to_write)
#
#     if not os.path.exists(path_to_write):
#         os.makedirs(path_to_write)
#
#     handle = win32file.CreateFile(
#         path_to_watch,
#         file_list_directory,
#         win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
#         None,
#         win32con.OPEN_EXISTING,
#         win32con.FILE_FLAG_BACKUP_SEMANTICS,
#         None
#     )
#
#     if apply_post_facto:
#         for file in os.listdir(path_to_watch):
#             print('Discovered ' + file)
#             rule_monitor_to_scheduler(rule.task.create_process(file, path_to_watch, path_to_write))
#
#     while True:
#         results = win32file.ReadDirectoryChangesW(
#             handle,
#             1024,
#             True,
#             win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
#             win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
#             win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
#             win32con.FILE_NOTIFY_CHANGE_SIZE |
#             win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
#             win32con.FILE_NOTIFY_CHANGE_SECURITY,
#             None,
#             None
#         )
#         for action, file in results:
#             if actions.get(action) == 'Created' or \
#                     actions.get(action) == 'Renamed to something' or \
#                     (actions.get(action) == 'Updated' and repeat_on_data_change) or \
#                     (actions.get(action) == 'Renamed from something' and repeat_on_data_change):
#                 print('Seen an event and scheduling ' + file)
#                 rule_monitor_to_scheduler(rule.task.create_process(file, path_to_watch, path_to_write))
#
