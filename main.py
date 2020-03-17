import json
import re

from alu_parser import AluParser
from uart_parser import UartParser
from memory_parser import MemoryParser
from memory_map import MemoryMap
from list_data_input import data

remove_death_time = True

alu_dir_out = "errors_alu"
uart_dir_out = "errors_uart"
memory_dir_out = "errors_memory"
memory_map_dir_out = "memory_map"
wolfram_dir = "wolfram"
number_errors_filename = "number_errors.log"
map_memory_coords_filename = "map_coords.log"


def create_dir(path_dir):
    import os
    if os.path.isdir(path_dir) is False:
        os.mkdir(path_dir)


with open(number_errors_filename, 'w') as f:
    pass

for file, cosrad_table in data:
    alu = AluParser(remove_death_time if cosrad_table else False)
    uart = UartParser(remove_death_time if cosrad_table else False)
    memory = MemoryParser(remove_death_time if cosrad_table else False)
    memory_map = MemoryMap()

    print("{0:s} is being processed".format(file))
    with open(file, 'r') as f:
        lines = f.readlines()

    alu_errors = alu.find_error(lines, cosrad_table)
    del alu
    create_dir(alu_dir_out)
    with open("{0:s}/alu_{1:s}".format(alu_dir_out, file.split('/')[1]), 'w') as f:
        json.dump(alu_errors[1], f, indent=2)

    uart_errors = uart.find_error(lines, cosrad_table)
    del uart
    create_dir(uart_dir_out)
    with open("{0:s}/uart_{1:s}".format(uart_dir_out, file.split('/')[1]), 'w') as f:
        json.dump(uart_errors[1], f, indent=2)

    memory_errors = memory.find_error(lines, cosrad_table)
    fluence = memory.fluence
    del memory
    create_dir(memory_dir_out)
    with open("{0:s}/memory_{1:s}".format(memory_dir_out, file.split('/')[1]), 'w') as f:
        json.dump(memory_errors[1], f, indent=2)

    with open(number_errors_filename, 'a') as f:
        numbers_errors = ["{0:s}\n".format(file),
                          "\tALU:\t\t{0:d}\n".format(alu_errors[0]),
                          "\tUART:\t\t{0:d}\n".format(uart_errors[0]),
                          "\tMemory:\t\t{0:d}\n".format(memory_errors[0]),
                          "\tFluence:\t{0:f}\n\n".format(fluence)]
        f.writelines(numbers_errors)

    map_data = [[[a[2], a[3]] for a in pack] for pack in memory_errors[1]]
    map_coords = memory_map.calculate(map_data)
    del memory_map

    create_dir(memory_map_dir_out)
    with open("{0:s}/map_{1:s}".format(memory_map_dir_out, file.split('/')[1]), 'w') as f:
        json.dump(map_coords, f, indent=2)

    create_dir(wolfram_dir)
    with open("{0:s}/wolf_map_{1:s}".format(wolfram_dir, file.split('/')[1]), 'w') as f:
        for line in map_coords:
            f.write(re.sub(']', '}', re.sub('\[', '{', str(line) + "\n")))

print("End of processing")
