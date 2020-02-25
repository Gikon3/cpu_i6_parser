class AluParser:
    OPCODE = "F0DA4000"
    REFERENCE = "00000801"

    def divider_str(self, massive):
        massive_out = []
        for line in massive:
            massive_out.append(line[:-1].split())
        return massive_out

    def find_error(self, massive):
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
                    massive_errors.append([line[0], line[1], line[2]])
                    errors_all += 1

        return [errors_all, massive_errors]
