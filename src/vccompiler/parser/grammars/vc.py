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
assignment_expr = S("assignment-expr")
assignment_expr_suffix = S("assignment-expr-suffix")
cond_or_expr = S("cond-or-expr")
cond_or_expr_suffix = S("cond-or-expr-suffix")
cond_and_expr = S("cond-and-expr")
cond_and_expr_suffix = S("cond-and-expr-suffix")
equality_expr = S("equality-expr")
equality_expr_suffix = S("equality-expr-suffix")
rel_expr = S("rel-expr")
rel_expr_suffix = S("rel-expr-suffix")
additive_expr = S("additive-expr")
additive_expr_suffix = S("additive-expr-suffix")
multiplicative_expr = S("multiplicative-expr")
multiplicative_expr_suffix = S("multiplicative-expr-suffix")
unary_expr = S("unary-expr")
primary_expr = S("primary-expr")

rules = [
    R(program, stmt, program, formatter="{0}{=}{1}"),
    R(program, S.eps),

    R(if_stmt, "if", "(", expr, ")", stmt, else_stmt, formatter="if ({2}){=}{{{>}{4}{<}}}{5}"),
    R(else_stmt, S.eps),
    R(else_stmt, "else", stmt, formatter="{=}else{=}{{{>}{1}{<}}}"),

    R(stmt, if_stmt),
    R(stmt, expr_stmt),

    R(expr_stmt, ";"),
    R(expr_stmt, expr, ";"),

    R(expr, assignment_expr),

    R(assignment_expr, cond_or_expr, assignment_expr_suffix, formatter="({0}{1})"),
    R(assignment_expr_suffix, "=", assignment_expr, formatter=" = {1}"),
    R(assignment_expr_suffix, S.eps),

    R(cond_or_expr, cond_and_expr, cond_or_expr_suffix, formatter="({0}{1})", op=(0,), op_prec=7),
    R(cond_or_expr_suffix, "||", cond_or_expr, formatter=" || {1}", op=(1,), op_prec=7),
    R(cond_or_expr_suffix, S.eps),

    R(cond_and_expr, equality_expr, cond_and_expr_suffix, formatter="({0}{1})", op=(0,), op_prec=6),
    R(cond_and_expr_suffix, "&&", cond_and_expr, formatter=" && {1}", op=(1,), op_prec=6),
    R(cond_and_expr_suffix, S.eps),

    R(equality_expr, rel_expr, equality_expr_suffix, formatter="({0}{1})", op=(0,), op_prec=5),
    R(equality_expr_suffix, "==", equality_expr, formatter=" == {1}", op=(1,), op_prec=5),
    R(equality_expr_suffix, "!=", equality_expr, formatter=" != {1}", op=(1,), op_prec=5),
    R(equality_expr_suffix, S.eps),

    R(rel_expr, additive_expr, rel_expr_suffix, formatter="({0}{1})", op=(0,), op_prec=4),
    R(rel_expr_suffix, "<", rel_expr, formatter=" < {1}", op=(1,), op_prec=4),
    R(rel_expr_suffix, "<=", rel_expr, formatter=" <= {1}", op=(1,), op_prec=4),
    R(rel_expr_suffix, ">", rel_expr, formatter=" > {1}", op=(1,), op_prec=4),
    R(rel_expr_suffix, ">=", rel_expr, formatter=" >= {1}", op=(1,), op_prec=4),
    R(rel_expr_suffix, S.eps),

    R(additive_expr, multiplicative_expr, additive_expr_suffix, formatter="({0}{1})", op=(0,), op_prec=3),
    R(additive_expr_suffix, "+", additive_expr, formatter=" + {1}", op=(1,), op_prec=3),
    R(additive_expr_suffix, "-", additive_expr, formatter=" - {1}", op=(1,), op_prec=3),
    R(additive_expr_suffix, S.eps),

    R(multiplicative_expr, unary_expr, multiplicative_expr_suffix, formatter="({0}{1})", op=(0,), op_prec=2),
    R(multiplicative_expr_suffix, "*", multiplicative_expr, formatter=" * {1}", op=(1,), op_prec=2),
    R(multiplicative_expr_suffix, "/", multiplicative_expr, formatter=" / {1}", op=(1,), op_prec=2),
    R(multiplicative_expr_suffix, S.eps),

    R(unary_expr, primary_expr),
    R(unary_expr, "+", unary_expr, formatter="(+ {1})"),
    R(unary_expr, "-", unary_expr, formatter="(- {1})"),
    R(unary_expr, "!", unary_expr, formatter="(! {1})"),

    R(primary_expr, TokenEnum.IDENTIFIER),
    R(primary_expr, "(", expr, ")"),
    R(primary_expr, TokenEnum.LITERAL),
]

grammar = L(program, conflict_handler=dangling_else_handler, left_to_right=(2, 3, 4, 5, 6, 7))
for rule in rules:
    grammar.add_rule(rule)
