from ..token import TokenEnum
from ...dfa import EndState, State
from ..charset import alias

def identifier_cb(token):
    return token, TokenEnum.IDENTIFIER

state0 = State(0)   # begin state
state1 = EndState(1, identifier_cb)

state0.add_transition(alias["letter"], state1)
state1.set_default_transition(state1)