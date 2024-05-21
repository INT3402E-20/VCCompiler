import logging
from vccompiler.exceptions import VCException
from vccompiler.lexer.charset import EOF
from vccompiler.lexer.token import Token, TokenEnum
from vccompiler.ll1.cst import CST
from vccompiler.ll1.rule import Rule, RuleGenerator
from vccompiler.ll1.symbol import Symbol


logger = logging.getLogger(__name__)


class LL1ParserError(VCException):
    def __init__(self, token, what):
        self.token = token
        self.what = what

    def __str__(self):
        return self.what


class LL1GrammarError(VCException):
    pass


class LL1Grammar:
    """
    Represents an LL(1) grammar.

    Args:
        start: The start symbol for the grammar.
        conflict_handler: A custom conflict handler (optional).
        **semantics: Additional semantic information (optional).
    """
    def __init__(self, start, conflict_handler=None, **semantics):
        self.production_rules = []
        self.first_table = None
        self.follow_table = None
        self.parsing_table = None
        self.terminals = set()
        self.non_terminals = set()
        self.conflict_handler = conflict_handler
        self.semantics = semantics

        self.start = Symbol("grammar-start")
        eof = Symbol("EOF", EOF)
        self.add_rule(Rule(self.start, (start, eof)))

    def add_symbol(self, sym):
        """
        Add a symbol to the grammar.

        Args:
            sym: The symbol to add.
        """
        assert isinstance(sym, Symbol)
        if sym.is_terminal:
            self.terminals.add(sym)
        else:
            self.non_terminals.add(sym)

    def add_rule(self, rule: Rule):
        """
        Add a production rule to the grammar.

        Args:
            rule: The production rule to add.
        """
        self.add_symbol(rule.lhs)
        for beta in rule.rhs:
            self.add_symbol(beta)
        self.production_rules.append(rule)

    def get_first(self, *syms):
        """
        Compute the FIRST set for a sequence of symbols.

        Args:
            syms: The symbols for which to compute the FIRST set.

        Returns:
            set: The computed FIRST set.
        """
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
        """
        Compute the FIRST sets for all symbols in the grammar.
        """
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
                    logger.debug(f"LL1 First updates {alpha}, {sym}")
                    self.first_table[alpha].add(sym)
                    stopped = False

            for rule in self.production_rules:
                # first(A) -> first(X) for X -> A
                for sym in self.get_first(*rule.rhs):
                    update(rule.lhs, sym)

    def build_follow(self):
        """
        Compute the FOLLOW sets for all non-terminal symbols in the grammar.
        """
        self.follow_table = {}
        for sym in self.non_terminals:
            self.follow_table[sym] = set()

        stopped = False
        while not stopped:
            stopped = True

            def update(alpha, sym):
                nonlocal stopped
                if sym not in self.follow_table[alpha]:
                    logger.debug(f"LL1 Follow updates {alpha}, {sym}")
                    self.follow_table[alpha].add(sym)
                    stopped = False

            for rule in self.production_rules:
                for i, beta in enumerate(rule.rhs):
                    if beta in self.non_terminals:
                        first_set = self.get_first(*rule.rhs[i + 1:])
                        # first(b) - {eps} -> follow(X) for each A -> aXb
                        for sym in first_set:
                            if sym is not Symbol.eps:
                                update(beta, sym)
                        # follow(A) -> follow(X) for each A -> aXb where eps in first(b)
                        if Symbol.eps in first_set:
                            for sym in self.follow_table[rule.lhs]:
                                update(beta, sym)

    def build_ll1(self):
        """
        Compute the LL1 table.
        """
        self.parsing_table = dict()

        def update(alpha, sym, entry):
            logger.debug(f"LL1 table updates ({alpha}, {sym}) = {entry}")
            try:
                # workaround for dangling else
                old_entry = self.parsing_table[(alpha, sym)]
                if self.conflict_handler is not None:
                    self.parsing_table[(alpha, sym)] = self.conflict_handler(alpha, sym, old_entry, entry)
                    logger.warning(f"conflict handled at ({alpha}, {sym}) = {self.parsing_table[(alpha, sym)]}")
                else:
                    raise LL1GrammarError(f"table conflict at ({alpha}, {sym})")
            except KeyError:
                self.parsing_table[(alpha, sym)] = entry

        for rule in self.production_rules:
            first_set = self.get_first(*rule.rhs)
            for sym in first_set:
                # table[A, t] = X for all terminal t in first(X), A -> X
                if sym in self.terminals:
                    update(rule.lhs, sym, rule)
            if Symbol.eps in first_set:
                # if eps in first(X)
                for sym in self.follow_table[rule.lhs]:
                    # table[A, t] = X for all terminal t in follow(X) if eps in first(X), A -> X
                    update(rule.lhs, sym, Symbol.eps)

    def build(self):
        self.build_first()
        self.build_follow()
        self.build_ll1()

    def parse(self, tokens):
        """
        Parse the given sequence of tokens.
        :param tokens:
        :return: generated parse tree
        """
        tokens.append(Token(EOF, TokenEnum.EOF))
        tree = CST(self.semantics)
        stack = [(self.start, tree.root)]

        ptr = 0
        while len(stack) > 0 and ptr < len(tokens):
            sym, node = stack.pop()
            if sym in self.terminals:
                # the token must match the terminal symbol
                token = tokens[ptr]
                if sym.fit(token):
                    ptr += 1
                    node.rule = token
                    logger.info(f"{sym} -> {token}")
                else:
                    raise LL1ParserError(token, f"expected {sym}, found {token}")
            elif sym in self.non_terminals:
                token = tokens[ptr]
                # find the terminal symbol that match the token
                matches = [term for term in self.terminals if term.fit(token)]
                if len(matches) == 0:
                    raise LL1ParserError(token, f"unknown token {token}")
                if len(matches) > 1:
                    raise LL1ParserError(token, f"ambiguous token {token}")
                term = matches.pop()

                if (sym, term) not in self.parsing_table:
                    raise LL1ParserError(token, f"invalid token {token}")

                rule = self.parsing_table[(sym, term)]
                if rule is Symbol.eps:
                    # skip the symbol if it's empty string
                    node.rule = ""
                    logger.info(f"{sym} -> ε")
                    continue
                assert rule.lhs == sym

                for _ in range(len(rule.rhs)):
                    node.add_child(tree.new_node())

                # push the production rule to the stack in reversed order
                stack.extend(reversed(list(zip(rule.rhs, node.children))))

                node.rule = rule
                logger.info(rule)

        # this part is unreachable by design since the input was terminated with EOF token
        # we put these checks here just in case
        if len(stack) > 0:
            raise LL1ParserError(tokens[ptr], "EOF reached")
        if ptr < len(tokens):
            raise LL1ParserError(tokens[ptr], f"expected EOF, found {tokens[ptr]}")

        return tree

    @staticmethod
    def from_yaml(file):
        """
        Generate LL1 grammar given a YAML file.
        :param file:
        :return:
        """
        try:
            from yaml import safe_load
        except ImportError:
            logger.error("YAML import requires PyYAML to be installed")
            return

        parsed = safe_load(file)
        R = RuleGenerator()
        rules = []
        symbol_maps = {}

        for name, hook in parsed["symbols"].items():
            if hook is not None:
                if hook.startswith("\""):
                    hook = hook[1:-1]
                elif hook.startswith("T."):
                    hook = TokenEnum[hook[2:]]
            symbol = Symbol(name, hook=hook)
            assert name not in symbol_maps
            symbol_maps[name] = symbol

        for rule in parsed["rules"]:
            args = []
            for sym in rule["R"]:
                if sym.startswith("\""):
                    sym = sym[1:-1]
                elif sym.startswith("T."):
                    sym = TokenEnum[sym[2:]]
                elif sym == "S.eps":
                    sym = Symbol.eps
                else:
                    sym = symbol_maps[sym]
                args.append(sym)
            kwargs = rule.copy()
            kwargs.pop("R")
            rules.append(R(*args, **kwargs))

        grammar = parsed["grammar"].copy()
        start = symbol_maps[grammar.pop("start")]
        if "conflict_handler" in grammar and grammar["conflict_handler"] == "dangling_else_handler":
            from vccompiler.parser.grammars.vc import dangling_else_handler
            grammar["conflict_handler"] = dangling_else_handler
        grammar = LL1Grammar(start, **grammar)

        for rule in rules:
            grammar.add_rule(rule)

        return grammar
