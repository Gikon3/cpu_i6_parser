import json
import re

from alu_parser import AluParser
from uart_parser import UartParser
from memory_parser import MemoryParser
from wdt_parser import WdtParser
from memory_map import MemoryMap
from list_data_input import data

remove_death_time = True
module_list = ["ALU", "UART", "Memory", "WDT"]
total_cells_error = [1, 1, 55000 * 32, 1]

alu_dir_out = "errors_alu"
uart_dir_out = "errors_uart"
memory_dir_out = "errors_memory"
wdt_dir_out = "errors_wdt"
memory_map_dir_out = "memory_map"
wolfram_dir = "wolfram"
brief_data_filename = "brief_data.log"
map_memory_coords_filename = "map_coords.log"


def create_dir(path_dir):
    import os
    if os.path.isdir(path_dir) is False:
        os.mkdir(path_dir)


with open(brief_data_filename, 'w') as f:
    pass

for file, cosrad_table in data:
    alu = AluParser(remove_death_time if cosrad_table else False)
    uart = UartParser(remove_death_time if cosrad_table else False)
    memory = MemoryParser(remove_death_time if cosrad_table else False)
    wdt = WdtParser(remove_death_time if cosrad_table else False)
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
    fluence = int(memory.calc_fluence())
    del memory
    create_dir(memory_dir_out)
    with open("{0:s}/memory_{1:s}".format(memory_dir_out, file.split('/')[1]), 'w') as f:
        json.dump(memory_errors[1], f, indent=2)

    wdt_errors = wdt.find_error(lines, cosrad_table)
    del wdt
    create_dir(wdt_dir_out)
    with open("{0:s}/wdt_{1:s}".format(wdt_dir_out, file.split('/')[1]), 'w') as f:
        json.dump(wdt_errors[1], f, indent=2)

    with open(brief_data_filename, 'a') as f:
        brief_data_list = ["{0:s}\n  Errors\n".format(file)]
        for module, error_number in zip(module_list, [alu_errors[0], uart_errors[0], memory_errors[0], wdt_errors[0]]):
            brief_data_list.append("    {0:<7s}: {1:d}\n".format(module, error_number))
        brief_data_list.append("  Cut\n".format(file))
        for module, error_number, total_cells in zip(module_list, [alu_errors[0], uart_errors[0], memory_errors[0], wdt_errors[0]],
                                                     total_cells_error):
            brief_data_list.append("    {0:<7s}: {1:e}\n".format(module, error_number / fluence / total_cells))
        brief_data_list.append("  Fluence: {0:d}\n\n".format(fluence))
        f.writelines(brief_data_list)

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
