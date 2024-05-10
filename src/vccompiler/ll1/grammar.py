import logging
from vccompiler.exceptions import VCException
from vccompiler.lexer.charset import EOF
from vccompiler.lexer.token import TokenEnum
from vccompiler.ll1.symbol import Symbol


logger = logging.getLogger(__name__)


class ParserError(VCException):
    def __init__(self, token_index, what):
        self.token_index = token_index
        self.what = what


class Rule:
    def __init__(self, alpha, betas):
        self.alpha = alpha
        self.betas = betas


class LL1Grammar:
    def __init__(self, start):
        self.production_rules = []
        self.first_table = None
        self.follow_table = None
        self.parsing_table = None
        self.terminals = set()
        self.non_terminals = set()

        self.start = Symbol("grammar-start")
        eof = Symbol("EOF", EOF)
        self.add_rule(self.start, start, eof)

    def add_symbol(self, sym):
        if isinstance(sym, Symbol):
            if sym.is_terminal:
                self.terminals.add(sym)
            else:
                self.non_terminals.add(sym)
        if isinstance(sym, str):
            sym = Symbol(sym, sym)
            self.terminals.add(sym)
        return sym

    def add_rule(self, alpha, *betas):
        alpha = self.add_symbol(alpha)
        betas = [self.add_symbol(beta) for beta in betas]
        rule = Rule(alpha, betas)
        self.production_rules.append(rule)

    def get_first(self, *syms):
        first_set = set()
        nullable = True
        for sym in syms:
            if nullable:
                first_set |= self.first_table[sym]
            nullable = nullable and Symbol.eps in self.first_table[sym]
        first_set.discard(Symbol.eps)
        if nullable:
            first_set.add(Symbol.eps)
        return first_set

    def build_first(self):
        self.first_table = {}
        for sym in self.terminals:
            self.first_table[sym] = {sym}
        for sym in self.non_terminals:
            self.first_table[sym] = set()
        self.first_table[Symbol.eps] = {Symbol.eps}

        stopped = False
        while not stopped:
            stopped = True

            def update(alpha, sym):
                nonlocal stopped
                if sym not in self.first_table[alpha]:
                    self.first_table[alpha].add(sym)
                    stopped = False

            for rule in self.production_rules:
                if all(Symbol.eps in self.first_table[beta] for beta in rule.betas):
                    update(rule.alpha, Symbol.eps)

                for sym in self.get_first(*rule.betas):
                    update(rule.alpha, sym)

    def build_follow(self):
        self.follow_table = {}
        for sym in self.non_terminals:
            self.follow_table[sym] = set()

        stopped = False
        while not stopped:
            stopped = True

            def update(alpha, sym):
                nonlocal stopped
                if sym not in self.follow_table[alpha]:
                    self.follow_table[alpha].add(sym)
                    stopped = False

            for rule in self.production_rules:
                for i, beta in enumerate(rule.betas):
                    if beta in self.non_terminals:
                        first_set = self.get_first(*rule.betas[i+1:])
                        for sym in first_set:
                            if sym is not Symbol.eps:
                                update(beta, sym)
                        if Symbol.eps in first_set:
                            for sym in self.follow_table[rule.alpha]:
                                update(beta, sym)

    def build_ll1(self):
        self.parsing_table = dict()

        def update(alpha, sym, entry):
            assert (alpha, sym) not in self.parsing_table
            self.parsing_table[(alpha, sym)] = entry

        for rule in self.production_rules:
            first_set = self.get_first(*rule.betas)
            for sym in first_set:
                if sym in self.terminals:
                    update(rule.alpha, sym, rule)
            if Symbol.eps in first_set:
                for sym in self.follow_table[rule.alpha]:
                    update(rule.alpha, sym, Symbol.eps)

    def build(self):
        self.build_first()
        self.build_follow()
        self.build_ll1()

    def parse(self, tokens):
        tokens.append((EOF, TokenEnum.EOF))
        stack = [self.start]

        ptr = 0
        while len(stack) > 0 and ptr < len(tokens):
            sym = stack.pop()
            if sym in self.terminals:
                token, kind = tokens[ptr]
                if sym.fit(token, kind):
                    ptr += 1
                    logger.info(f"{sym} -> \"{token}\"")
                else:
                    raise ParserError(ptr, f"expected {sym}, found {token}")
            elif sym in self.non_terminals:
                term = None
                token, kind = tokens[ptr]
                for terminal in self.terminals:
                    if terminal.fit(token, kind):
                        term = terminal
                if term is None:
                    raise ParserError(ptr, "unknown token")

                if (sym, term) not in self.parsing_table:
                    raise ParserError(ptr, "invalid token")

                rule = self.parsing_table[(sym, term)]
                if rule is Symbol.eps:
                    continue
                assert rule.alpha == sym
                for beta in reversed(rule.betas):
                    stack.append(beta)
                logger.info(f"{rule.alpha} -> {rule.betas}")

        if len(stack) > 0:
            raise ParserError(ptr, "EOF reached")
        if ptr < len(tokens):
            raise ParserError(ptr, f"expected EOF, found {tokens[ptr][0]}")
