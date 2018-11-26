import os
import time
from debugging import *
from pycsp.parallel import *
from EventMonitor import EventMonitor
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent
from global_methods import recursive_search_to_list


@process
def event_monitor(to_server_stdin, directory_to_monitor):

    # # identify already existing files
    # initial_data = []
    # recursive_search_to_list(directory_to_monitor, initial_data)
    # for data in initial_data:
    #     to_server_stdin((data))

    monitor = EventMonitor(to_server_stdin)
    observer = Observer()
    observer.schedule(monitor, directory_to_monitor, recursive=True)
    observer.start()

    # identify already existing files
    initial_data = []
    recursive_search_to_list(directory_to_monitor, initial_data)
    for data in initial_data:
        full_debug('Found initial file ' + str(data))
        file_system_event = FileSystemEvent(data)
        file_system_event.event_type = system_variables.initial_file_descriptor
        full_debug('created event: ' + str(file_system_event))
        monitor.on_created(file_system_event)
        # to_server_stdin((data, system_variables.initial_file_descriptor))

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            pass



