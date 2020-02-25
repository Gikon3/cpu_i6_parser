class MemoryParser:
    WDT = "FFDA8000"
    UNRESET_DEVICE = "FFDA6000"
    TIMEOUT_SPI = "FFDAB000"
    STM_START = "FFDAF000"
    BUFFER_FILL = "FFDAF100"
    MACHINE = "FFDAD000"
    SH_START = "F0DA2000"
    SH_UART = "F0DA3000"
    SH_ALU = "F0DA4000"

    OPCODE0 = "F0DA1000"
    OPCODE1 = "F0DA1001"
    REFERENCE0 = "55555555"
    SYMBOL0 = "5"
    REFERENCE1 = "AAAAAAAA"
    SYMBOL1 = "A"
    THRESHOLD = 128

    def divider_str(self, massive):
        massive_out = []
        for line in massive:
            massive_out.append(line[:-1].split())
        return massive_out

    def find_error(self, massive):
        import operator

        data = self.divider_str(massive)
        massive_errors = []
        f_number_errors = False
        f_errors = False
        number_errors = 0
        count_errors = 0
        stage = ""
        address = ""
        package_errors = []
        errors_all = 0
        for line in data:
            if line[2] == self.WDT or line[2] == self.UNRESET_DEVICE or line[2] == self.TIMEOUT_SPI\
                    or line[2] == self.SH_ALU or line[2] == self.SH_UART or line[2] == self.SH_START:
                f_number_errors = False
                f_errors = False
                number_errors = 0
                count_errors = 0

            elif line[2] == self.OPCODE0 or line[2] == self.OPCODE1:
                f_number_errors = True
                # stage = line[2]

            elif f_number_errors is True:
                f_number_errors = False
                if int(line[2], 16) > 0:
                    f_errors = True
                    number_errors = int(line[2], 16) if int(line[2], 16) < self.THRESHOLD else self.THRESHOLD
                    count_errors = 0

            elif f_errors is True:
                if count_errors < number_errors * 2:
                    if line[2] != self.REFERENCE0 and line[2] != self.REFERENCE1 and count_errors % 2 == 1:
                        error_xor = ""
                        number_5 = line[2].count(self.SYMBOL0)
                        number_a = line[2].count(self.SYMBOL1)
                        if number_5 > 5 or number_a > 5:
                            pattern = self.REFERENCE0 if number_5 > number_a else self.REFERENCE1
                            error_xor = "{0:032b}".format(operator.xor(int(line[2], 16), int(pattern, 16)))
                            # if stage == self.OPCODE0:
                            # error_xor = "{0:032b}".format(operator.xor(int(line[2], 16), int(self.REFERENCE0, 16)))
                            # else:
                            # error_xor = "{0:032b}".format(operator.xor(int(line[2], 16), int(self.REFERENCE1, 16)))
                            package_errors.append([line[0], line[1], address, error_xor])
                            errors_all += sum([int(i) for i in error_xor])
                            # if sum([int(i) for i in error_xor]) > 1:
                            #     print(line[1], sum([int(i) for i in error_xor]), line[2], error_xor)
                    else:
                        address = line[2]
                    count_errors += 1

                if count_errors == number_errors * 2:
                    f_errors = False
                    massive_errors.append(package_errors)
                    package_errors = []

        return [errors_all, massive_errors]