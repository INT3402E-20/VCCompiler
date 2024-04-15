from ...dfa import EndState, State
from ..token import TokenEnum
from .. import charset


def operator_cb(token):
    return token, TokenEnum.OPERATOR


def comment_cb(token):
    return token, TokenEnum.COMMENT


state0 = State(0)   # begin state
state1 = EndState(1, operator_cb)
state2 = EndState(2, operator_cb)
state3 = EndState(3, operator_cb)
state4 = EndState(4, operator_cb)
state5 = EndState(5, operator_cb)
state6 = EndState(6, operator_cb)
state7 = EndState(7, operator_cb)
state8 = EndState(8, operator_cb)
state9 = EndState(9, operator_cb)
state10 = EndState(10, operator_cb)
state11 = EndState(11, operator_cb)
state12 = EndState(12, operator_cb)
state13 = State(13)
state14 = EndState(14, operator_cb)
state15 = State(15)
state16 = EndState(16, operator_cb)
state17 = EndState(17, comment_cb)
state18 = State(18)
state19 = State(19)
state20 = EndState(20, comment_cb)


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