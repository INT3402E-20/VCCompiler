from vccompiler.lexer.token import TokenEnum


class Symbol:
    eps = object()

    def __init__(self, name, hook=None):
        self.name = name
        self.hook = hook

    def __repr__(self):
        return f"Symbol(\"{self.name}\")"

    @property
    def is_terminal(self):
        return self.hook is not None

    def fit(self, token, kind):
        assert self.is_terminal

        if isinstance(self.hook, TokenEnum):
            return kind == self.hook
        if isinstance(self.hook, str):
            return token == self.hook

        assert False
