from .comment import state0 as comment
from .whitespace import state0 as whitespace
from .string_literal import state0 as string_literal
from ...dfa import DFA


dfa = DFA([
    whitespace,
    string_literal,
])
