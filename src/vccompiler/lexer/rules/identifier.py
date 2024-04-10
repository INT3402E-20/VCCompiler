from ..token import TokenEnum
from ...dfa import EndState, State
from ..charset import alias

def identifier_cb(token):
    return token, TokenEnum.IDENTIFIER

state0 = State(0)   # begin state
state1 = State(1)
state2 = EndState(2, identifier_cb)

state0.add(alias.letter, state1)
state1.add(alias.letter + alias.digit, state1)
state1.default(state2)
