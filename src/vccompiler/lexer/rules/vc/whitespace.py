from vccompiler.dfa import EndState, State
from vccompiler.lexer.token_types import TokenEnum
from vccompiler.lexer.charset import *


state0 = State(0)   # begin state
state1 = EndState(1, TokenEnum.WHITESPACE)

state0.add(alias.whitespace, state1)
state1.add(alias.whitespace, state1)
