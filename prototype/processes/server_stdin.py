from pycsp.parallel import *
from prototype.structs.Task import Task
from prototype.structs.Deschedule import Deschedule
from prototype.global_methods.debugging import *


@process
def server_stdin(from_event_monitor, to_scheduler):
    while True:
        message = from_event_monitor()
        if isinstance(message, Task):
            to_scheduler(message)
        elif isinstance(message, Deschedule):
            to_scheduler(message)
        else:
            full_debug("object was not a task or a deschedule so was ignored")
