from structs import Task
import time
import variables


def first_function(process):
    try:
        input_file = open(process.watching + '\\' + process.file_to_process, 'r')
        data = input_file.read()
        input_file.close()
        data += 'processed by First Task' + '\n'
        time.sleep(variables.processing_time)
        output_file = open(process.writing + '\\' + process.file_to_process, 'w')
        output_file.write(data)
        output_file.close()
        print('First Task processed ' + process.file_to_process)
    except PermissionError:
        print('Could not process, permission denied')


def second_function(process):
    try:
        input_file = open(process.watching + '\\' + process.file_to_process, 'r')
        data = input_file.read()
        input_file.close()
        data += 'processed by Second Task' + '\n'
        time.sleep(variables.processing_time)
        output_file = open(process.writing + '\\' + process.file_to_process, 'w')
        output_file.write(data)
        output_file.close()
        print('Second Task processed ' + process.file_to_process)
    except PermissionError:
        print('Could not process, permission denied')


def third_function(process):
    try:
        input_file = open(process.watching + '\\' + process.file_to_process, 'r')
        data = input_file.read()
        input_file.close()
        data += 'processed by Third Task' + '\n'
        time.sleep(variables.processing_time)
        output_file = open(process.writing + '\\' + process.file_to_process, 'w')
        output_file.write(data)
        output_file.close()
        print('Third Task processed ' + process.file_to_process)
    except PermissionError:
        print('Could not process, permission denied')


all_tasks = {
    'First Task': Task(first_function),
    'Second Task': Task(second_function),
    'Third Task': Task(third_function)
}

