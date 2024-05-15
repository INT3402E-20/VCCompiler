from vccompiler.lexer.token import TokenEnum
from vccompiler.ll1 import Format as F, LL1Grammar as L, Symbol as S


program = S("program")   # start symbol
func_decl = S("func-decl")
var_decl = S("var-decl")
var_type = S("type")
declarator = S("declarator", TokenEnum.IDENTIFIER)

rules = [
    (program, func_decl, program),
    (program, F("{", 1), var_decl, F(-1, "}"), program),
    (program, S.eps),
    (var_decl, var_type, F(" "), declarator, ";"),
    (var_type, "void"),
    (var_type, "boolean"),
    (var_type, "int"),
    (var_type, "float"),
]

grammar = L(program)
for rule in rules:
    grammar.add_rule(*rule)
