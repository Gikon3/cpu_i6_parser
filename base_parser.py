class BaseParser:
    def __init__(self, remove_death_time=False):
        self.table = []
        self.fluence = 0.0
        self.FLUX_THRESHOLD = 1.0
        self.remove_death_time = remove_death_time

    def divider_str(self, massive):
        massive_out = []
        for line in massive:
            massive_out.append(line[:-1].split())
        return massive_out

    def read_table(self, filename):
        with open(filename, 'r') as f:
            temp_table = []
            for line in f.readlines():
                temp_table.append(line[:-1].split('\t'))
        temp_table.pop(0)

        for row in temp_table:
            full_date_list = row[1].split()  # row[1] in format "YYYY-MM-DD HH:MM:SS"
            date_list = full_date_list[0].split('-')
            date = "{0:s}.{1:s}.{2:s}".format(date_list[2], date_list[1], date_list[0])
            time = "{0:s}.000000".format(full_date_list[1])
            flux = row[2]
            self.table.append([date, time, float(flux)])

    def read_xls(self, filename):
        import xlrd
        rb = xlrd.open_workbook(filename, formatting_info=True)
        sheet = rb.sheet_by_index(0)
        self.table = 0

    def read_xlsx(self, filename):
        import openpyxl
        wb = openpyxl.load_workbook(filename=filename)
        sheet = wb[0]
        self.table = [v[0].value for v in sheet.range('B2:B10')]

    def calc_death_time(self, massive_errors):
        import datetime
        result_full = []
        counter_flux_unit = 0
        accumulate_flux = 0
        dt_prev = None
        try:
            for pack in massive_errors:
                result_pack = []
                for error in pack:
                    dt_error_time = "{0:s} {1:s}".format(error[0], error[1])[:-7]
                    dt_error = datetime.datetime.strptime(dt_error_time, "%d.%m.%Y %H:%M:%S")

                    dt_time = "{0:s} {1:s}".format(self.table[counter_flux_unit][0],
                                                   self.table[counter_flux_unit][1])[:-7]
                    dt = datetime.datetime.strptime(dt_time, "%d.%m.%Y %H:%M:%S")

                    if dt > dt_error:
                        break

                    while dt < dt_error:
                        # print(dt, dt_error)
                        counter_flux_unit += 1
                        dt_time = "{0:s} {1:s}".format(self.table[counter_flux_unit][0],
                                                       self.table[counter_flux_unit][1])[:-7]
                        dt = datetime.datetime.strptime(dt_time, "%d.%m.%Y %H:%M:%S")

                    if self.table[counter_flux_unit][2] >= self.FLUX_THRESHOLD:
                        result_pack.append(error)

                        if dt != dt_prev or dt_prev is None:
                            accumulate_flux += self.table[counter_flux_unit][2]

                        dt_prev = dt

                if result_pack:
                    result_full.append(result_pack)

        except IndexError:
            print("... IndexError")

        self.fluence = accumulate_flux

        return result_full
