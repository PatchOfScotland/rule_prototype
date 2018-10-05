import os
import variables


def get_path_details(complete_path):
    path_buffer = complete_path.replace(variables.our_path, '')
    directory_path = path_buffer[:path_buffer.rfind('\\')]
    file = path_buffer[path_buffer.rfind('\\'):]
    return (directory_path, file)


def recursive_search_to_list(search_directory, file_list):
    print('---')
    print('Searching through : ' + search_directory)
    if os.path.isdir(search_directory):
        print('is a directory')
        for file in os.listdir(search_directory):
            print('found file: ' + str(file))
            file_path = search_directory + '\\' + file
            # If file is a directory then search in that as well
            if '.' not in file:
                recursive_search_to_list(file_path, file_list)
            else:
                path_details = get_path_details(file_path)
                file_list.append(path_details)
                print('file added')
    else:
        print('IS NOT A DIRECTORY')


def get_matching_patterns_by_recipe(all_patterns, recipe):
#    print('finding matching pattern...')
#    print('all_patterns: ' + str(all_patterns))
#    print('recipe: ' + str(recipe))
#    print('recipe.name: ' + str(recipe.name))
    recipe_directory = variables.recipe_directory.replace(variables.our_path, '')
    matching_patterns = []
    for pattern in all_patterns:
#        print('pattern recipe: ' + str(all_patterns[pattern].recipe))
        recipe_path = recipe_directory + '\\' + all_patterns[pattern].recipe
        if recipe_path == recipe.name:
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

