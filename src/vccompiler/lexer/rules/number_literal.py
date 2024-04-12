from ...dfa import EndState, State
from ..token import TokenEnum
from .. charset import *


def number_literal_cb(token):
    return token, TokenEnum.LITERAL


state0 = State(0)
state1 = EndState(1, number_literal_cb)
state2 = EndState(2, number_literal_cb)
state3 = State(3)
state4 = State(4)
state5 = EndState(5, number_literal_cb)
state6 = State(6)
state7 = EndState(7, number_literal_cb)


state0.add(alias.digit, state1)
state1.add(alias.digit, state1)
state1.add(".", state2)
state1.add("eE", state3)
state2.add("eE", state3)
state2.add(alias.digit, state7)
state3.add("+-", state4)
state3.add(alias.digit, state5)
state4.add(alias.digit, state5)
state5.add(alias.digit, state5)

state0.add(".", state6)
state6.add(alias.digit, state7)
state7.add(alias.digit, state7)
state7.add("eE", state3)
