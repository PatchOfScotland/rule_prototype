import system_variables

def full_debug(message):
    if system_variables.debug_mode == system_variables.FULL:
        debug(message)


def partial_debug(message):
    if system_variables.debug_mode != system_variables.NONE:
        debug(message)


def debug(message):
    print(message)