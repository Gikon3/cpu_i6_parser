from base_parser import BaseParser


class WdtParser(BaseParser):
    def __init__(self, remove_death_time):
        BaseParser.__init__(self, remove_death_time)
        self.WDT = "FFDA8000"

    def find_error(self, massive, cosrad_table):
        data = self.divider_str(massive)
        massive_errors = []
        errors_all = 0
        for line in data:
            date = line[0]
            time = line[1]
            fact = line[2]
            if fact == self.WDT:
                massive_errors.append([[date, time, fact]])
                errors_all += 1

        if self.remove_death_time is True:
            self.read_table(cosrad_table)
        return [errors_all, self.calc_death_time(massive_errors) if self.remove_death_time is True else massive_errors]
