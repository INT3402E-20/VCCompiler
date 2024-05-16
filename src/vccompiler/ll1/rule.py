from vccompiler.lexer.token import TokenEnum
from vccompiler.ll1.symbol import Symbol


class Rule:
    def __init__(self, alpha, betas, **semantics):
        self.lhs = alpha
        self.rhs = betas
        self.semantics = semantics

    def __str__(self):
        return f"{self.lhs} -> {' '.join(str(beta) for beta in self.rhs)}"


class RuleGenerator:
    def __init__(self):
        self.literal_symbols = {}
        self.token_enum_symbols = {}

    def init(self, sym):
        if isinstance(sym, str):
            literal = sym
            sym = self.literal_symbols.get(literal, Symbol(sym, sym))
            self.literal_symbols[literal] = sym
        elif isinstance(sym, TokenEnum):
            token = sym
            sym = self.token_enum_symbols.get(sym, Symbol(sym.value, sym))
            self.token_enum_symbols[token] = sym
        return sym

    def __call__(self, alpha, *betas, **kwargs):
        alpha = self.init(alpha)
        betas = [self.init(beta) for beta in betas]
        return Rule(alpha, betas, **kwargs)


class CSTNode:
    def __init__(self, rule=None):
        self.rule = rule
        self.children = []

    @property
    def semantics(self):
        return self.rule.semantics if isinstance(self.rule, Rule) else {}
