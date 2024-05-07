from vccompiler.ll1 import LL1Grammar, Symbol


program = Symbol("program")   # start symbol
func_decl = Symbol("func-decl")
var_decl = Symbol("var-decl")

grammar = LL1Grammar(program)
grammar.add_rule(program, func_decl, program)
grammar.add_rule(program, var_decl, program)
grammar.add_rule(program, Symbol.eps)
