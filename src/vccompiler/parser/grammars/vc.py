from vccompiler.lexer.token import TokenEnum
from vccompiler.ll1 import LL1Grammar as L, Symbol as S, RuleGenerator

R = RuleGenerator()


def dangling_else_handler(alpha, sym, old_entry, entry):
    if entry is not S.eps:
        return entry
    return old_entry


program = S("program")   # start symbol

declare_type = S("declare-type")
vc_type = S("type", TokenEnum.TYPE_INIT)
identifier = S("identifier", TokenEnum.IDENTIFIER)

func_decl_suffix = S("func-decl-suffix")
para_list = S("para-list")
para_list_suffix = S("para-list-suffix")
proper_para_list = S("proper-para-list")
proper_para_list_suffix = S("proper-para-list-suffix")
para_decl = S("para-decl")
arg_list = S("arg-list")
arg_list_suffix = S("arg-list-suffix")
proper_arg_list = S("proper-arg-list")
proper_arg_list_suffix = S("proper-arg-list-suffix")
arg = S("arg")

var_decl = S("var-decl")
var_decl_suffix = S("var-decl-suffix")
many_init_declarator = S("init-declarator*")
init_declarator = S("init-declarator")
init_declarator_suffix = S("init-declarator-suffix")
declarator = S("declarator")
initialiser = S("initialiser")
initialiser_assign = S("initialiser-assign")
array_decl = S("array-decl")
array_size = S("array-size")
many_expr = S("many-expr")

compound_stmt = S("compound-stmt")
compound_stmt_inner = S("compound-stmt-inner")
many_stmt = S("stmt*")

stmt = S("stmt")
if_stmt = S("if-stmt")
else_stmt = S("else-stmt")
for_stmt = S("for-stmt")
while_stmt = S("while-stmt")
break_stmt = S("break-stmt")
continue_stmt = S("continue-stmt")
return_stmt = S("return-stmt")
expr_stmt = S("expr-stmt")
is_expr = S("expr?")

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
primary_expr_suffix = S("primary-expr-suffix")

program_rules = [
    R(program, vc_type, identifier, declare_type,
      program, formatter="{0} {1}{2}{=}{3}"),
    R(program, S.eps),

    R(declare_type, func_decl_suffix),
    R(declare_type, var_decl_suffix),
]

function_rules = [
    R(func_decl_suffix, para_list, compound_stmt, formatter="{0}{=}{1}"),

    R(para_list, "(", para_list_suffix),
    R(para_list_suffix, proper_para_list, ")"),
    R(para_list_suffix, ")"),

    R(proper_para_list, para_decl, proper_para_list_suffix),
    R(proper_para_list_suffix, ",", proper_para_list),
    R(proper_para_list_suffix, S.eps),

    R(para_decl, vc_type, identifier, array_decl),

    R(arg_list, "(", arg_list_suffix),
    R(arg_list_suffix, proper_arg_list, ")"),
    R(arg_list_suffix, ")"),

    R(proper_arg_list, arg, proper_arg_list_suffix),
    R(proper_arg_list_suffix, ",", arg, proper_arg_list_suffix),
    R(proper_arg_list_suffix, S.eps),

    R(arg, expr),
]

declaration_rules = [
    R(var_decl_suffix, array_decl, initialiser_assign, many_init_declarator, ";"),
    R(many_init_declarator, ",", init_declarator, many_init_declarator),
    R(many_init_declarator, S.eps),

    R(var_decl, vc_type, init_declarator,
      many_init_declarator, ";", formatter="{0} {1}{2};"),

    R(initialiser_assign, "=", initialiser, formatter=" = {1}"),
    R(initialiser_assign, S.eps),

    R(init_declarator, declarator, init_declarator_suffix),
    R(init_declarator_suffix, "=", initialiser),
    R(init_declarator_suffix, S.eps),

    R(declarator, identifier, array_decl),

    R(array_decl, "[", array_size, "]"),
    R(array_decl, S.eps),
    R(array_size, TokenEnum.INTLITERAL),
    R(array_size, S.eps),

    R(initialiser, expr),
    R(initialiser, "{", expr, many_expr, "}"),
    R(many_expr, ",", expr, many_expr),
    R(many_expr, S.eps),
]

statement_rules = [
    R(stmt, compound_stmt),
    R(stmt, if_stmt),
    R(stmt, for_stmt),
    R(stmt, while_stmt),
    R(stmt, break_stmt),
    R(stmt, continue_stmt),
    R(stmt, return_stmt),
    R(stmt, expr_stmt),
]

compound_stmt_rules = [
    R(compound_stmt, "{", compound_stmt_inner, "}", formatter="{{{>}{1}{<}}}"),
    R(many_stmt, stmt, many_stmt, formatter="{0}{=}{1}"),
    R(many_stmt, S.eps),
    R(compound_stmt_inner, var_decl,
      compound_stmt_inner, formatter="{0}{=}{1}"),
    R(compound_stmt_inner, many_stmt),
]

