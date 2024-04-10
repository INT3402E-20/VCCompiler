from ...dfa import EndState, State
from ..token import TokenEnum
from .. import charset


def separator_cb(token):
    return token, TokenEnum.SEPARATOR


state0 = State(0)   # begin state
state1 = EndState(1, separator_cb)
state2 = EndState(2, separator_cb)
state3 = EndState(3, separator_cb)
state4 = EndState(4, separator_cb)
state5 = EndState(5, separator_cb)
state6 = EndState(6, separator_cb)
state7 = EndState(7, separator_cb)
state8 = EndState(8, separator_cb)

state0.add("{", state1)
state0.add("}", state2)

state0.add("(", state3)
state0.add(")", state4)


state0.add("[", state5)
state0.add("]", state6)


state0.add(",", state7)

state0.add(";", state8)
