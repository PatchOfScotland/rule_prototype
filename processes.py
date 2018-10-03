import win32file
import win32con
import variables
from recipe import Recipe
from pattern import Pattern
from task import Task
from pycsp.parallel import *
from methods import *


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
    recursive_search(directory_to_monitor, to_handler)

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
                print('Seen an event (' + str(variables.actions.get(action)) + ') and sending it on to the handler: ' + file)
                path_details = get_path_details(directory_to_monitor + '\\' + file)
                to_handler(path_details)


@process
def data_handler(from_directory_monitor, to_task_generator):
    while True:
        data_input = from_directory_monitor()
#        print('Data handler received input: ' + data_input[1])
        to_task_generator(data_input)



@process
def pattern_handler(from_directory_monitor, to_task_generator):
    while True:
        pattern_input = from_directory_monitor()
#        print('Pattern handler received input: ' + pattern_input[1])
        with open(variables.our_path + pattern_input[0] + pattern_input[1]) as input_file:
            pattern = input_file.read()
        try:
            pattern_as_tuple = eval(pattern)
            recipe_name = pattern_as_tuple[0] + variables.recipe_extension
            pattern = Pattern(recipe_name, pattern_as_tuple[1], pattern_as_tuple[2])
            to_task_generator(pattern)
        except:
            print('Something went wrong with parsing the pattern')


@process
def recipe_handler(from_directory_monitor, to_task_generator):
    while True:
        recipe_input = from_directory_monitor()
#        print('Recipe handler received input: ' + recipe_input[1])
        complete_process = ''
        with open(variables.our_path + recipe_input[0] + recipe_input[1]) as input_file:
            for line in input_file:
                complete_process += line
        try:
            recipe = Recipe(recipe_input[0] + recipe_input[1], complete_process)
            to_task_generator(recipe)
        except:
            print('Something went wrong with parsing the recipe')


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
                # TODO re-run previous scheduled work with this new pattern
            else:
                patterns[message.get_pattern_name()] = message
                print('~~~ Pattern is new, has been added (' + str(len(patterns)) + ')')
                # TODO post facto apply to data already detected
        elif input_channel == from_recipe_handler:
            print('~~~ Task Generator was notified by the recipe handler about: ' + str(message))
#            print('message: ' + str(message))
#            print('message.name : ' + str(message.name))

            if message.name in recipes:
                recipes[message.name] = message
                print('~~~ Recipe was already present, has been updated')
                # TODO re-run previous scheduled work with this new recipe
            else:
                recipes[message.name] = message
                print('~~~ Recipe is new, has been added (' + str(len(recipes)) + ')')
                # TODO post facto apply to patterns already added but not run
        elif input_channel == from_data_handler:
            print('~~~ Task Generator was notified by the data handler about: ' + str(message))
            input_file = message[1]
            input_directory = message[0]
            # # if there is some intermediate directory
            # if '\\' in input_file:
            #     input_directory = input_directory + '\\' + input_file[:input_file.rfind('\\')]
            matching_patterns = get_matching_patterns(patterns, variables.our_path + input_directory)
            for pattern in matching_patterns:
                recipe = get_recipe(recipes, pattern)
                if recipe != None:
                    task = Task(pattern, recipe, input_file)
                    print('new task scheduled')
                    to_scheduler(task)
                    # TODO add to some list of all scheduled tasks
                # rule_monitor_to_scheduler(rule.task.create_process(file, path_to_watch, path_to_write))
                else:
                    print('Required recipe does not exist yet')
                    # TODO save this to some list to be run again if the recipe does turn up



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
            # TODO overwrite existing tasks in the buffer if they're for the same thing
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
            if len(buffer) == 0:
                for x in range(len(from_resources)):
                    pre_conditions[x] = False


@process
def resource(to_scheduler, from_scheduler):
    while True:
        to_scheduler(0)
        input_task = from_scheduler()
        if not os.path.exists(input_task.pattern.output_directory):
            os.makedirs(input_task.pattern.output_directory)
        input_process = input_task.create_process()
        input_process.process_file()
