from ..token import TokenEnum
from ...dfa import EndState, State
from ..charset import alias

def keyword_cb(token):
    return token, TokenEnum.KEYWORD

def identifier_cb(token):
    return token, TokenEnum.IDENTIFIER

state0 = State(0)

# {'f', 'e', 'v', 'b', 'r', 'c', 'i', 'w'}
#index
state1 = State(1)
state0.add('f', state1)
#index
state2 = State(2)
state0.add('e', state2)
#index
state3 = State(3)
state0.add('v', state3)
#index
state4 = State(4)
state0.add('b', state4)
#index
state5 = State(5)
state0.add('r', state5)
#index
state6 = State(6)
state0.add('c', state6)
#index
state7 = State(7)
state0.add('i', state7)
#index
state8 = State(8)
state0.add('w', state8)

state99 = EndState(99, identifier_cb)
state0.default(state99)

# {'el', 'fo', 'br', 'if', 'in', 'vo', 'wh', 're', 'co', 'bo', 'fl'}
#index e
state9 = State(9)
state2.add('l', state9)
state2.default(state100)
#index f
state10 = State(10)
state1.add('o', state10)
state1.default(state101)
#index b
state11 = State(11)
state4.add('r', state11)
state4.default(state102)
#index i
state12 = State(12)
state7.add('f', state12)
state7.default(state103)
#index i
state13 = State(13)
state7.add('n', state13)
state7.default(state104)
#index v
state14 = State(14)
state3.add('o', state14)
state3.default(state105)
#index w
state15 = State(15)
state8.add('h', state15)
state8.default(state106)
#index r
state16 = State(16)
state5.add('e', state16)
state5.default(state107)
#index c
state17 = State(17)
state6.add('o', state17)
state6.default(state108)
#index b
state18 = State(18)
state4.add('o', state18)
state4.default(state109)
#index f
state19 = State(19)
state1.add('l', state19)
state1.default(state110)

# {'bre', 'voi', 'els', 'boo', 'whi', 'ret', 'flo', 'con', 'for', 'int'}
#index br
state20 = State(20)
state11.add('e', state20)
#index vo
state21 = State(21)
state14.add('i', state21)
#index el
state22 = State(22)
state9.add('s', state22)
#index bo
state23 = State(23)
state18.add('o', state23)
#index wh
state24 = State(24)
state15.add('i', state24)
#index re
state25 = State(25)
state16.add('t', state25)
#index fl
state26 = State(26)
state19.add('o', state26)
#index co
state27 = State(27)
state17.add('n', state27)
#index fo
state28 = State(28)
state10.add('r', state28)
#index in
state29 = State(29)
state13.add('t', state29)

# {'else', 'retu', 'void', 'whil', 'floa', 'brea', 'bool', 'cont'}
#index els
state30 = State(30)
state22.add('e', state30)
state22.default(state111)
#index ret
state31 = State(31)
state25.add('u', state31)
state25.default(state112)
#index voi
state32 = State(32)
state21.add('d', state32)
state21.default(state113)
#index whi
state33 = State(33)
state24.add('l', state33)
state24.default(state114)
#index flo
state34 = State(34)
state26.add('a', state34)
state26.default(state115)
#index bre
state35 = State(35)
state20.add('a', state35)
state20.default(state116)
#index boo
state36 = State(36)
state23.add('l', state36)
state23.default(state117)
#index con
state37 = State(37)
state27.add('t', state37)
state27.default(state118)

# {'break', 'while', 'retur', 'conti', 'boole', 'float'}
#index brea
state38 = State(38)
state35.add('k', state38)
#index whil
state39 = State(39)
state33.add('e', state39)
#index retu
state40 = State(40)
state31.add('r', state40)
#index cont
state41 = State(41)
state37.add('i', state41)
#index bool
state42 = State(42)
state36.add('e', state42)
#index floa
state43 = State(43)
state34.add('t', state43)

# {'contin', 'return', 'boolea'}
#index conti
state44 = State(44)
state41.add('n', state44)
state41.default(state119)
#index retur
state45 = State(45)
state40.add('n', state45)
state40.default(state120)
#index boole
state46 = State(46)
state42.add('a', state46)
state42.default(state121)

# {'continu', 'boolean'}
#index contin
state47 = State(47)
state44.add('u', state47)
#index boolea
state48 = State(48)
state46.add('n', state48)

# {'continue'}
#index continu
state49 = State(49)
state47.add('e', state49)
state47.default(state122)