from prototype.structs.Process import Process
from prototype.global_methods.debugging import *


class Deschedule:
    def __init__(self, edss_event):
        self.path = edss_event.path
        self.file_name = edss_event.file_name
        self.intermediate_directories = edss_event.intermediate_directories
