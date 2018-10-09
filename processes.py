import win32file
import win32con
import time
import ast
import system_variables
from recipe import Recipe
from pattern import Pattern
from task import Task
from pycsp.parallel import *
from methods import *

# In the unlikely occurrence of multiple events at once, only a single one will be detected. This may be a problem unique to win32, or may also be the case in other operating systems
@process
def directory_monitor(directory_to_monitor, to_handler):

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

    # Get initial data sets
    initial_data = []
    recursive_search_to_list(directory_to_monitor, initial_data)
    for data in initial_data:
        to_handler((data, system_variables.initial_file_descriptor))

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
            print('Seen something (action: ' + str(action) + ') (file: ' + str(file))
            if action in system_variables.actions:
                print('Seen an event (' + str(system_variables.actions.get(action)) + ') and sending it on to the handler: ' + file)
                path_details = get_path_details(directory_to_monitor + '\\' + file)
                to_handler((path_details, system_variables.new_file_event_descriptor))


@process
def data_handler(from_directory_monitor, to_task_generator):
    while True:
        message = from_directory_monitor()
        data_input = message[0]
        print('Data handler received input: ' + data_input[0] + '\\' + data_input[1])
        to_task_generator(message)


@process
def pattern_handler(from_directory_monitor, to_task_generator):
    while True:
        message = from_directory_monitor()
        # can ignore event creation descriptor as will always update a pattern
        pattern_input = message[0]
        print('Pattern handler received input: ' + pattern_input[1])
#        print('Complete pattern_input: ' + str(pattern_input))
#        print('pattern_input[0]: ' + str(pattern_input[0]))
#        print('pattern_input[1]: ' + str(pattern_input[1]))
#        print('our_path: ' + variables.our_path)
        while True:
            try:
                with open(system_variables.pattern_path + pattern_input[0] + pattern_input[1]) as input_file:
#                    print('opened: ' + variables.our_path + pattern_input[0] + pattern_input[1])
                    raw_pattern = input_file.read()
                input_file.close()
                break
            except PermissionError:
                print('Permission denied to open pattern file, will try again')
                time.sleep(system_variables.retry_duration)
        pattern_dictionary = ast.literal_eval(raw_pattern)
        print(type(pattern_dictionary))
        print(str(pattern_dictionary))
        print('keys: ' + str(pattern_dictionary.keys()))
        recipe = pattern_dictionary['recipe'] + system_variables.recipe_extension
        print('recipe_name: ' + recipe)
        input_directory = system_variables.data_path + pattern_dictionary['input_directory']
        print('input_directory: ' + input_directory)
        output_directory = system_variables.data_path + pattern_dictionary['output_directory']
        print('output_directory: ' + output_directory)
        file_type_filter = pattern_dictionary['type_filter']
        print('type_filter: ' + str(file_type_filter))
        event_filter = pattern_dictionary['event_filter']
        print('event_filter: ' + str(event_filter))
        recipe_variables = pattern_dictionary['variables']
        print('recipe_variables: ' + str(system_variables))
        pattern = Pattern(recipe, input_directory, output_directory, file_type_filter, event_filter, recipe_variables)
        to_task_generator(pattern)


@process
def recipe_handler(from_directory_monitor, to_task_generator):
    while True:
        message = from_directory_monitor()
        # can ignore event creation descriptor as will always update a recipe
        recipe_input = message[0]
        print('Recipe handler received input: ' + recipe_input[1])
        while True:
            try:
                complete_process = ''
                with open(system_variables.recipe_path + recipe_input[0] + recipe_input[1]) as input_file:
                    for line in input_file:
                        complete_process += line
                input_file.close()
                break
            except PermissionError:
                print('Permission denied to open recipe file, will try again')
                time.sleep(system_variables.retry_duration)
        recipe = Recipe(recipe_input[0] + recipe_input[1], complete_process)
        to_task_generator(recipe)


@process
def task_generator(from_data_handler, from_pattern_handler, from_recipe_handler, to_scheduler):
    recipes = {}
    patterns = {}
    while True:
        input_channel, message = PriSelect(
            InputGuard(from_pattern_handler),
            InputGuard(from_recipe_handler),
            InputGuard(from_data_handler)
        )

        if input_channel == from_pattern_handler:
            print('~~~ Task Generator was notified by the pattern handler about: ' + str(message))
            if message.get_pattern_name() in patterns:
                patterns[message.get_pattern_name()] = message
                print('~~~ Pattern was already present, has been updated')
            else:
                patterns[message.get_pattern_name()] = message
                print('~~~ Pattern is new, has been added (' + str(len(patterns)) + ')')
            # print('pattern: ' + str(message))
            # print('pattern.recipe: ' + str(message.recipe))
            # print('pattern.input_directory: ' + str(message.input_directory))
            # print('pattern.output_directory: ' + str(message.output_directory))
            input_directory_contents = []
