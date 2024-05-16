from string import Formatter

from vccompiler.lexer.token import Token, TokenEnum


class CSTFormatter:
    class NodeFormatter(Formatter):
        def parse(self, format_string):
            return zip(*list(zip(*super().parse(format_string)))[:2])

    def __init__(self, indent=0, tab='\t', eol='\n'):
        self.tab = tab
        self.eol = eol
        self.indent = indent

    def format(self, root):
        if isinstance(root.rule, Token):
            token = root.rule
            return "" if token.kind == TokenEnum.EOF else token.value
        if isinstance(root.rule, str):
            return root.rule
        if "formatter" not in root.semantics:
            return "".join(self.format(child) for child in root.children)

        formatter = CSTFormatter.NodeFormatter()
        format_spec = root.semantics["formatter"]
        source = ""

        indent_rule = {">": 1, "=": 0, "<": -1}

        for sep, fmt in formatter.parse(format_spec):
            source += sep
            if fmt in indent_rule:
                self.indent += indent_rule[fmt]
                assert self.indent >= 0
                source += self.eol + self.tab * self.indent
            elif fmt is not None:
                source += self.format(root.children[int(fmt)])

        return source
