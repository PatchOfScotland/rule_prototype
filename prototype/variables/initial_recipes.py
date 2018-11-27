
# used to populate system with data for testing purposes
initial_recipes = [
    [
        "import time",
        "input_file = open(self.input_file, 'r')",
        "data = input_file.read()",
        "input_file.close()",
        "data += 'processed by ' + self.name + '\\n'",
        "time.sleep(processing_time)",
        "output_file = open(self.output_file, 'w')",
        "output_file.write(data)",
        "output_file.close()"
    ],
    [
        "import time",
        "input_file = open(self.input_file, 'r')",
        "data = input_file.read()",
        "input_file.close()",
        "data += 'processed by ' + self.name + '\\n'",
        "time.sleep(processing_time)",
        "output_file = open(self.output_file, 'w')",
        "output_file.write(data)",
        "output_file.close()"
    ],
    [
        "import time",
        "input_file = open(self.input_file, 'r')",
        "data = input_file.read()",
        "input_file.close()",
        "data += 'processed by ' + self.name + '\\n'",
        ("data += str(var_a) + ', ' + str(var_b) + ', ' + str(var_c) + "
         "', ' + str(var_d) +'\\n'"),
        "time.sleep(processing_time)",
        "output_file = open(self.output_file, 'w')",
        "output_file.write(data)",
        "output_file.close()"
    ],
    [
        "import time",
        "input_file = open(self.input_file, 'r')",
        "data = input_file.read()",
        "input_file.close()"
    ],
    [
        "output_file = open(self.output_file, 'w')",
        "output_file.write(data)",
        "output_file.close()"
    ],
    [
        "data += 'processed by ' + self.name + '\\n'",
    ]
]
