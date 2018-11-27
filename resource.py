import os
from pycsp.parallel import *
from debugging import *


@process
def resource(to_scheduler, from_scheduler):
    while True:
        to_scheduler(0)
        input_task = from_scheduler()
        partial_debug('Resource got new task: ' + str(input_task))
        if not os.path.exists(input_task.pattern.output_directory):
            try:
                os.makedirs(input_task.pattern.output_directory)
            except OSError:
                debug('File already exists')
        input_process = input_task.create_process()
        partial_debug('Resource created new process: ' + str(input_process))
        input_process.process_file()
