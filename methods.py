import os
import system_variables
from pattern import Pattern


def file_is_in_filter(file_type_filter, file):
    file_type = file[file.rfind('.'):]
    if file_type in file_type_filter:
        return True
    return False


def get_path_details(complete_path):
    path_buffer = complete_path.replace(system_variables.pattern_path, '')
    path_buffer = path_buffer.replace(system_variables.data_path, '')
    path_buffer = path_buffer.replace(system_variables.recipe_path, '')
    directory_path = path_buffer[:path_buffer.rfind('\\')]
    file = path_buffer[path_buffer.rfind('\\'):]
    return (directory_path, file)


def recursive_search_to_list(search_directory, file_list):
#    print('---')
#    print('Searching through : ' + search_directory)
    if os.path.isdir(search_directory):
#        print('is a directory')
        for file in os.listdir(search_directory):
#            print('found file: ' + str(file))
            file_path = search_directory + '\\' + file
            # If file is a directory then search in that as well
            if '.' not in file:
                recursive_search_to_list(file_path, file_list)
            else:
                path_details = get_path_details(file_path)
                file_list.append(path_details)
#                print('file added')
#    else:
#        print('IS NOT A DIRECTORY')


def get_matching_patterns_by_recipe(all_patterns, recipe):
#    print('finding matching pattern...')
#    print('all_patterns: ' + str(all_patterns))
#    print('recipe: ' + str(recipe))
#    print('recipe.name: ' + str(recipe.name))
    recipe_directory = system_variables.recipe_directory.replace(system_variables.our_path, '')
    matching_patterns = []
    for pattern in all_patterns:
#        print('pattern recipe: ' + str(all_patterns[pattern].recipe))
        recipe_path = recipe_directory + '\\' + all_patterns[pattern].recipe
        if recipe_path == recipe.name:
            matching_patterns.append(all_patterns[pattern])
#    print('matching_patterns: ' + str(matching_patterns))
    return matching_patterns


def get_matching_patterns_by_input(all_patterns, directory):
    print('finding matching pattern...')
    print('all_patterns: ' + str(all_patterns))
    print('directory: ' + directory)
    matching_patterns = []
    for pattern in all_patterns:
        print('pattern input_directory: ' + str(all_patterns[pattern].input_directory))
        if all_patterns[pattern].input_directory == directory:
            matching_patterns.append(all_patterns[pattern])
    print('matching_patterns: ' + str(matching_patterns))
    return matching_patterns


def get_recipe(all_recipes, pattern):
    print('finding recipe...')
    print('pattern.recipe: ' + str(pattern.recipe))
    print('all recipes: :' + str(all_recipes))
    recipe_path = '\\' + pattern.recipe
    print('recipe_path: ' + recipe_path)
    for recipe in all_recipes:
        print('recipe: ' + str(all_recipes[recipe].name))
        if all_recipes[recipe].name == recipe_path:
            return all_recipes[recipe]
    return None


def variable_inclusive_pattern_parser(input_string):
#    print('PARSING INPUT INTO PATTERN')
#    print(input_string)
    # check is intended as dictionary
    if input_string[0] == '{' and input_string[len(input_string) - 1] == '}':
        buffer_dictionary = {}
#        print('Input is a dictionary')
        dictionary_contents = input_string[1:len(input_string) - 1]
#        print(dictionary_contents)
        dictionary_key_value_pairs = dictionary_contents.split(', ')
        for key_value_pair in dictionary_key_value_pairs:
#            print(str(key_value_pair))
            key_and_value = key_value_pair.split(': ')
            # remove pesky quotation marks
            for index, element in enumerate(key_and_value):
                if (element[0] == '"' or element[0] == '\'') and (element[len(element) - 1] == '"' or element[len(element) - 1] == '\''):
                    key_and_value[index] = element[1:len(element) - 1]
#                    print(key_and_value[index])
            buffer_dictionary[key_and_value[0]] = key_and_value[1]

        input_directory = buffer_dictionary['input_directory']
        output_directory = buffer_dictionary['output_directory']
        if '\\\\' in input_directory:
            input_directory = input_directory.replace('\\\\', '\\')
        if '\\\\' in output_directory:
            output_directory = output_directory.replace('\\\\', '\\')
        print('}{ input_directory: ' + str(input_directory))
        print('}{ output_directory: ' + str(output_directory))
        # crude hack for if is code to be executed. Improve this
        # TODO replace all this with different way of defining input directories. perhaps assume they are always within the projcet directory and appending the front end within the program
        if ' + ' in input_directory:
            input_directory_buffer = ''
            parts = input_directory.split(' + ')
            for part in parts:
                if part[0] == '\'':
                    input_directory_buffer = input_directory_buffer + part[1:len(part) - 1]
                else:
                    # expand this beyond variables two deep maybe?
                    elements = part.split('.')
                    input_directory_buffer = input_directory_buffer + locals()[elements[0]]
        # crude hack for if is code to be executed. Improve this
        if ' + ' in output_directory:
            output_directory_buffer = ''
            parts = output_directory.split(' + ')
            for part in parts:
                if part[0] == '\'':
                    output_directory_buffer = output_directory_buffer + part[1:len(part) - 1]
                else:
                    output_directory_buffer = output_directory_buffer + locals()[part]
        print('}{ input_directory: ' + str(input_directory))
        print('}{ output_directory: ' + str(output_directory))
        return Pattern(buffer_dictionary['recipe'], input_directory, output_directory, buffer_dictionary['variables'])


