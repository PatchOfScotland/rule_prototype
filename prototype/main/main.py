import os
import prototype.variables.system_variables as system_variables
from pycsp.parallel import *
from prototype.variables.initial_data import initial_data
from prototype.variables.initial_patterns import initial_patterns
from prototype.variables.initial_recipes import initial_recipes
from prototype.processes.server_stdin import server_stdin
from prototype.processes.event_monitor import event_monitor
from prototype.processes.resource import resource
from prototype.processes.scheduler import scheduler
from prototype.global_methods.debugging import *

if __name__ == '__main__':
    partial_debug('timestamp: ' + str(system_variables.time_stamp))

    if not os.path.exists(system_variables.our_path):
        os.makedirs(system_variables.initial_data_path)
        os.makedirs(system_variables.recipe_path)
        os.makedirs(system_variables.pattern_path)
    else:
        partial_debug('Path already exists, exiting')
        exit()
    for count, recipe in enumerate(initial_recipes):
        recipe_file = open(system_variables.recipe_path + '/recipe_' +
                           str(count) + system_variables.recipe_extension, 'w')
        for line in recipe:
            recipe_file.write(line + '\n')
        recipe_file.close()
    for count, data in enumerate(initial_data):
        data_file = open(system_variables.initial_data_path + '/data_' +
                         str(count) + system_variables.data_extension, 'w')
        data_file.write(data)
        data_file.close()
    for count, pattern in enumerate(initial_patterns):
        pattern_file = open(system_variables.pattern_path + '/pattern_' +
                            str(count) + system_variables.pattern_extension,
                            'w')
        pattern_file.write(str(pattern))
        pattern_file.close()

    partial_debug('Initial setup complete')

    event_monitor_to_server_stdin_channel = Channel()
    server_stdin_to_scheduler = Channel()

    process_list = [
        event_monitor(
            event_monitor_to_server_stdin_channel.writer(),
            system_variables.our_path
        ),
        server_stdin(
            event_monitor_to_server_stdin_channel.reader(),
            server_stdin_to_scheduler.writer()
        )
    ]

    # sort out the scheduler and resources.
    resources_to_scheduler_channels = []
    scheduler_to_resources_channels = []
    for x in range(system_variables.number_of_resources):
        resource_to_scheduler_channel = Channel()
        resources_to_scheduler_channels.append(resource_to_scheduler_channel)
        scheduler_to_resource_channel = Channel()
        scheduler_to_resources_channels.append(scheduler_to_resource_channel)
        process_list.append(
            resource(resource_to_scheduler_channel.writer(),
                     scheduler_to_resource_channel.reader()))
    from_resource_readers = []
    for from_resource_reader in resources_to_scheduler_channels:
        from_resource_readers.append(from_resource_reader.reader())
    to_resource_writers = []
    for to_resource_writer in scheduler_to_resources_channels:
        to_resource_writers.append(to_resource_writer.writer())

    process_list.append(
        scheduler(
            server_stdin_to_scheduler.reader(),
            from_resource_readers,
            to_resource_writers
        )
    )

    Parallel(process_list)