#            print('input_directory: ' + str(message.input_directory))
#            print('output_directory: ' + str(message.output_directory))
            recursive_search_to_list(message.input_directory, input_directory_contents)
            recipe = get_recipe(recipes, message)
#            print('input_directory_contents length: ' + str(len(input_directory_contents)))
#            print('recipe: ' + str(recipe))
            if recipe is not None:
                if len(input_directory_contents) == 0:
                    print('Nothing in ' + message.input_directory)
                for file in input_directory_contents:
                    if file_is_in_filter(message.file_type_filter, file[1]):
                        task = Task(message, recipe, file[1])
                        print('new task sent to scheduler')
                        to_scheduler(task)
            else:
                print('Required recipe does not exist yet (I)')

        elif input_channel == from_recipe_handler:
            print('~~~ Task Generator was notified by the recipe handler about: ' + str(message))
#            print('message: ' + str(message))
            print('message.name : ' + str(message.name))
            if message.name in recipes:
                recipes[message.name] = message
                print('~~~ Recipe was already present, has been updated')
            else:
                recipes[message.name] = message
                print('~~~ Recipe is new, has been added (' + str(len(recipes)) + ')')
            matched_patterns = get_matching_patterns_by_recipe(patterns, message)
            for pattern in matched_patterns:
                input_directory_contents = []
                recursive_search_to_list(pattern.input_directory, input_directory_contents)
                for file in input_directory_contents:
                    if file_is_in_filter(pattern.file_type_filter, file[1]):
                        task = Task(pattern, message, file[1])
#                        print('new task sent to scheduler')
                        to_scheduler(task)

        elif input_channel == from_data_handler:
            print('~~~ Task Generator was notified by the data handler about: ' + str(message))
            data = message[0]
            event = message[1]
            input_file = data[1]
            input_directory = data[0]
            # # if there is some intermediate directory
            # if '\\' in input_file:
            #     input_directory = input_directory + '\\' + input_file[:input_file.rfind('\\')]
            matching_patterns = get_matching_patterns_by_input(patterns, system_variables.data_path + input_directory)
            for pattern in matching_patterns:
                recipe = get_recipe(recipes, pattern)
                if recipe is not None:
                    if file_is_in_filter(pattern.file_type_filter, input_file):
                        if event_is_in_filter(pattern.event_filter, event):
                            task = Task(pattern, recipe, input_file)
#                            print('new task sent to scheduler')
                            to_scheduler(task)
                else:
                    print('Required recipe does not exist yet (II)')


@process
def scheduler(from_task_generator, from_resources, to_resources):
    buffer = []
    pre_conditions = [False] * len(from_resources)
    # This is for the monitor, should always be True
    pre_conditions.append(True)
    input_guards = []
    for from_resource in from_resources:
        input_guards.append(InputGuard(from_resource))
    input_guards.append(InputGuard(from_task_generator))
    while True:
        pre_conditioned = []
        for i, guard in enumerate(input_guards):
            if pre_conditions[i]:
                pre_conditioned.append(guard)
        channel_index, message = PriSelect(
            pre_conditioned
        )
        if channel_index == from_task_generator:
            task_match = False
            for index, buffered in enumerate(buffer):
                if buffered.get_task_name() == message.get_task_name():
                    buffer[index] = message
                    print('old task updated (' + str(len(buffer)) + ')')
                    task_match = True
                    break
            if not task_match:
                print('new task scheduled (' + str(len(buffer)) + ')')
                buffer.append(message)
            for x in range(len(from_resources)):
                pre_conditions[x] = True
        # Input message came from a resource looking for a process. Can ignore empty input
        else:
            i = -1
            for a in range(len(from_resources)):
                if from_resources[a] == channel_index:
                    i = a
            to_resources[i](buffer[0])
            del buffer[0]
            print('task processed (' + str(len(buffer)) + ')')
            if len(buffer) == 0:
                for x in range(len(from_resources)):
                    pre_conditions[x] = False


@process
def resource(to_scheduler, from_scheduler):
    while True:
        to_scheduler(0)
        input_task = from_scheduler()
#        print('Resource got new task: ' + str(input_task))
        if not os.path.exists(input_task.pattern.output_directory):
            os.makedirs(input_task.pattern.output_directory)
        input_process = input_task.create_process()
#        print('Resource created new process: ' + str(input_process))
        input_process.process_file()
