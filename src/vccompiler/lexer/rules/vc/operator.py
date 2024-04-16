from vccompiler.dfa import EndState, State
from vccompiler.lexer.token_types import TokenEnum


state0 = State(0)   # begin state
state1 = EndState(1, TokenEnum.OPERATOR)
state2 = EndState(2, TokenEnum.OPERATOR)
state3 = EndState(3, TokenEnum.OPERATOR)
state4 = EndState(4, TokenEnum.OPERATOR)
state5 = EndState(5, TokenEnum.OPERATOR)
state6 = EndState(6, TokenEnum.OPERATOR)
state7 = EndState(7, TokenEnum.OPERATOR)
state8 = EndState(8, TokenEnum.OPERATOR)
state9 = EndState(9, TokenEnum.OPERATOR)
state10 = EndState(10, TokenEnum.OPERATOR)
state11 = EndState(11, TokenEnum.OPERATOR)
state12 = EndState(12, TokenEnum.OPERATOR)
state13 = State(13)
state14 = EndState(14, TokenEnum.OPERATOR)
state15 = State(15)
state16 = EndState(16, TokenEnum.OPERATOR)
state17 = EndState(17, TokenEnum.COMMENT)
state18 = State(18)
state19 = State(19)
state20 = EndState(20, TokenEnum.COMMENT)


state0.add("+", state1)
state0.add("-", state2)
state0.add("*", state3)
state0.add("/", state4)
state4.add("/", state17)
state17.default(state17)
state17.add("\n", State.none)
state4.add("*", state18)
state18.add("*", state19)
state18.default(state18)
state19.add("/", state20)
state19.default(state18)

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

# Mermaid graph

# flowchart LR
#     id0((0))
#     id1(((1)))
#     id2(((2)))
#     id3(((3)))
#     id4(((4)))
#     id5(((5)))
#     id6(((6)))
#     id7(((7)))
#     id8(((8)))
#     id9(((9)))
#     id10(((10)))
#     id11(((11)))
#     id12(((12)))
#     id13((13))
#     id14(((14)))
#     id15((15))
#     id16(((16)))
#     id17(((17)))
#     id18((18))
#     id19((19))
#     id20(((20)))

#     id0-->|"+"|id1
#     id0-->|"-"|id2
#     id0-->|"*"|id3
#     id0-->|"/"|id4
#     id0-->|"<"|id5
#     id5-->|"="|id6
#     id0-->|"="|id7
#     id7-->|"="|id8
#     id0-->|">"|id9
#     id9-->|"="|id10
#     id0-->|"!"|id11
#     id11-->|"="|id12
#     id0-->|"|"|id13
#     id13-->|"|"|id14
#     id0-->|"&"|id15
#     id15-->|"&"|id16
#     id4-->|"/"|id17
#     id17-->|any|id17
#     id4-->|"*"|id18
#     id18-->|"*"|id19
#     id18-->|any|id18
#     id19-->|"/"|id20