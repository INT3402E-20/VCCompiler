from vccompiler.dfa import EndState, State
from vccompiler.lexer.token import *


state0 = State(0)
state1 = State(1)
state2 = State(2)
state3 = EndState(3, STRINGLITERAL)

state0.add("\"", state1)
state1.default(state1)
state1.add("\n", State.none)
state1.add("\\", state2)
state2.add("bfnrt\'\"\\", state1)
state1.add("\"", state3)
