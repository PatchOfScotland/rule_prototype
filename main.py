import time
import variables
from structs import *
from processes import *
# from tasks import all_tasks


if __name__ == '__main__':
    print('timestamp for this run: ' + str(variables.time_stamp))

    if not os.path.exists(variables.our_path):
        os.makedirs(variables.data_directory)
        os.makedirs(variables.recipe_directory)
        os.makedirs(variables.rule_directory)
    else:
        print('Path already exists, exiting')
        exit()

    rule_monitor_to_handler = Channel()
    recipe_monitor_to_handler = Channel()
    data_monitor_to_handler = Channel()

    meta_process_list = [
        directory_monitor(variables.rule_directory, rule_monitor_to_handler.writer()),
        rule_handler(rule_monitor_to_handler.reader()),
        directory_monitor(variables.recipe_directory, recipe_monitor_to_handler.writer()),
        recipe_handler(recipe_monitor_to_handler.reader()),
        directory_monitor(variables.data_directory, data_monitor_to_handler.writer()),
        data_handler(data_monitor_to_handler.reader())
    ]

    Parallel(
        meta_process_list
    )
    #
    # rule_one_watch_directory = '\demo\inputDirectory'
    # rule_one_write_directory = '\demo\\' + str(time_stamp) + '\pattern1_outputDirectory'
    # rule_one = Rule(all_tasks['First Task'], rule_one_watch_directory, rule_one_write_directory)
    #
    # rule_two_watch_directory = '\demo\inputDirectory'
    # rule_two_write_directory = '\demo\\' + str(time_stamp) + '\pattern2_outputDirectory'
    # rule_two = Rule(all_tasks['Second Task'], rule_two_watch_directory, rule_two_write_directory)
    # rule_three_watch_directory = rule_one_write_directory
    # rule_three_write_directory = '\demo\\' + str(time_stamp) + '\pattern3_outputDirectory'
    # rule_three = Rule(all_tasks['Third Task'], rule_three_watch_directory, rule_three_write_directory)
    #
    # all_rules = [
    #     rule_one,
    #     rule_two,
    #     rule_three
    # ]
    #
    # run = Run(all_rules, repeat_on_data_change=True, repeat_on_rule_change=True)
    #
    # rule_monitors_to_scheduler_channel = Channel()
    #
    # meta_process_list = []
    #
    # resources_to_scheduler_channels = []
    # scheduler_to_resources_channels = []
    # for x in range(variables.number_of_resources):
    #     resource_to_scheduler_channel = Channel()
    #     resources_to_scheduler_channels.append(resource_to_scheduler_channel)
    #     scheduler_to_resource_channel = Channel()
    #     scheduler_to_resources_channels.append(scheduler_to_resource_channel)
    #     meta_process_list.append(resource(resource_to_scheduler_channel.writer(), scheduler_to_resource_channel.reader()))
    # from_resource_readers = []
    # for from_resource_reader in resources_to_scheduler_channels:
    #     from_resource_readers.append(from_resource_reader.reader())
    # to_resource_writers = []
    # for to_resource_writer in scheduler_to_resources_channels:
    #     to_resource_writers.append(to_resource_writer.writer())
    #
    # meta_process_list.append(scheduler(rule_monitors_to_scheduler_channel.reader(), from_resource_readers, to_resource_writers))
    #
    # for rule in run.rules:
    #     changer_to_monitor = Channel()
    #     meta_process_list.append(rule_monitor(rule, run.repeat_on_rule_change, run.repeat_on_data_change, run.apply_post_facto, rule_monitors_to_scheduler_channel.writer(), changer_to_monitor.reader()))
    #     meta_process_list.append(rule_changer(changer_to_monitor.writer()))
    #
    # Parallel(
    #     meta_process_list
    # )
