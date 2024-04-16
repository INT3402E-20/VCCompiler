from vccompiler.dfa import EndState, State
from vccompiler.lexer.token_types import TokenEnum
from vccompiler.lexer.charset import *


state0 = State(0)
state1 = EndState(1, TokenEnum.LITERAL)
state2 = EndState(2, TokenEnum.LITERAL)
state3 = State(3)
state4 = State(4)
state5 = EndState(5, TokenEnum.LITERAL)
state6 = State(6)
state7 = EndState(7, TokenEnum.LITERAL)


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
