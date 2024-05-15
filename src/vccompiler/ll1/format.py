from vccompiler.lexer.token import Token, TokenEnum
from vccompiler.ll1.grammar import CSTNode
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


def source_format(root: CSTNode, indent=0):
    if isinstance(root.rule, Token):
        token = root.rule
        return "" if token.kind == TokenEnum.EOF else token.value
    if isinstance(root.rule, str):
        return root.rule

    source = ""
    child_index = 0

    for sym in root.rule.rhs_with_formatting:
        if isinstance(sym, Format):
            indent, sep = sym.execute(indent)
            source += sep
        elif isinstance(sym, Symbol):
            source += source_format(root.children[child_index], indent)
            child_index += 1
    return source
