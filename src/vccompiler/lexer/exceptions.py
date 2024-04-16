from ..exceptions import VCException
from ..helper import get_line_column_number, get_line_at, get_number_of_lines


class LexerError(VCException):
    def __init__(self, source, source_index, err):
        super().__init__()
        self.source = source
        self.source_index = source_index
        self.err = err

    def __str__(self):
        line_number, column_number = get_line_column_number(self.source, self.source_index)
        err_msg = ""
        err_msg += f"{self.err} at line {line_number}, column {column_number}\n"

        # print 3 lines around the error
        for i in range(line_number - 1, line_number + 2):
            if 1 <= i <= get_number_of_lines(self.source):
                err_msg += f"{i: >8} | {get_line_at(self.source, i)}\n"
            if i == line_number:
                err_msg += " " * 10 + " " * column_number + "^\n"

        return err_msg
