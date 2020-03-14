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
            if line[2] == self.OPCODE:
                f_number_errors = True

            elif f_number_errors is True:
                f_number_errors = False
                if int(line[2], 16) > 0:
                    f_errors = True

            elif f_errors is True:
                f_errors = False
                if line[2] != self.REFERENCE:
                    massive_errors.append([[line[0], line[1], line[2]]])
                    errors_all += 1

        if self.remove_death_time is True:
            self.read_table(cosrad_table)
        return [errors_all, self.calc_death_time(massive_errors) if self.remove_death_time is True else massive_errors]
