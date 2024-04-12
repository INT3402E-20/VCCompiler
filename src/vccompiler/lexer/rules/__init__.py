from .comment import state0 as comment
from .whitespace import state0 as whitespace
from .string_literal import state0 as string_literal
from .separator import state0 as separator
from .operator import state0 as operator
from .number_literal import state0 as number_literal
from .keyword import state0 as keyword
from ...dfa import DFA


dfa = DFA([
    whitespace,
    string_literal,
    separator,
    operator,
    number_literal,
    keyword,

])
