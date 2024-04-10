from .comment import state0 as comment
from .whitespace import state0 as whitespace
from .identifier import state0 as identifier
from .keyword_after import state0 as keyword_after
from ...dfa import DFA


dfa = DFA([
    whitespace,
    identifier,
    keyword_after,
])
