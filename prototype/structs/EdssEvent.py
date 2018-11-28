from prototype.variables.system_variables import *
from prototype.global_methods.debugging import *


def get_event(observed_event):
    source_path = observed_event.src_path
    edss_event_type = None
    event_file = None
    intermediate_directories = None
    if recipe_path + '/' in source_path:
        edss_event_type = recipe_directory
        intermediate_directories = source_path.replace(recipe_path, '')
    elif pattern_path + '/' in source_path:
        edss_event_type = pattern_directory
        intermediate_directories = source_path.replace(pattern_path, '')
    elif data_path + '/' in source_path:
        edss_event_type = data_directory
        intermediate_directories = source_path.replace(data_path, '')

    if edss_event_type is None:
        debug("event is not identifiable and so will be ignored")
    else:
        event_file = source_path[source_path.rfind('/'):]
        intermediate_directories = \
            intermediate_directories.replace(event_file, '')
        # if this is a system file then maybe there is a destination path that
        # leads to the actual altered file. maybe
        debug('event_file: ' + event_file)
#        if event_file[1] == '.':
        try:
            if os.path.isfile(observed_event.dest_path):
                source_path = observed_event.dest_path
                debug('dest_path: ' + str(source_path))
                event_file = source_path[source_path.rfind('/'):]
                debug('event_file: ' + event_file)
        except AttributeError:
            debug('No destination detected for system file, no event created')
        event = EdssEvent(event_file,
                          intermediate_directories,
                          edss_event_type,
                          observed_event.event_type,
                          source_path)
        return event


class EdssEvent:
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
