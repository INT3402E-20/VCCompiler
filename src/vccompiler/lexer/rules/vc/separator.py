from vccompiler.dfa import EndState, State
from vccompiler.lexer.token import *


state0 = State(0)   # begin state
state1 = EndState(1, SEPARATOR)
state2 = EndState(2, SEPARATOR)
state3 = EndState(3, SEPARATOR)
state4 = EndState(4, SEPARATOR)
state5 = EndState(5, SEPARATOR)
state6 = EndState(6, SEPARATOR)
state7 = EndState(7, SEPARATOR)
state8 = EndState(8, SEPARATOR)

state0.add("{", state1)
state0.add("}", state2)

state0.add("(", state3)
state0.add(")", state4)


state0.add("[", state5)
state0.add("]", state6)


state0.add(",", state7)

state0.add(";", state8)

# Mermaid graph:

# flowchart TB
#     id0((0))
#     id1(((1)))
#     id2(((2)))
#     id3(((3)))
#     id4(((4)))
#     id5(((5)))
#     id6(((6)))
#     id7(((7)))
#     id8(((8)))

#     id0-->|"{"|id1
#     id0-->|"}"|id2
#     id0-->|"["|id3
#     id0-->|"]"|id4
#     id0-->|"("|id5
#     id0-->|")"|id6
#     id0-->|","|id7
#     id0-->|";"|id8