from vccompiler.lexer.token_types import TokenEnum
from vccompiler.ll1 import LL1Grammar, Symbol


program = Symbol("program")   # start symbol
func_decl = Symbol("func-decl")
var_decl = Symbol("var-decl")
var_type = Symbol("type")
declarator = Symbol("declarator", TokenEnum.IDENTIFIER)

grammar = LL1Grammar(program)
# grammar.add_rule(program, func_decl, program)
grammar.add_rule(program, var_decl, program)
grammar.add_rule(program, Symbol.eps)

grammar.add_rule(var_decl, var_type, declarator, ";")
grammar.add_rule(var_type, "void")
grammar.add_rule(var_type, "boolean")
grammar.add_rule(var_type, "int")
grammar.add_rule(var_type, "float")