from vccompiler.dfa import EndState, State
from vccompiler.lexer.token import *


state0 = State(0)   # begin state
state1 = EndState(1, OPERATOR)
state2 = EndState(2, OPERATOR)
state3 = EndState(3, OPERATOR)
state4 = EndState(4, OPERATOR)
state5 = State(5)
state6 = State(6)
state7 = EndState(7, COMMENT)
state8 = EndState(8, COMMENT)
state9 = EndState(9, OPERATOR)
state10 = EndState(10, OPERATOR)
state11 = EndState(11, OPERATOR)
state12 = EndState(12, OPERATOR)
state13 = EndState(13, OPERATOR)
state14 = EndState(14, OPERATOR)
state15 = EndState(15, OPERATOR)
state16 = EndState(16, OPERATOR)
state17 = State(17)
state18 = EndState(18, OPERATOR)
state19 = State(19)
state20 = EndState(20, OPERATOR)


state0.add("+", state1)
state0.add("-", state2)
state0.add("*", state3)
state0.add("/", state4)
state4.add("/", state8)
state8.default(state8)
state8.add("\n", State.none)
state4.add("*", state5)
state5.add("*", state6)
state5.default(state5)
state6.add("/", state7)
state6.add("*", state6)
state6.default(state5)

state0.add("<", state9)
state9.add("=", state10)

state0.add("=", state11)
state11.add("=", state12)

state0.add(">", state13)
state13.add("=", state14)

state0.add("!", state15)
state15.add("=", state16)

state0.add("|", state17)
state17.add("|", state18)

state0.add("&", state19)
state19.add("&", state20)

# Mermaid Graph:

# flowchart TB
#     op0((0)) 
#     op1(((1)))
#     op2(((2)))
#     op3(((3)))
#     op4(((4)))
#     op5((5))
#     op6((6))
#     op7(((7)))
#     op8(((8)))
#     op9(((9)))
#     op10(((10)))
#     op11(((11)))
#     op12(((12)))
#     op13(((13)))
#     op14(((14)))
#     op15(((15)))
#     op16(((16)))
#     op17((17))
#     op18(((18)))
#     op19((19))
#     op20(((20)))

#     op0-->|"+"|op1
#     op0-->|"-"|op2
#     op0-->|"*"|op3
#     op0-->|"/"|op4
#     op4-->|"/"|op8
#     op8-->|any|op8
#     op4-->|"*"|op5
#     op5-->|"*"|op6
#     op5-->|any|op5
#     op6-->|"/"|op7
#     op6-->|"*"|op6
#     op6-->|any|op5

#     op0-->|"<"|op9
#     op9-->|"="|op10

#     op0-->|"="|op11
#     op11-->|"="|op12

#     op0-->|">"|op13
#     op13-->|"="|op14

#     op0-->|"!"|op15
#     op15-->|"="|op16

#     op0-->|"|"|op17
#     op17-->|"|"|op18

#     op0-->|"&"|op19
#     op19-->|"&"|op20