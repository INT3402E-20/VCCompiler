from vccompiler.lexer.token import TokenEnum
from vccompiler.ll1 import LL1Grammar, Symbol
from vccompiler.ll1.production import FormatEnum


program = Symbol("program")   # start symbol
func_decl = Symbol("func-decl")
var_decl = Symbol("var-decl")
var_type = Symbol("type")
declarator = Symbol("declarator", TokenEnum.IDENTIFIER)

grammar = LL1Grammar(program)
# grammar.add_rule(program, func_decl, program)
grammar.add_rule(program, var_decl, FormatEnum.NL, program)
grammar.add_rule(program, Symbol.eps)

grammar.add_rule(var_decl, var_type, FormatEnum.SPACE, declarator, ";")
grammar.add_rule(var_type, "void")
grammar.add_rule(var_type, "boolean")
grammar.add_rule(var_type, "int")
grammar.add_rule(var_type, "float")
