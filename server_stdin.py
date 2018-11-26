from pycsp.parallel import *
from task import Task
from debugging import *


@process
def server_stdin(from_event_monitor, to_scheduler):
    while True:
        message = from_event_monitor()
        if isinstance(message, Task):
            to_scheduler(message)
        else:
            full_debug("object was not a task so was ignored")