other_stmt_rules = [
    R(if_stmt, "if", "(", expr, ")", stmt, else_stmt,
      formatter="if ({2}){=}{{{>}{4}{<}}}{5}"),
    R(else_stmt, S.eps),
    R(else_stmt, "else", stmt, formatter="{=}else{=}{{{>}{1}{<}}}"),
    R(for_stmt, "for", "(", is_expr, ";", is_expr, ";", is_expr, ")",
      stmt, formatter="for ({2}; {4}; {6}){=}{8}"),
    R(while_stmt, "while", "(", expr, ")", stmt),
    R(break_stmt, "break", ";"),
    R(continue_stmt, "continue", ";"),
    R(return_stmt, "return", is_expr, ";"),
    R(expr_stmt, is_expr, ";"),
    R(is_expr, expr),
    R(is_expr, S.eps),
]

expr_rules = [
    R(expr, assignment_expr),

    R(assignment_expr, cond_or_expr,
      assignment_expr_suffix, formatter="({0}{1})"),
    R(assignment_expr_suffix, "=", assignment_expr, formatter=" = {1}"),
    R(assignment_expr_suffix, S.eps),

    R(cond_or_expr, cond_and_expr, cond_or_expr_suffix,
      formatter="({0}{1})", op=(0,), op_prec=7),
    R(cond_or_expr_suffix, "||", cond_or_expr,
      formatter=" || {1}", op=(1,), op_prec=7),
    R(cond_or_expr_suffix, S.eps),

    R(cond_and_expr, equality_expr, cond_and_expr_suffix,
      formatter="({0}{1})", op=(0,), op_prec=6),
    R(cond_and_expr_suffix, "&&", cond_and_expr,
      formatter=" && {1}", op=(1,), op_prec=6),
    R(cond_and_expr_suffix, S.eps),

    R(equality_expr, rel_expr, equality_expr_suffix,
      formatter="({0}{1})", op=(0,), op_prec=5),
    R(equality_expr_suffix, "==", equality_expr,
      formatter=" == {1}", op=(1,), op_prec=5),
    R(equality_expr_suffix, "!=", equality_expr,
      formatter=" != {1}", op=(1,), op_prec=5),
    R(equality_expr_suffix, S.eps),

    R(rel_expr, additive_expr, rel_expr_suffix,
      formatter="({0}{1})", op=(0,), op_prec=4),
    R(rel_expr_suffix, "<", rel_expr, formatter=" < {1}", op=(1,), op_prec=4),
    R(rel_expr_suffix, "<=", rel_expr,
      formatter=" <= {1}", op=(1,), op_prec=4),
    R(rel_expr_suffix, ">", rel_expr, formatter=" > {1}", op=(1,), op_prec=4),
    R(rel_expr_suffix, ">=", rel_expr,
      formatter=" >= {1}", op=(1,), op_prec=4),
    R(rel_expr_suffix, S.eps),

    R(additive_expr, multiplicative_expr, additive_expr_suffix,
      formatter="({0}{1})", op=(0,), op_prec=3),
    R(additive_expr_suffix, "+", additive_expr,
      formatter=" + {1}", op=(1,), op_prec=3),
    R(additive_expr_suffix, "-", additive_expr,
      formatter=" - {1}", op=(1,), op_prec=3),
    R(additive_expr_suffix, S.eps),

    R(multiplicative_expr, unary_expr, multiplicative_expr_suffix,
      formatter="({0}{1})", op=(0,), op_prec=2),
    R(multiplicative_expr_suffix, "*", multiplicative_expr,
      formatter=" * {1}", op=(1,), op_prec=2),
    R(multiplicative_expr_suffix, "/", multiplicative_expr,
      formatter=" / {1}", op=(1,), op_prec=2),
    R(multiplicative_expr_suffix, S.eps),

    R(unary_expr, primary_expr),
    R(unary_expr, "+", unary_expr, formatter="(+ {1})"),
    R(unary_expr, "-", unary_expr, formatter="(- {1})"),
    R(unary_expr, "!", unary_expr, formatter="(! {1})"),

    R(primary_expr, identifier, primary_expr_suffix),
    R(primary_expr, "(", expr, ")"),
    R(primary_expr, TokenEnum.INTLITERAL),
    R(primary_expr, TokenEnum.FLOATLITERAL),
    R(primary_expr, TokenEnum.BOOLEANLITERAL),
    R(primary_expr, TokenEnum.STRINGLITERAL),
    R(primary_expr_suffix, arg_list),
    R(primary_expr_suffix, S.eps),
    R(primary_expr_suffix, "[", expr, "]"),
]

grammar = L(program, conflict_handler=dangling_else_handler,
            left_to_right=(2, 3, 4, 5, 6, 7))

for rule in program_rules:
    grammar.add_rule(rule)
for rule in function_rules:
    grammar.add_rule(rule)
for rule in declaration_rules:
    grammar.add_rule(rule)
for rule in statement_rules:
    grammar.add_rule(rule)
for rule in compound_stmt_rules:
    grammar.add_rule(rule)
for rule in other_stmt_rules:
    grammar.add_rule(rule)
for rule in expr_rules:
    grammar.add_rule(rule)
