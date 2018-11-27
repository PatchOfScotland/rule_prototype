
import os
from debugging import *


def recursive_search_to_list(search_directory, file_list):
    full_debug('Searching through : ' + str(search_directory))
    if os.path.isdir(search_directory):
        full_debug('is a directory')
        for found_file in os.listdir(search_directory):
            full_debug('found file: ' + str(found_file))
            file_path = search_directory + '/' + found_file
            # If file is a directory then search in that as well
            if '.' not in found_file:
                recursive_search_to_list(file_path, file_list)
            else:
                pass
                file_list.append(file_path)
                full_debug('file added')
