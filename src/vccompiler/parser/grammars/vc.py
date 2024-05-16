from vccompiler.lexer.token import TokenEnum
from vccompiler.ll1 import LL1Grammar as L, Symbol as S, RuleGenerator

R = RuleGenerator()


def dangling_else_handler(alpha, sym, old_entry, entry):
    if entry is not S.eps:
        return entry
    return old_entry


program = S("program")   # start symbol
if_stmt = S("if-stmt")
stmt = S("stmt")
else_stmt = S("else-stmt")
expr_stmt = S("expr-stmt")
expr = S("expr")

rules = [
    R(program, stmt, program, formatter="{0}{=}{1}"),
    R(program, S.eps),
    R(if_stmt, "if", "(", ")", stmt, else_stmt, formatter="if (){=}{{{>}{3}{<}}}{4}"),
    R(else_stmt, S.eps),
    R(else_stmt, "else", stmt, formatter="{=}else{=}{{{>}{1}{<}}}"),
    R(stmt, if_stmt),
    R(stmt, expr_stmt),
    R(expr_stmt, TokenEnum.IDENTIFIER, ";"),
    R(expr_stmt, ";"),
]

grammar = L(program, conflict_handler=dangling_else_handler)
for rule in rules:
    grammar.add_rule(rule)
