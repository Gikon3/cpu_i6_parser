from base_parser import BaseParser


class MemoryParser(BaseParser):
    def __init__(self, remove_death_time):
        BaseParser.__init__(self, remove_death_time)
        self.WDT = "FFDA8000"
        self.UNRESET_DEVICE = "FFDA6000"
        self.TIMEOUT_SPI = "FFDAB000"
        self.STM_START = "FFDAF000"
        self.BUFFER_FILL = "FFDAF100"
        self.MACHINE = "FFDAD000"
        self.SH_START = "F0DA2000"
        self.SH_UART = "F0DA3000"
        self.SH_ALU = "F0DA4000"

        self.OPCODE0 = "F0DA1000"
        self.OPCODE1 = "F0DA1001"
        self.REFERENCE0 = "55555555"
        self.SYMBOL0 = "5"
        self.REFERENCE1 = "AAAAAAAA"
        self.SYMBOL1 = "A"
        self.THRESHOLD = 128

        self.double_errors = []

    def find_error(self, massive, cosrad_table):
        import operator

        data = self.divider_str(massive)
        massive_errors = []
        f_number_errors = False
        f_errors = False
        number_errors = 0
        count_errors = 0
        address = ""
        package_errors = []
        errors_all = 0
        for line in data:
            date = line[0]
            time = line[1]
            fact = line[2]
            if fact == self.WDT or fact == self.UNRESET_DEVICE or fact == self.TIMEOUT_SPI\
                    or fact == self.SH_ALU or fact == self.SH_UART or fact == self.SH_START:
                f_number_errors = False
                f_errors = False
                number_errors = 0
                count_errors = 0

            elif fact == self.OPCODE0 or fact == self.OPCODE1:
                f_number_errors = True

            elif f_number_errors is True:
                f_number_errors = False
                if int(fact, 16) > 0:
                    f_errors = True
                    number_errors = int(fact, 16) if int(fact, 16) < self.THRESHOLD else self.THRESHOLD
                    count_errors = 0

            elif f_errors is True:
                if count_errors < number_errors * 2:
                    if fact != self.REFERENCE0 and fact != self.REFERENCE1 and count_errors % 2 == 1:
                        number_5 = fact.count(self.SYMBOL0)
                        number_a = fact.count(self.SYMBOL1)
                        if number_5 > 5 or number_a > 5:
                            pattern = self.REFERENCE0 if number_5 > number_a else self.REFERENCE1
                            error_xor = "{0:032b}".format(operator.xor(int(fact, 16), int(pattern, 16)))
                            package_errors.append([date, time, address, error_xor])
                            errors_all += sum([int(i) for i in error_xor])
                            self.set_last_datetime(date, time)
                            if error_xor.count('1') > 1:
                                self.double_errors.append([date, time, address, error_xor])
                    elif count_errors % 2 == 0:
                        address = fact
                    else:
                        self.remember_death_datatime(date, time)
                    count_errors += 1

                if count_errors == number_errors * 2:
                    f_errors = False
                    massive_errors.append(package_errors)
                    package_errors = []

        if self.remove_death_time is True:
            self.read_table(cosrad_table)
        return [errors_all, self.calc_death_time(massive_errors) if self.remove_death_time is True else massive_errors]

    def get_double_errors(self):
        return self.double_errors
