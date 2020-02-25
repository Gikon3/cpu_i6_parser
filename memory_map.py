class MemoryMap:
    def calculate(self, data):
        coord_errors_pack = []
        prev_coord_error = []
        for pack in data:
            coord_error = []
            for error in pack:
                for i, symbol in enumerate(error[1][::-1]):
                    if symbol == "1":
                        addr_bin = "{0:032b}".format(int(error[0], 16))
                        x = int("{0:03b}{1:05b}{2:03b}".format(
                            int(addr_bin[-5:-2], 2), i, 7 - int(addr_bin[-8:-5], 2)), 2) if i < 16 \
                            else int("{0:03b}{1:05b}{2:03b}".format(
                            int(addr_bin[-5:-2], 2), i, int(addr_bin[-8:-5], 2)), 2)
                        y = int("{0:014b}{1:02b}".format(
                            int(addr_bin[-24:-10], 2), 3 - int(addr_bin[-10:-8], 2)), 2) if addr_bin[-11:-10] == "1" \
                            else int("{0:014b}{1:02b}".format(int(addr_bin[-24:-10], 2), int(addr_bin[-10:-8], 2)), 2)
                        coord_error.append([x, y])
            coord_errors_pack.append(self.remove_repeat_error(coord_error, prev_coord_error))
            prev_coord_error = coord_error.copy()

        return coord_errors_pack

    def remove_repeat_error(self, relev_list, prev_list):
        result = []
        for error in relev_list:
            if error not in prev_list and error not in result:
                result.append(error)

        return result
