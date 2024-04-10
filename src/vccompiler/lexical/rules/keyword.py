from ..token import TokenEnum
from ...dfa import EndState, State
from ..charset import alias

def boolean_cb(token):
    return token, TokenEnum.KEYWORD

def break_cb(token):
    return token, TokenEnum.KEYWORD

def continue_cb(token):
    return token, TokenEnum.KEYWORD

def else_cb(token):
    return token, TokenEnum.KEYWORD

def for_cb(token):
    return token, TokenEnum.KEYWORD

def float_cb(token):
    return token, TokenEnum.KEYWORD

def if_cb(token):
    return token, TokenEnum.KEYWORD

def int_cb(token):
    return token, TokenEnum.KEYWORD

def return_cb(token):
    return token, TokenEnum.KEYWORD

def void_cb(token):
    return token, TokenEnum.KEYWORD

def while_cb(token):
    return token, TokenEnum.KEYWORD

state0 = State(0)   # begin state
state1 = State(1)  # b char state
state2 = EndState(2, continue_cb)  # continue end state
state3 = EndState(3, else_cb)  # else end state
state4 = State(4)  # f char state
state5 = State(5)  # i char state
state6 = EndState(6, return_cb)  # return end state
state7 = EndState(7, void_cb)  # void end state
state8 = EndState(8, while_cb)  # while end state

state9 = EndState(9, boolean_cb) # boolean end state
state10 = EndState(10, break_cb) # break end state
state11 = EndState(11, float_cb) # float end state
state12 = EndState(12, for_cb) # for end state
state13 = EndState(13, if_cb) # if end state
state14 = EndState(14, int_cb) # int end state

state0.add_transition("b", state1)
state0.add_transition("c", state2)
state0.add_transition("e", state3)
state0.add_transition("f", state4)
state0.add_transition("i", state5)
state0.add_transition("r", state6)
state0.add_transition("v", state7)
state0.add_transition("w", state8)