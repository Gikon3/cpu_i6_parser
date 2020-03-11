import json
import re

from base_parser import BaseParser
from alu_parser import AluParser
from uart_parser import UartParser
from memory_parser import MemoryParser
from memory_map import MemoryMap

files_in = ["logs_input/session_216_short.log",
            "logs_input/session_216.log",
            "logs_input/session_217.log",
            "logs_input/session_218.log",
            "logs_input/session_265.log",
            "logs_input/session_266.log",
            "logs_input/session_267.log",
            "logs_input/session_82_cpu_i6_1_Xe_short.log",
            "logs_input/session_82_cpu_i6_1_Xe.log",
            "logs_input/session_83_cpu_i6_2_Xe_short.log",
            "logs_input/session_83_cpu_i6_2_Xe.log",
            "logs_input/session_84_cpu_i6_3_Xe_short.log",
            "logs_input/session_84_cpu_i6_3_Xe.log"]

files_excel = ["cosrad_excel/82_2020-3-3_23i16i27.xls",
               "cosrad_excel/83_2020-3-4_0i55i26.xls",
               "cosrad_excel/84_2020-3-4_1i33i48.xls"]

alu_dir_out = "errors_alu"
uart_dir_out = "errors_uart"
memory_dir_out = "errors_memory"
memory_map_dir_out = "memory_map"
wolfram_dir = "wolfram"
number_errors_filename = "number_errors.log"
map_memory_coords_filename = "map_coords.log"


# def add_end_of_line(data):
#     massive_out = []
#     for line in data:
#         massive_out.append("{0:s} {1:s} {2:s}\n".format(line[0], line[1], line[2]))
#     return massive_out


base = BaseParser()
alu = AluParser()
uart = UartParser()
memory = MemoryParser()
map = MemoryMap()

base.read_table(files_excel[0])
h = input("END")

with open(number_errors_filename, 'w') as f:
    pass

for file in files_in:
    print("{0:s} is being processed".format(file))
    with open(file, 'r') as f:
        lines = f.readlines()

    alu_errors = alu.find_error(lines)
    with open("{0:s}/alu_{1:s}".format(alu_dir_out, file.split('/')[1]), 'w') as f:
        # f.writelines(add_end_of_line(alu_errors[1]))
        json.dump(alu_errors[1], f, indent=2)

    uart_errors = uart.find_error(lines)
    with open("{0:s}/uart_{1:s}".format(uart_dir_out, file.split('/')[1]), 'w') as f:
        # f.writelines(add_end_of_line(uart_errors[1]))
        json.dump(uart_errors[1], f, indent=2)

    memory_errors = memory.find_error(lines)
    with open("{0:s}/memory_{1:s}".format(memory_dir_out, file.split('/')[1]), 'w') as f:
        json.dump(memory_errors[1], f, indent=2)

    with open(number_errors_filename, 'a') as f:
        numbers_errors = ["{0:s}\n".format(file),
                          "\tALU   : {0:d}\n".format(alu_errors[0]),
                          "\tUART  : {0:d}\n".format(uart_errors[0]),
                          "\tMemory: {0:d}\n\n".format(memory_errors[0])]
        f.writelines(numbers_errors)

    # map_data = []
    # for pack in memory_errors[1]:
    #     map_data += [[a[2], a[3]] for a in pack]

    map_data = [[[a[2], a[3]] for a in pack] for pack in memory_errors[1]]
    map_coords = map.calculate(map_data)

    with open("{0:s}/map_{1:s}".format(memory_map_dir_out, file.split('/')[1]), 'w') as f:
        json.dump(map_coords, f, indent=2)

    with open("{0:s}/wolf_map_{1:s}".format(wolfram_dir, file.split('/')[1]), 'w') as f:
        for line in map_coords:
            f.write(re.sub(']', '}', re.sub('\[', '{', str(line) + "\n")))

print("End of processing")
