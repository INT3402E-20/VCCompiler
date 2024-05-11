from enum import Enum

from vccompiler.exceptions import VCException
from vccompiler.lexer.token import Token, TokenEnum
from vccompiler.ll1.symbol import Symbol


class Format:
    def __init__(self, sep=" "):
        self.sep = sep

    def execute(self, level):
        TAB = "\t"
        NL = "\n"

        if isinstance(self.sep, int):
            new_indent = level + self.sep
            assert new_indent >= 0
            return new_indent, NL + TAB * new_indent
        if isinstance(self.sep, str):
            return level, self.sep


class Rule:
    def __init__(self, alpha, betas):
        self.lhs = alpha
        self.rhs_with_formatting = betas

    @property
    def rhs(self):
        return [beta for beta in self.rhs_with_formatting if not isinstance(beta, Format)]


def source_format(start, transforms):
    source = ""

    stack = [start]
    ptr = 0
    indent = 0

    while len(stack) > 0:
        sym = stack.pop()
        if isinstance(sym, Format):
            indent, sep = sym.execute(indent)
            source += sep
        elif isinstance(sym, Symbol):
            assert ptr < len(transforms)
            transform = transforms[ptr]
            ptr += 1

            assert transform[0] == sym

            if isinstance(transform[1], Token):
                if transform[1].kind != TokenEnum.EOF:
                    source += transform[1].value
            elif isinstance(transform[1], Symbol):
                assert transform[1] is Symbol.eps
            elif isinstance(transform[1], Rule):
                rule = transform[1]
                assert sym == rule.lhs

                stack.extend(reversed(rule.rhs_with_formatting))
    return source
