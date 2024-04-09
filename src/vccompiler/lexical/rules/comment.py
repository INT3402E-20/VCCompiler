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

state0.add_transition("/", state1)
state1.add_transition("/", state2)
state2.set_default_transition(state2)
state2.add_transition("\n" + charset.EOF, state3)

state1.add_transition("*", state4)
state4.set_default_transition(state4)
state4.add_transition("*", state5)
state5.set_default_transition(state4)
state5.add_transition("/", state6)
state6.set_default_transition(state7)
