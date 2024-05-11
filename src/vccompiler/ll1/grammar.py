import logging
from vccompiler.exceptions import VCException
from vccompiler.lexer.charset import EOF
from vccompiler.lexer.token import Token, TokenEnum
from vccompiler.ll1.production import Rule
from vccompiler.ll1.symbol import Symbol


logger = logging.getLogger(__name__)


class LL1ParserError(VCException):
    def __init__(self, token, what):
        self.token = token
        self.what = what

    def __str__(self):
        return self.what


class LL1Grammar:
    def __init__(self, start):
        self.production_rules = []
        self.first_table = None
        self.follow_table = None
        self.parsing_table = None
        self.terminals = set()
        self.non_terminals = set()
        self.literal_symbols = {}
        self.token_enum_symbols = {}

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
            sym = self.literal_symbols.get(sym, Symbol(sym, sym))
            self.terminals.add(sym)
        if isinstance(sym, TokenEnum):
            sym = self.token_enum_symbols.get(sym, Symbol(sym.value, sym))
            self.terminals.add(sym)
        return sym

    def add_rule(self, alpha, *betas, **kwargs):
        alpha = self.add_symbol(alpha)
        betas = [self.add_symbol(beta) for beta in betas]
        rule = Rule(alpha, betas, **kwargs)
        self.production_rules.append(rule)

    def get_first(self, *syms):
        first_set = set()
        nullable = True
        for sym in syms:
            if nullable:
                # append first(Ai) - {eps} if eps in first(Aj) for all j < i
                first_set |= self.first_table[sym]
            nullable = nullable and Symbol.eps in self.first_table[sym]
        first_set.discard(Symbol.eps)
        if nullable:
            # append eps if eps in first(Ai) for all i
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
                # first(A) -> first(X) for X -> A
                for sym in self.get_first(*rule.rhs):
                    update(rule.lhs, sym)

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
                for i, beta in enumerate(rule.rhs):
                    if beta in self.non_terminals:
                        first_set = self.get_first(*rule.rhs[i + 1:])
                        # follow(b) - {eps} -> follow(X) for each A -> aXb
                        for sym in first_set:
                            if sym is not Symbol.eps:
                                update(beta, sym)
                        # follow(A) -> follow(X) for each A -> aXb where eps in first(b)
                        if Symbol.eps in first_set:
                            for sym in self.follow_table[rule.lhs]:
                                update(beta, sym)

    def build_ll1(self):
        self.parsing_table = dict()

        def update(alpha, sym, entry):
            assert (alpha, sym) not in self.parsing_table
            self.parsing_table[(alpha, sym)] = entry

        for rule in self.production_rules:
            first_set = self.get_first(*rule.rhs)
            for sym in first_set:
                if sym in self.terminals:
                    update(rule.lhs, sym, rule)
            if Symbol.eps in first_set:
                for sym in self.follow_table[rule.lhs]:
                    update(rule.lhs, sym, Symbol.eps)

    def build(self):
        self.build_first()
        self.build_follow()
        self.build_ll1()

    def parse(self, tokens):
        tokens.append(Token(EOF, TokenEnum.EOF))
        stack = [self.start]
        transforms = []

        ptr = 0
        while len(stack) > 0 and ptr < len(tokens):
            sym = stack.pop()
            if sym in self.terminals:
                # the token must match the terminal symbol
                token = tokens[ptr]
                if sym.fit(token):
                    ptr += 1
                    transforms.append((sym, token))
                    logger.info(f"{sym} -> \"{token}\"")
                else:
                    raise LL1ParserError(token, f"expected {sym}, found \"{token}\"")
            elif sym in self.non_terminals:
                token = tokens[ptr]
                # find the terminal symbol that match the token
                matches = [term for term in self.terminals if term.fit(token)]
                if len(matches) == 0:
                    raise LL1ParserError(token, f"unknown token \"{token}\"")
                if len(matches) > 1:
                    raise LL1ParserError(token, f"ambiguous token \"{token}\"")
                term = matches.pop()

                if (sym, term) not in self.parsing_table:
                    raise LL1ParserError(token, f"invalid token \"{token}\"")

                rule = self.parsing_table[(sym, term)]
                if rule is Symbol.eps:
                    # skip the symbol if it's empty string
                    transforms.append((sym, Symbol.eps))
                    logger.info(f"{sym} -> ε")
                    continue
                assert rule.lhs == sym
                # push the production rule to the stack in reversed order
                for beta in reversed(rule.rhs):
                    stack.append(beta)

                transforms.append((sym, rule))
                logger.info(f"{sym} -> {' '.join(str(beta) for beta in rule.rhs)}")

        # this part is unreachable by design since the input was terminated with EOF token
        # we put these checks here just in case
        if len(stack) > 0:
            raise LL1ParserError(tokens[ptr], "EOF reached")
        if ptr < len(tokens):
            raise LL1ParserError(tokens[ptr], f"expected EOF, found \"{tokens[ptr]}\"")

        return transforms
