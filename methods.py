import os


def recursive_search(search_directory, to_handler):
    for file in os.listdir(search_directory):
        print('Discovered initial file and sending it on to handler: ' + file)
        # If file is a directory then search in that as well
        if '.' not in file:
            recursive_search(search_directory + '\\' + file, to_handler)
        else:
            to_handler((search_directory, file))


def get_matching_patterns(all_patterns, input):
    print('checking patterns ...')
    print('input: ' + input)
    matching_patterns = []
    for pattern in all_patterns:
        print('pattern: ' + str(all_patterns[pattern].input_directory))
        if all_patterns[pattern].input_directory == input:
            matching_patterns.append(all_patterns[pattern])
    print('matching patterns: ' + str(matching_patterns))
    return matching_patterns



