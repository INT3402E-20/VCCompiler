from .comment import state0 as comment
from .whitespace import state0 as whitespace
from ...dfa import DFA


dfa = DFA([
    whitespace,

])
