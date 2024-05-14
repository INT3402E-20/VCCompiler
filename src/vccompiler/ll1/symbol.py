from vccompiler.lexer.token import Token, TokenEnum


class Symbol:
    def __init__(self, name, hook=None):
        self.name = name
        self.hook = hook

    def __repr__(self):
        return f"Symbol(\"{self.name}\")"

    @property
    def is_terminal(self):
        return self.hook is not None

    def fit(self, token: Token):
        assert self.is_terminal

        if isinstance(self.hook, TokenEnum):
            return token.kind == self.hook
        if isinstance(self.hook, str):
            return token.value == self.hook

        assert False


class EpsSymbol(Symbol):
    def __str__(self):
        return "ε"

    @property
    def is_terminal(self):
        return False

    def fit(self, token: Token):
        raise NotImplementedError


Symbol.eps = EpsSymbol("EPS")
