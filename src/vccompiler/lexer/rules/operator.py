from ...dfa import EndState, State
from ..token import TokenEnum
from .. import charset


def operator_cb(token):
    return token, TokenEnum.OPERATOR


state0 = State(0)   # begin state
state1 = EndState(1, operator_cb)
state2 = EndState(2, operator_cb)
state3 = EndState(3, operator_cb)
state4 = EndState(4, operator_cb)
state5 = EndState(5, operator_cb)
state6 = EndState(6, operator_cb)
state7 = EndState(7, operator_cb)
state8 = EndState(8, operator_cb)
state9 = EndState(9, operator_cb)
state10 = EndState(10, operator_cb)
state11 = EndState(11, operator_cb)
state12 = EndState(12, operator_cb)
state13 = EndState(13, operator_cb)
state14 = EndState(14, operator_cb)
state15 = State(15)
state16 = EndState(16, operator_cb)
state17 = State(17)

state0.add("+", state1)
state0.add("-", state2)
state0.add("*", state3)
state0.add("/", state4)

state0.add("<", state5)
state5.add("=", state6)

state0.add("=", state7)
state7.add("=", state8)

state0.add(">", state9)
state9.add("=", state10)

state0.add("!", state11)
state11.add("=", state12)

state0.add("|", state13)
state13.add("|", state14)

state0.add("&", state15)
state15.add("&", state16)