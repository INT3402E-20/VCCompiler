from ...dfa import EndState, State
from ..token import TokenEnum
from ..charset import *


def string_literal_cb(token):
    return token, TokenEnum.LITERAL


state0 = State(0)
state1 = State(1)
state2 = State(2)
state3 = EndState(3, string_literal_cb)

state0.add("\"", state1)
state1.default(state1)
state1.add("\n", State.none)
state1.add("\\", state2)
state2.add("bfnrt\'\"\\", state1)
state1.add("\"", state3)
