from .helper import get_line_column_number, get_number_of_lines, get_line_at


class VCException(Exception):
    pass


class VCSourceError(VCException):
    def __init__(self, source, source_index, what):
        super().__init__()
        self.source = source
        self.source_index = source_index
        self.what = what

    def __str__(self):
        line_number, column_number = get_line_column_number(self.source, self.source_index)
        err_msg = f"{self.what} at line {line_number}, column {column_number}\n"

        # print 3 lines around the error
        for i in range(line_number - 1, line_number + 2):
            if 1 <= i <= get_number_of_lines(self.source):
                err_msg += f"{i: >8} | {get_line_at(self.source, i)}\n"
            if i == line_number:
                err_msg += " " * 10 + " " * column_number + "^\n"

        return err_msg
