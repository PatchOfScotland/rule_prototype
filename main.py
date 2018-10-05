from processes import *
from variables import Variables


if __name__ == '__main__':
    print('timestamp for this run: ' + str(Variables.time_stamp))

    if not os.path.exists(Variables.our_path):
        os.makedirs(Variables.initial_data_directory)
        os.makedirs(Variables.recipe_directory)
        os.makedirs(Variables.pattern_directory)
    else:
        print('Path already exists, exiting')
        exit()
    for count, recipe in enumerate(Variables.initial_recipes):
        recipe_file = open(Variables.recipe_directory + '\\recipe_' + str(count) + Variables.recipe_extension, 'w')
        for line in recipe:
            recipe_file.write(line + '\n')
        recipe_file.close()
    for count, data in enumerate(Variables.initial_data):
        data_file = open(Variables.initial_data_directory + '\\data_' + str(count) + Variables.data_extension, 'w')
        data_file.write(data)
        data_file.close()
    for count, pattern in enumerate(Variables.initial_patterns):
        pattern_file = open(Variables.pattern_directory + '\\pattern_' + str(count) + Variables.pattern_extension, 'w')
        pattern_file.write(str(pattern))
        pattern_file.close()

    print('Initial setup complete')

    pattern_monitor_to_handler = Channel()
    pattern_handler_to_task_generator = Channel()
    recipe_monitor_to_handler = Channel()
    recipe_handler_to_task_generator = Channel()
    data_monitor_to_handler = Channel()
    data_handler_to_task_generator = Channel()
    task_generator_to_scheduler = Channel()

    meta_process_list = [
        directory_monitor(Variables.pattern_directory, pattern_monitor_to_handler.writer()),
        pattern_handler(pattern_monitor_to_handler.reader(), pattern_handler_to_task_generator.writer()),
        directory_monitor(Variables.recipe_directory, recipe_monitor_to_handler.writer()),
        recipe_handler(recipe_monitor_to_handler.reader(), recipe_handler_to_task_generator.writer()),
        directory_monitor(Variables.data_directory, data_monitor_to_handler.writer()),
        data_handler(data_monitor_to_handler.reader(), data_handler_to_task_generator.writer()),
        task_generator(data_handler_to_task_generator.reader(), pattern_handler_to_task_generator.reader(), recipe_handler_to_task_generator.reader(), task_generator_to_scheduler.writer()),
    ]

    # sort out the scheduler and resources. Probably a neater way to do this but it works
    resources_to_scheduler_channels = []
    scheduler_to_resources_channels = []
    for x in range(Variables.number_of_resources):
        resource_to_scheduler_channel = Channel()
        resources_to_scheduler_channels.append(resource_to_scheduler_channel)
        scheduler_to_resource_channel = Channel()
        scheduler_to_resources_channels.append(scheduler_to_resource_channel)
        meta_process_list.append(resource(resource_to_scheduler_channel.writer(), scheduler_to_resource_channel.reader()))
    from_resource_readers = []
    for from_resource_reader in resources_to_scheduler_channels:
        from_resource_readers.append(from_resource_reader.reader())
    to_resource_writers = []
    for to_resource_writer in scheduler_to_resources_channels:
        to_resource_writers.append(to_resource_writer.writer())

    meta_process_list.append(scheduler(task_generator_to_scheduler.reader(), from_resource_readers, to_resource_writers))

    Parallel(
        meta_process_list
    )
