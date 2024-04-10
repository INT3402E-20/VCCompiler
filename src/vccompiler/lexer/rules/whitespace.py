from ...dfa import EndState, State
from ..token import TokenEnum
from ..charset import *


def whitespace_cb(token):
    return token, TokenEnum.WHITESPACE


state0 = State(0)   # begin state
state1 = EndState(1, whitespace_cb)

state0.add(alias.whitespace, state1)
state1.add(alias.whitespace, state1)
