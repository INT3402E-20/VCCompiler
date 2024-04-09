from ...dfa import EndState, State
from ..token import TokenEnum
from .. import charset


def comment_cb(token):
    return token, TokenEnum.COMMENT


state0 = State(0)   # begin state
state1 = State(1)
state2 = State(2)
state3 = EndState(3, comment_cb)
state4 = State(4)
state5 = State(5)
state6 = State(6)
state7 = EndState(7, comment_cb)

state0.add("/", state1)
state1.add("/", state2)
state2.default(state2)
state2.add("\n" + charset.EOF, state3)

state1.add("*", state4)
state4.default(state4)
state4.add("*", state5)
state5.default(state4)
state5.add("/", state6)
state6.default(state7)
