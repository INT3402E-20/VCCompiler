from bisect import bisect_left
from functools import cache


@cache
def get_newlines(source):
    return tuple(i for i in range(len(source)) if source[i] == '\n')


def get_number_of_lines(source):
    return len(get_newlines(source)) + 1


def get_line_column_number(source, source_index):
    # get line number and column number from file pointer (1-indexed)
    # this function use binary search to find the line number
    newlines = get_newlines(source)
    position = bisect_left(newlines, source_index)

    if position == 0:
        # first line
        return 1, source_index + 1
    else:
        return position + 1, source_index - newlines[position - 1]


def get_line_at(source, line_number):
    # line number is 1-indexed
    assert 1 <= line_number <= get_number_of_lines(source)

    newlines = get_newlines(source)

    position_left = 0 if line_number == 1 else newlines[line_number - 2] + 1
    position_right = -1 if line_number >= len(newlines) + 1 else newlines[line_number - 1]

    return source[position_left:position_right]
