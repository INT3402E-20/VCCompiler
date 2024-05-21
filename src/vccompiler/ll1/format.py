from string import Formatter

from vccompiler.lexer.token import Token, TokenEnum


class CSTFormatter:
    """
    A formatter for Concrete Syntax Trees (CSTs).

    Args:
        indent (int): The initial indentation level (default is 0).
        tab (str): The string used for indentation (default is '\\t').
        eol (str): The end-of-line character (default is '\\n').
    """
    class NodeFormatter(Formatter):
        """
        A specialized formatter for CST nodes.
        """
        def parse(self, format_string):
            """
            Parse the format string.

            Args:
                format_string (str): The format string to parse.

            Returns:
                zip: A zipped iterable of format components.
            """
            return zip(*list(zip(*super().parse(format_string)))[:2])

    def __init__(self, indent=0, tab='\t', eol='\n'):
        self.tab = tab
        self.eol = eol
        self.indent = indent

    def format(self, root):
        """
        Format a CST node.

        Args:
            root: The root node of the CST.

        Returns:
            str: The formatted source code.
        """
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
