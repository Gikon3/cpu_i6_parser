import json
import re

from alu_parser import AluParser
from uart_parser import UartParser
from memory_parser import MemoryParser
from memory_map import MemoryMap

remove_death_time = True

data_in = [
    ["logs_input/session_216_short.log", ""],
    ["logs_input/session_216.log", ""],
    ["logs_input/session_217.log", ""],
    ["logs_input/session_218.log", ""],
    ["logs_input/session_265.log", ""],
    ["logs_input/session_266.log", ""],
    ["logs_input/session_267.log", ""],
    ["logs_input/session_82_cpu_i6_1_Xe_short.log", "cosrad_excel/82_2020-3-3_23i16i27.xls"],
    ["logs_input/session_82_cpu_i6_1_Xe.log", "cosrad_excel/82_2020-3-3_23i16i27.xls"],
    ["logs_input/session_83_cpu_i6_2_Xe_short.log", "cosrad_excel/83_2020-3-4_0i55i26.xls"],
    ["logs_input/session_83_cpu_i6_2_Xe.log", "cosrad_excel/83_2020-3-4_0i55i26.xls"],
    ["logs_input/session_84_cpu_i6_3_Xe_short.log", "cosrad_excel/84_2020-3-4_1i33i48.xls"],
    ["logs_input/session_84_cpu_i6_3_Xe.log", "cosrad_excel/84_2020-3-4_1i33i48.xls"],
    ["logs_input/session_245_cpu_i6_1_Ar.log", "cosrad_excel/245_2020-3-11_4i40i25.xls"],
    ["logs_input/session_246_cpu_i6_1_Ar_dop.log", "cosrad_excel/246_2020-3-11_5i38i30.xls"],
    ["logs_input/session_247_cpu_i6_2_Ar.log", "cosrad_excel/247_2020-3-11_6i21i41.xls"],
    ["logs_input/session_248_cpu_i6_2_Ar_dop.log", "cosrad_excel/248_2020-3-11_6i54i15.xls"],
    ["logs_input/session_249_cpu_i6_3_Ar.log", "cosrad_excel/249_2020-3-11_8i14i2.xls"],
    ["logs_input/session_251_cpu_i6_3_Ar_dop.log", "cosrad_excel/251_2020-3-11_9i55i51.xls"],
    ["logs_input/session_281_cpu_i6_1_Kr.log", "cosrad_excel/281_2020-3-13_4i41i18.xls"],
    ["logs_input/session_282_cpu_i6_2_Kr.log", "cosrad_excel/282_2020-3-13_5i16i50.xls"]
]

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

for file, cosrad_table in data_in:
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
    del memory
    create_dir(memory_dir_out)
    with open("{0:s}/memory_{1:s}".format(memory_dir_out, file.split('/')[1]), 'w') as f:
        json.dump(memory_errors[1], f, indent=2)

    with open(number_errors_filename, 'a') as f:
        numbers_errors = ["{0:s}\n".format(file),
                          "\tALU   : {0:d}\n".format(alu_errors[0]),
                          "\tUART  : {0:d}\n".format(uart_errors[0]),
                          "\tMemory: {0:d}\n\n".format(memory_errors[0])]
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
