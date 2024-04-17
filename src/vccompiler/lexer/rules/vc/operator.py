from vccompiler.dfa import EndState, State
from vccompiler.lexer.token_types import TokenEnum


state0 = State(0)   # begin state
state1 = EndState(1, TokenEnum.OPERATOR)
state2 = EndState(2, TokenEnum.OPERATOR)
state3 = EndState(3, TokenEnum.OPERATOR)
state4 = EndState(4, TokenEnum.OPERATOR)
state5 = State(5)
state6 = State(6)
state7 = EndState(7, TokenEnum.COMMENT)
state8 = EndState(8, TokenEnum.COMMENT)
state9 = EndState(9, TokenEnum.OPERATOR)
state10 = EndState(10, TokenEnum.OPERATOR)
state11 = EndState(11, TokenEnum.OPERATOR)
state12 = EndState(12, TokenEnum.OPERATOR)
state13 = EndState(13, TokenEnum.OPERATOR)
state14 = EndState(14, TokenEnum.OPERATOR)
state15 = EndState(15, TokenEnum.OPERATOR)
state16 = EndState(16, TokenEnum.OPERATOR)
state17 = State(17)
state18 = EndState(18, TokenEnum.OPERATOR)
state19 = State(19)
state20 = EndState(20, TokenEnum.OPERATOR)


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
state6.default(state6)
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
