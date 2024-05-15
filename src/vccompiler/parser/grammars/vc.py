from vccompiler.lexer.token import TokenEnum
from vccompiler.ll1 import Format as F, LL1Grammar as L, Symbol as S


program = S("program")   # start symbol

declare_type = S("declare-type")
vc_type = S("type", TokenEnum.TYPE_INIT)
identifier = S("identifier", TokenEnum.IDENTIFIER)

func_decl = S("func-decl")
para_list = S("para-list")
compound_stmt = S("compound-stmt")
proper_para_list = S("proper-para-list")
temp_para_list = S("temp-para-list")
para_decl = S("para-decl")
array_decl = S("array-decl")
array_size = S("array-size")

temp_compound = S("temp-compound")
var_decl = S("var-decl")
temp_compound_next = S("temp-compound-next")
init_decl_tial = S("init-decl-tial")
temp_init_decl = S("temp-init-decl")
init_decl = S("init-decl")
initialiser = S("initialiser")
many_expr = S("many-expr")
expr = S("expr")

stmt = S("stmt")
if_stmt = S("if-stmt")
for_stmt = S("for-stmt")
while_stmt = S("while-stmt")
break_stmt = S("break-stmt")
continue_stmt = S("continue-stmt")
return_stmt = S("return-stmt")
expr_stmt = S("expr-stmt")
is_expr = S("is-expr")

grammar = L(program)
# grammar.add_rule(program, func_decl, program)

program_rules = [
    (program, vc_type, identifier, declare_type, program),
    (program, S.eps),
    (declare_type, func_decl),
    (declare_type, var_decl),
]

funtion_rules = [
    (func_decl, para_list, compound_stmt),
    (para_list, "(", proper_para_list, ")"),
    (proper_para_list, para_decl, temp_para_list),
    (proper_para_list, S.eps),
    (temp_para_list, ",", para_decl, temp_para_list),
    (temp_para_list, S.eps),
    (para_decl, vc_type, identifier, array_decl),
]

declaration_rules = [
    (var_decl, array_decl, init_decl_tial, temp_init_decl, ";"),
    (temp_init_decl, ",", init_decl, temp_init_decl),
    (temp_init_decl, S.eps),
    (init_decl, identifier, array_decl, init_decl_tial),
    (init_decl_tial, "=", initialiser),
    (init_decl_tial, S.eps),
    (initialiser, expr),
    (initialiser, "{", expr, many_expr, "}"),
    (many_expr, ",", expr, many_expr),
    (many_expr, S.eps),
    (array_decl, "[", array_size, "]"),
    (array_decl, S.eps),
    (array_size, TokenEnum.INTLITERAL),
    (array_size, S.eps),
]

statement_rules = [
    (stmt, compound_stmt),
    (stmt, if_stmt),
    (stmt, for_stmt),
    (stmt, while_stmt),
    (stmt, break_stmt),
    (stmt, continue_stmt),
    (stmt, return_stmt),
    (stmt, expr_stmt),
]

compound_stmt_rules = [
    (compound_stmt, "{" , temp_compound_next, "}"),
    (temp_compound, vc_type, var_decl, temp_compound_next),
    (temp_compound, stmt, temp_compound_next),
    (temp_compound_next, temp_compound),
    (temp_compound_next, S.eps),
]

other_stmt_rules = [
    (if_stmt, "if", "(", expr, ")", stmt, "else", stmt),
    (for_stmt, "for", "(", is_expr, ";", is_expr, ";", is_expr, ")", stmt),
    (is_expr, expr),
    (is_expr, S.eps),
    (while_stmt, "while", "(", expr, ")", stmt),
    (break_stmt, "break", ";"),
    (continue_stmt, "continue", ";"),
    (return_stmt, "return", is_expr, ";"),
    (expr_stmt, is_expr, ";"),
]

# Continue with expr rule

for rule in program_rules:
    grammar.add_rule(*rule)
for rule in funtion_rules:
    grammar.add_rule(*rule)
for rule in declaration_rules:
    grammar.add_rule(*rule)
for rule in statement_rules:
    grammar.add_rule(*rule)
for rule in compound_stmt_rules:
    grammar.add_rule(*rule)
for rule in other_stmt_rules:
    grammar.add_rule(*rule)
