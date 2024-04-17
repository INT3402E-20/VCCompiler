from vccompiler.dfa import State
from vccompiler.lexer.token_types import TokenEnum
from vccompiler.lexer.charset import *
from vccompiler.lexer.util import insert_keyword


state0 = State(0)
state1 = State(1, TokenEnum.IDENTIFIER)

state0.add(alias.letter, state1)
state1.add(alias.letter + alias.digit, state1)

KEYWORDS = ["boolean", "break", "continue", "else", "float", "for", "if", "int", "return", "void", "while"]
LITERALS = ["true", "false"]

for keyword in KEYWORDS:
    insert_keyword(state0, keyword, -1, TokenEnum.KEYWORD)

for literal in LITERALS:
    insert_keyword(state0, literal, -1, TokenEnum.LITERAL)
