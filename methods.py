import os
import variables


def get_path_details(complete_path):
    path_buffer = complete_path.replace(variables.our_path, '')
    directory_path = path_buffer[:path_buffer.rfind('\\')]
    file = path_buffer[path_buffer.rfind('\\'):]
    return (directory_path, file)


def recursive_search_to_process(search_directory, to_handler):
    if os.path.isdir(search_directory):
        for file in os.listdir(search_directory):
            file_path = search_directory + '\\' + file
            # If file is a directory then search in that as well
            if '.' not in file:
                recursive_search_to_process(file_path, to_handler)
            else:
                path_details = get_path_details(file_path)
                to_handler(path_details)


def recursive_search_to_list(search_directory, file_list):
    if os.path.isdir(search_directory):
        for file in os.listdir(search_directory):
            file_path = search_directory + '\\' + file
            # If file is a directory then search in that as well
            if '.' not in file:
                recursive_search_to_process(file_path, file_list)
            else:
                path_details = get_path_details(file_path)
                file_list.append(path_details)


def get_matching_patterns_by_recipe(all_patterns, recipe):
#    print('finding matching pattern...')
#    print('all_patterns: ' + str(all_patterns))
#    print('recipe: ' + recipe)
    matching_patterns = []
    for pattern in all_patterns:
#        print('pattern recipe: ' + str(all_patterns[pattern].recipe))
        if all_patterns[pattern].recipe == recipe.name:
            matching_patterns.append(all_patterns[pattern])
#    print('matching_patterns: ' + str(matching_patterns))
    return matching_patterns


def get_matching_patterns_by_input(all_patterns, directory):
#    print('finding matching pattern...')
#    print('all_patterns: ' + str(all_patterns))
#    print('directory: ' + directory)
    matching_patterns = []
    for pattern in all_patterns:
#        print('pattern input_directory: ' + str(all_patterns[pattern].input_directory))
        if all_patterns[pattern].input_directory == directory:
            matching_patterns.append(all_patterns[pattern])
#    print('matching_patterns: ' + str(matching_patterns))
    return matching_patterns


def get_recipe(all_recipes, pattern):
#    print('finding recipe...')
#    print('pattern.recipe: ' + str(pattern.recipe))
#    print('all recipes: :' + str(all_recipes))
    recipe_directory = variables.recipe_directory.replace(variables.our_path, '')
    recipe_path = recipe_directory + '\\' + pattern.recipe
#    print('recipe_directory: ' + recipe_directory)
#    print('recipe_path: ' + recipe_path)
    for recipe in all_recipes:
#        print('recipe: ' + str(all_recipes[recipe].name))
        if all_recipes[recipe].name == recipe_path:
            return all_recipes[recipe]
    return None



