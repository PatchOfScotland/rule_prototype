from system_variables import *

# used to populate system with data for testing purposes
initial_patterns = [
    {
        'recipes': [
            'recipe_0'
        ],
        'input_directories': [
            initial_data_directory
        ],
        'output_directory':
            '/pattern_0_output',
        'type_filter': [
            data_extension
        ],
        'variables': {
            'processing_time': processing_time
        }
    },
    {
        'recipes': [
            'recipe_1'
        ],
        'input_directories': [
            initial_data_directory
        ],
        'output_directory':
            '/pattern_1_output',
        'type_filter': [
            data_extension
        ],
        'variables': {
            'processing_time': processing_time
        }
    },
    {
        'recipes': [
            'recipe_2'
        ],
        'input_directories': [
            '/pattern_0_output'
        ],
        'output_directory':
            '/pattern_2_output',
        'type_filter': [
            data_extension
        ],
        'variables': {
            'processing_time': processing_time,
            'var_a': 867,
            'var_b': 1444,
            'var_c': 1936,
            'var_d': 2100
        }
    },
    {
        'recipes': [
            'recipe_3',
            'recipe_5',
            'recipe_4'
        ],
        'input_directories': [
            initial_data_directory
        ],
        'output_directory':
            '/pattern_3_output',
        'type_filter': [
            data_extension
        ],
        'variables': {
            'processing_time': processing_time
        }
    }
]
