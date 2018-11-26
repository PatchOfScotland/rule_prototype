from system_variables import *
from debugging import *


def get_event(observed_event):
    source_path = observed_event.src_path
    edss_event_type = None
    file = None
    intermediate_directories = None
    if recipe_path + '/' in source_path:
        edss_event_type = recipe_directory
        intermediate_directories = source_path.replace(recipe_path, '')
        file = source_path[source_path.rfind('/'):]
        intermediate_directories = intermediate_directories.replace(file, '')

    elif pattern_path + '/' in source_path:
        edss_event_type = pattern_directory
        intermediate_directories = source_path.replace(pattern_path, '')
        file = source_path[source_path.rfind('/'):]
        intermediate_directories = intermediate_directories.replace(file, '')

    elif data_path + '/' in source_path:
        edss_event_type = data_directory
        intermediate_directories = source_path.replace(data_path, '')
        file = source_path[source_path.rfind('/'):]
        intermediate_directories = intermediate_directories.replace(file, '')

    if edss_event_type is None:
        debug("event is not identifiable and so will be ignored")
    else:
        event = Event(file,
                      intermediate_directories,
                      edss_event_type,
                      observed_event.event_type,
                      source_path)
        return event


class Event():
    def __init__(
            self,
            file_name,
            intermediate_directories,
            edss_event_type,
            system_event_type,
            path
    ):
        self.file_name = file_name
        self.intermediate_directories = intermediate_directories
        self.edss_event_type = edss_event_type
        self.system_event_type = system_event_type
        self.path = path
