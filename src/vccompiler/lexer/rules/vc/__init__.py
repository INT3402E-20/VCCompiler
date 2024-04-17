from .whitespace import state0 as whitespace
from .string_literal import state0 as string_literal
from .separator import state0 as separator
from .operator import state0 as operator
from .number_literal import state0 as number_literal
from .identifier import state0 as identifier


__all__ = ['rule']

rule = [
    whitespace,
    string_literal,
    separator,
    operator,
    number_literal,
    identifier,
]
