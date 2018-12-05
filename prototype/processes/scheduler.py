from pycsp.parallel import *
from prototype.global_methods.debugging import *
from prototype.structs.Task import Task
from prototype.structs.Deschedule import Deschedule


@process
def scheduler(from_server_stdin, from_resources, to_resources):
    scheduler_buffer = []
    pre_conditions = [False] * len(from_resources)
    # This is for the monitor, should always be True
    pre_conditions.append(True)
    input_guards = []
    for from_resource in from_resources:
        input_guards.append(InputGuard(from_resource))
    input_guards.append(InputGuard(from_server_stdin))
    while True:
        pre_conditioned = []
        for i, guard in enumerate(input_guards):
            if pre_conditions[i]:
                pre_conditioned.append(guard)
        channel_index, message = PriSelect(
            pre_conditioned
        )
        if channel_index == from_server_stdin:
            # if we've been sent a new task to be scheduled
            if isinstance(message, Task):
                task_match = False
                for index, buffered in enumerate(scheduler_buffer):
                    if buffered == message:
                        scheduler_buffer[index] = message
                        partial_debug('old task updated (' +
                                      str(len(scheduler_buffer)) + ')')
                        task_match = True
                        break
                if not task_match:
                    partial_debug('new task scheduled (' +
                                  str(len(scheduler_buffer)) + ')')
                    scheduler_buffer.append(message)
                for x in range(len(from_resources)):
                    pre_conditions[x] = True
            # if we've been sent a notification to deschedule things
            elif isinstance(message, Deschedule):
                deleting_tasks = []
                for index, buffered in enumerate(scheduler_buffer):
                    full_debug("buffered.file: " + buffered.file)
                    if buffered.file == message.path:
                        deleting_tasks.append(index)
                    if buffered.recipe.name == \
                            message.intermediate_directories + \
                            message.file_name:
                        deleting_tasks.append(index)
                    if buffered.pattern.path == message.path:
                        deleting_tasks.append(index)
                    for task in deleting_tasks:
                        scheduler_buffer.remove(task)

        # Input message came from a resource looking for a process.
        # Can ignore empty input
        else:
            i = -1
            for a in range(len(from_resources)):
                if from_resources[a] == channel_index:
                    i = a
            to_resources[i](scheduler_buffer[0])
            del scheduler_buffer[0]
            partial_debug('task processed (' +
                          str(len(scheduler_buffer)) + ')')
            if len(scheduler_buffer) == 0:
                for x in range(len(from_resources)):
                    pre_conditions[x] = False
