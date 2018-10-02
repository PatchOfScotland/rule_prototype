import os


def recursive_search(search_directory, to_handler):
    for file in os.listdir(search_directory):
        print('Discovered initial file and sending it on to handler: ' + file)
        # If file is a directory then search in that as well
        if '.' not in file:
            recursive_search(search_directory + '\\' + file, to_handler)
        else:
            to_handler((search_directory, file))


def get_matching_patterns(all_patterns, directory):
    matching_patterns = []
    for pattern in all_patterns:
        if all_patterns[pattern].input_directory == directory:
            matching_patterns.append(all_patterns[pattern])
    return matching_patterns


def get_recipe(all_recipes, pattern):
    print('finding recipe...')
    print('pattern.recipe: ' + str(pattern.recipe))
    print('all recipes: :' + str(all_recipes))
    for recipe in all_recipes:
        print('recipe: ' + str(all_recipes[recipe].name))
        if all_recipes[recipe].name == pattern.recipe:
            return all_recipes[recipe]
    return None



