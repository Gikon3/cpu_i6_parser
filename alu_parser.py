from base_parser import BaseParser


class AluParser(BaseParser):
    def __init__(self, remove_death_time):
        BaseParser.__init__(self, remove_death_time)
        self.OPCODE = "F0DA4000"
        self.REFERENCE = "00000801"

    def find_error(self, massive, cosrad_table):
        data = self.divider_str(massive)
        massive_errors = []
        f_number_errors = False
        f_errors = False
        errors_all = 0
        for line in data:
            date = line[0]
            time = line[1]
            fact = line[2]
            if fact == self.OPCODE:
                f_number_errors = True

            elif f_number_errors is True:
                f_number_errors = False
                if int(fact, 16) > 0:
                    f_errors = True

            elif f_errors is True:
                f_errors = False
                if fact != self.REFERENCE:
                    massive_errors.append([[date, time, fact]])
                    errors_all += 1

        if self.remove_death_time is True:
            self.read_table(cosrad_table)
        return [errors_all, self.calc_death_time(massive_errors) if self.remove_death_time is True else massive_errors]
