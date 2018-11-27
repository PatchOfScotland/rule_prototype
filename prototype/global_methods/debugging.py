import prototype.variables.system_variables


def full_debug(message):
    if prototype.variables.system_variables.debug_mode == \
            prototype.variables.system_variables.FULL:
        debug(message)


def partial_debug(message):
    if prototype.variables.system_variables.debug_mode != \
            prototype.variables.system_variables.NONE:
        debug(message)


def debug(message):
    print(message)
