from vccompiler.lexer.token import Token, TokenEnum
from vccompiler.ll1.grammar import Rule
from vccompiler.ll1.symbol import Symbol


class Format:
    def __init__(self, *separators):
        self.separators = separators

    def execute(self, level):
        TAB = "\t"
        NL = "\n"

        output = ""

        for sep in self.separators:
            if isinstance(sep, int):
                level += sep
                assert level >= 0
                output += NL + TAB * level
            if isinstance(sep, str):
                output += sep
        return level, output


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
