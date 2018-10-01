#
# class Rule:
#     def __init__(self, task, input_directory, output_directory):
#         self.task = task
#         self.input_directory = input_directory
#         self.output_directory = output_directory
#
#
# class Run:
#     def __init__(self, rules, repeat_on_rule_change=False, repeat_on_data_change=False, apply_post_facto=True):
#         self.rules = rules
#         self.repeat_on_rule_change = repeat_on_rule_change
#         self.repeat_on_data_change = repeat_on_data_change
#         self.apply_post_facto = apply_post_facto
#
#
# class Task:
#     def __init__(self, processing):
#         self.processing = processing
#
#     def create_process(self, file_to_process, watching, writing):
#         process = Process(self.processing, file_to_process, watching, writing)
#         return process
#
#
# class Process:
#     def __init__(self, processing, file_to_process, watching, writing):
#         self.processing = processing
#         self.file_to_process = file_to_process
#         self.watching = watching
#         self.writing = writing
#
#     def process_file(self):
#         self.processing(self)
#
#     def get_process_name(self):
#         return str(self.processing.__name__) + self.file_to_process + self.watching + self.writing
