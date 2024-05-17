from vccompiler.dfa import State
from vccompiler.lexer.token import *
from vccompiler.lexer.charset import *


state0 = State(0)
state1 = State(1, IDENTIFIER)

state0.add(alias.letter, state1)
state1.add(alias.letter + alias.digit, state1)

KEYWORDS = ["break", "continue", "else", "for", "if", "return", "while"]
TYPE_INITS = ["float", "int", "void", "boolean"]
LITERALS = ["true", "false"]

for keyword in KEYWORDS:
    state0.insert_keyword(keyword, -1, KEYWORD)

for type_init in TYPE_INITS:
    state0.insert_keyword(type_init, -1, TYPE_INIT)

for literal in LITERALS:
    state0.insert_keyword(literal, -1, BOOLEANLITERAL)
