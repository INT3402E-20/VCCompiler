from enum import Enum

from vccompiler.exceptions import VCException
from vccompiler.lexer.token import Token, TokenEnum
from vccompiler.ll1.symbol import Symbol


class FormatEnum(Enum):
    NL = 0
    NL_SL = 1
    NL_SR = 2
    SPACE = 3
    NONE = 4


class LL1FormatterError(VCException):
    def __init__(self, what):
        self.what = what

    def __str__(self):
        return self.what


class Rule:
    def __init__(self, alpha, betas, indentation=None):
        self.lhs = alpha
        self.rhs = betas
        self.indentation = indentation

        if self.indentation is not None:
            assert len(self.rhs) == len(self.indentation) + 1


def source_format(start, transforms):
    source = ""
    TAB = "\t"
    NL = "\n"
    SPACE = " "

    stack = [start]
    ptr = 0
    indent = 0

    while len(stack) > 0:
        sym = stack.pop()
        if isinstance(sym, FormatEnum):
            if sym == FormatEnum.NL:
                source += NL
                source += TAB * indent
            elif sym == FormatEnum.NL_SL:
                if indent <= 0:
                    raise LL1FormatterError("negative indentation")
                indent -= 1
                source += NL
                source += TAB * indent
            elif sym == FormatEnum.NL_SR:
                indent += 1
                source += NL
                source += TAB * indent
            elif sym == FormatEnum.SPACE:
                source += SPACE
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

                for i in range(len(rule.rhs) - 1, -1, -1):
                    if i + 1 < len(rule.rhs):
                        if rule.indentation is not None:
                            stack.append(rule.indentation[i])
                        else:
                            stack.append(FormatEnum.SPACE)
                    stack.append(rule.rhs[i])
    return source
