from ...dfa import EndState, State
from ..token import TokenEnum
from ..charset import *


def whitespace_cb(token):
    return token, TokenEnum.WHITESPACE


state0 = State(0)   # begin state
state1 = State(1)
state2 = EndState(2, whitespace_cb)

state0.add_transition(alias.whitespace, state1)
state1.add_transition(alias.whitespace, state1)
state1.set_default_transition(state2)
