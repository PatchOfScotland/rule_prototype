from watchdog.events import PatternMatchingEventHandler
from prototype.global_methods.global_methods import recursive_search_to_list
from prototype.structs.EdssEvent import *
from prototype.global_methods.debugging import *
from prototype.structs.Recipe import Recipe
from prototype.structs.Pattern import Pattern
from prototype.structs.Task import Task
from prototype.variables import system_variables
import ast


class EventMonitor(PatternMatchingEventHandler):
    def __init__(
            self,
            to_server_stdin,
            patterns=None,
            ignore_patterns=None,
            ignore_directories=True,
            case_sensitive=False
    ):
        full_debug('STARTING NEW EVENT MONITOR')
        self.to_server_stdin = to_server_stdin
        self.all_patterns = []
        self.all_recipes = []
        PatternMatchingEventHandler.__init__(
            self,
            patterns,
            ignore_patterns,
            ignore_directories,
            case_sensitive
        )

    def process_event(self, edss_event):
        full_debug('file name: ' + edss_event.file_name)
        if edss_event is not None and edss_event.file_name[1] != '.':
            partial_debug("file: " + edss_event.file_name)
            partial_debug("intermediates: " +
                          edss_event.intermediate_directories)
            partial_debug("edss: " + edss_event.edss_event_type)
            partial_debug("system: " + edss_event.system_event_type)

            # new recipe detected
            if edss_event.edss_event_type == recipe_directory:

                full_debug("Event handler found newly created recipe")
                complete_process = ''
                with open(edss_event.path) as input_file:
                    for line in input_file:
                        complete_process += line
                input_file.close()
                recipe = Recipe(edss_event.intermediate_directories +
                                edss_event.file_name,
                                complete_process)

                # check we don't have a duplicate recipe. If we do then replace
                # it with the updated one. Note that recipes may be exactly the
                # same and are deemed to be unique only based on their location
                removable_recipe = None
                for established_recipe in self.all_recipes:
                    if recipe.name == established_recipe.name:
                        removable_recipe = established_recipe
                if removable_recipe is not None:
                    self.all_recipes.remove(removable_recipe)

                self.all_recipes.append(recipe)
                full_debug('Adding recipe: ' + recipe.name)
                full_debug('Now have ' + str(len(self.all_recipes)) +
                           ' recipes')

                # check to see if there are any patterns matching which need
                # this recipe.
                full_debug('Checking patterns...')
                matching_patterns = []
                for pattern in self.all_patterns:
                    full_debug('inspecting ' + str(pattern.recipes) + ' for ' +
                               recipe.name)
                    if recipe.name in pattern.recipes:
                        matching_patterns.append(pattern)

                for pattern in matching_patterns:
                    full_debug('found pattern')
                    complete_recipe = ''
                    complete_name = ''
                    got_all_recipes = True
                    for pattern_recipe in pattern.recipes:
                        got_this_recipe = False
                        for recipe in self.all_recipes:
                            if recipe.name == pattern_recipe:
                                complete_recipe += recipe.recipe
                                complete_name += recipe.name + '_'
                                got_this_recipe = True
                        if not got_this_recipe:
                            got_all_recipes = False
                    # if we've got all the required recipes then check
                    # there is some data
                    if complete_recipe != '' and got_all_recipes:
                        completed_recipe = Recipe(
                            complete_name[:-1],
                            complete_recipe
                        )
                        initial_data = []
                        for input_directory in pattern.input_directories:
                            recursive_search_to_list(input_directory,
                                                     initial_data)
                        for data in initial_data:
                            task = Task(
                                pattern,
                                completed_recipe,
                                data
                            )
                            self.to_server_stdin(task)

            # new patterns detected
            if edss_event.edss_event_type == pattern_directory:

                full_debug("Event handler found newly created pattern")
                with open(edss_event.path) as input_file:
                    raw_pattern = input_file.read()
                input_file.close()
                pattern_dictionary = ast.literal_eval(raw_pattern)

                recipes = []
                for recipe in pattern_dictionary['recipes']:
                    recipes.append(
                        '/' + recipe + system_variables.recipe_extension
                    )
                full_debug("identified recipes: " + str(recipes))

                input_directories = []
                for input_directory in pattern_dictionary['input_directories']:
                    input_directories.append(system_variables.data_path +
                                             input_directory)

                output_directory = \
                    system_variables.data_path + \
                    pattern_dictionary['output_directory']

                file_type_filters = []
                for file_type_filter in pattern_dictionary['type_filter']:
                    file_type_filters.append(file_type_filter)

                recipe_variables = pattern_dictionary['variables']

                pattern = Pattern(
                    recipes,
                    input_directories,
                    output_directory,
                    file_type_filters,
                    recipe_variables)

                # check we don't have a duplicate pattern. If we do then we can
                # ignore this new one. Note that patterns cannot match the same
                # directories to the same recipe as this is just duplication
                matching_pattern = False
                for defined_pattern in self.all_patterns:
                    if defined_pattern == pattern:
                        matching_pattern = True
                if matching_pattern:
                    partial_debug("Pattern already exists, ignoring this one")
                else:
                    self.all_patterns.append(pattern)

                    full_debug("There are " + str(len(self.all_patterns)) +
                               " patterns")

                    # check to see if we've got all the necessary recipes
                    complete_recipe = ''
                    complete_name = ''
                    got_all_recipies = True
                    for pattern_recipe in pattern.recipes:
                        got_this_recipe = False
                        for recipe in self.all_recipes:
                            if recipe.name == pattern_recipe:
                                complete_recipe += recipe.recipe
                                complete_name += recipe.name + '_'
                                got_this_recipe = True
                        if not got_this_recipe:
                            got_all_recipies = False

                    # if we've got the recipes then check for pre-existing data
                    # files
                    if complete_recipe != '' and got_all_recipies:
                        initial_data = []
                        for input_directory in pattern.input_directories:
                            recursive_search_to_list(
                                input_directory,
                                initial_data
                            )
                        for data in initial_data:
                            completed_recipe = Recipe(
                                complete_name[:-1],
                                complete_recipe
                            )
                            task = Task(
                                pattern,
                                completed_recipe,
                                data
                            )
                            self.to_server_stdin(task)

            # new data detected
            if edss_event.edss_event_type == data_directory:
                full_debug("Event handler found newly created data")

                full_debug('Checking for matching patterns')
                # check to see if there are any patterns matching this data
                # directory
                matching_patterns = []
                for pattern in self.all_patterns:
                    for input_directory in pattern.input_directories:
                        full_directory = system_variables.data_path + \
                                         edss_event.intermediate_directories
                        full_debug('Inspecting ' +
                                   input_directory +
                                   ' against ' +
                                   full_directory)
                        if input_directory == full_directory:
                            matching_patterns.append(pattern)
                full_debug('Found ' + str(len(matching_patterns))
                           + ' matching patterns')

                # for each matching patterns check to see if we've got all the
                # required recipes
                for pattern in matching_patterns:
                    complete_recipe = ''
                    complete_name = ''
                    got_all_recipies = True
                    for pattern_recipe in pattern.recipes:
                        got_this_recipe = False
                        for recipe in self.all_recipes:
                            if recipe.name == pattern_recipe:
                                complete_recipe += recipe.recipe
                                complete_name += recipe.name + '_'
                                got_this_recipe = True
                        if not got_this_recipe:
                            got_all_recipies = False

                    # if we've got all the recipes then create a new task
                    if complete_recipe != '' and got_all_recipies:
                        completed_recipe = Recipe(
                            complete_name[:-1],
                            complete_recipe
                        )
                        task = Task(
                            pattern,
                            completed_recipe,
                            edss_event.path
                        )
                        self.to_server_stdin(task)
        else:
            full_debug("ignoring event")

    def on_moved(self, event):
        """Handle modified rule file"""
        partial_debug("Moved " + str(event))
        edss_event = get_event(
            event
        )
        self.process_event(edss_event)

    # This method probably isn't needed as any file changes should be covered
    # by the other functions. Keep this around just in case though
#     def on_any_event(self, event):
#         """Handle modified rule file"""
#         partial_debug("Any Event " + str(event))

    def on_modified(self, event):
        """Handle modified rule file"""
        partial_debug("Modified " + str(event))
        edss_event = get_event(
            event
        )
        self.process_event(edss_event)

    def on_created(self, event):
        """Handle new rule file"""
        partial_debug("Created " + str(event))
        edss_event = get_event(
            event
        )
        self.process_event(edss_event)

    def on_deleted(self, event):
        """Handle deleted rule file"""
        partial_debug("Deleted " + str(event))
        edss_event = get_event(
            event
        )
        if edss_event is not None:
            partial_debug("file: " + edss_event.file_name)
            partial_debug("intermediates: " +
                          edss_event.intermediate_directories)
            partial_debug("edss: " + edss_event.edss_event_type)
            partial_debug("system: " + edss_event.system_event_type)
