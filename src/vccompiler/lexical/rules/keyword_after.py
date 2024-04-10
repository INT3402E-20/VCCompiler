from ..token import TokenEnum
from ...dfa import EndState, State
from ..charset import alias

def keyword_cb(token):
    return token, TokenEnum.KEYWORD

def identifier_cb(token):
    return token, TokenEnum.IDENTIFIER

state0 = State(0)
state99 = EndState(99, identifier_cb)
state100 = EndState(100, keyword_cb)

# {'r', 'f', 'i', 'v', 'c', 'e', 'b', 'w'}
#index
state1 = State(1)
state0.add('r', state1)
#index
state2 = State(2)
state0.add('f', state2)
#index
state3 = State(3)
state0.add('i', state3)
#index
state4 = State(4)
state0.add('v', state4)
#index
state5 = State(5)
state0.add('c', state5)
#index
state6 = State(6)
state0.add('e', state6)
#index
state7 = State(7)
state0.add('b', state7)
#index
state8 = State(8)
state0.add('w', state8)
state0.add(alias["letter"],state99)

# {'wh', 'if', 'br', 'bo', 're', 'el', 'fl', 'fo', 'vo', 'co', 'in'}
#index w
state9 = State(9)
state8.add('h', state9)
state8.add(alias["letter"] + alias["digit"],state99)
#index i
state10 = State(10)
state3.add('f', state100)
state3.add(alias["letter"] + alias["digit"],state99)
#index b
state11 = State(11)
state7.add('r', state11)
state7.add(alias["letter"] + alias["digit"],state99)
#index b
state12 = State(12)
state7.add('o', state12)
state7.add(alias["letter"] + alias["digit"],state99)
#index r
state13 = State(13)
state1.add('e', state13)
state1.add(alias["letter"] + alias["digit"],state99)
#index e
state14 = State(14)
state6.add('l', state14)
state6.add(alias["letter"] + alias["digit"],state99)
#index f
state15 = State(15)
state2.add('l', state15)
state2.add(alias["letter"] + alias["digit"],state99)
#index f
state16 = State(16)
state2.add('o', state16)
state2.add(alias["letter"] + alias["digit"],state99)
#index v
state17 = State(17)
state4.add('o', state17)
state4.add(alias["letter"] + alias["digit"],state99)
#index c
state18 = State(18)
state5.add('o', state18)
state5.add(alias["letter"] + alias["digit"],state99)
#index i
state19 = State(19)
state3.add('n', state19)
state3.add(alias["letter"] + alias["digit"],state99)

# {'for', 'ret', 'flo', 'voi', 'whi', 'con', 'boo', 'int', 'els', 'bre'}
#index fo
state20 = State(20)
state16.add('r', state20)
state16.add(alias["letter"] + alias["digit"],state99)
#index re
state21 = State(21)
state13.add('t', state21)
state13.add(alias["letter"] + alias["digit"],state99)
#index fl
state22 = State(22)
state15.add('o', state22)
state15.add(alias["letter"] + alias["digit"],state99)
#index vo
state23 = State(23)
state17.add('i', state23)
state17.add(alias["letter"] + alias["digit"],state99)
#index wh
state24 = State(24)
state9.add('i', state24)
state9.add(alias["letter"] + alias["digit"],state99)
#index co
state25 = State(25)
state18.add('n', state25)
state18.add(alias["letter"] + alias["digit"],state99)
#index bo
state26 = State(26)
state12.add('o', state26)
state12.add(alias["letter"] + alias["digit"],state99)
#index in
state27 = State(27)
state19.add('t', state100)
state19.add(alias["letter"] + alias["digit"],state99)
#index el
state28 = State(28)
state14.add('s', state28)
state14.add(alias["letter"] + alias["digit"],state99)
#index br
state29 = State(29)
state11.add('e', state29)
state11.add(alias["letter"] + alias["digit"],state99)

# {'brea', 'bool', 'else', 'whil', 'cont', 'retu', 'floa', 'void'}
#index bre
state30 = State(30)
state29.add('a', state30)
state29.add(alias["letter"] + alias["digit"],state99)
#index boo
state31 = State(31)
state26.add('l', state31)
state26.add(alias["letter"] + alias["digit"],state99)
#index els
state32 = State(32)
state28.add('e', state32)
state28.add(alias["letter"] + alias["digit"],state99)
#index whi
state33 = State(33)
state24.add('l', state33)
state24.add(alias["letter"] + alias["digit"],state99)
#index con
state34 = State(34)
state25.add('t', state34)
state25.add(alias["letter"] + alias["digit"],state99)
#index ret
state35 = State(35)
state21.add('u', state35)
state21.add(alias["letter"] + alias["digit"],state99)
#index flo
state36 = State(36)
state22.add('a', state36)
state22.add(alias["letter"] + alias["digit"],state99)
#index voi
state37 = State(37)
state23.add('d', state100)
state23.add(alias["letter"] + alias["digit"],state99)

# {'boole', 'retur', 'float', 'while', 'break', 'conti'}
#index bool
state38 = State(38)
state31.add('e', state38)
state31.add(alias["letter"] + alias["digit"],state99)
#index retu
state39 = State(39)
state35.add('r', state39)
state35.add(alias["letter"] + alias["digit"],state99)
#index floa
state40 = State(40)
state36.add('t', state100)
state36.add(alias["letter"] + alias["digit"],state99)
#index whil
state41 = State(41)
state33.add('e', state100)
state33.add(alias["letter"] + alias["digit"],state99)
#index brea
state42 = State(42)
state30.add('k', state100)
state30.add(alias["letter"] + alias["digit"],state99)
#index cont
state43 = State(43)
state34.add('i', state43)
state34.add(alias["letter"] + alias["digit"],state99)

# {'return', 'contin', 'boolea'}
#index retur
state44 = State(44)
state39.add('n', state100)
state39.add(alias["letter"] + alias["digit"],state99)
#index conti
state45 = State(45)
state43.add('n', state45)
state43.add(alias["letter"] + alias["digit"],state99)
#index boole
state46 = State(46)
state38.add('a', state46)
state38.add(alias["letter"] + alias["digit"],state99)

# {'continu', 'boolean'}
#index contin
state47 = State(47)
state45.add('u', state47)
state45.add(alias["letter"] + alias["digit"],state99)
#index boolea
state48 = State(48)
state46.add('n', state100)
state46.add(alias["letter"] + alias["digit"],state99)

# {'continue'}
#index continu
state49 = State(49)
state47.add('e', state100)
state47.add(alias["letter"] + alias["digit"],state99)