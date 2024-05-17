from enum import Enum


class TokenEnum(Enum):
    IDENTIFIER = "identifier"
    KEYWORD = "keyword"
    TYPE_INIT = "type"
    SEPARATOR = "separator"
    OPERATOR = "operator"
    INTLITERAL = "int_literal"
    FLOATLITERAL = "float_literal"
    BOOLEANLITERAL = "boolean_literal"
    STRINGLITERAL = "string_literal"
    COMMENT = "comment"
    WHITESPACE = "whitespace"
    EOF = "EOF"


class Token:
    def __init__(self, value: str, kind: TokenEnum, start_pos: int = -1):
        self.value = value
        self.kind = kind
        self.start_pos = start_pos

    def __str__(self):
        if self.kind == TokenEnum.EOF:
            return "$"
        return f"\"{self.value}\""

    def __repr__(self):
        return f"Token({self}, {self.kind.value}, {self.start_pos})"


globals().update(TokenEnum.__members__)
