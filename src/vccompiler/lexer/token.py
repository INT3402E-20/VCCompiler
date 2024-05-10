from enum import Enum


class TokenEnum(Enum):
    IDENTIFIER = "identifier"
    KEYWORD = "keyword"
    SEPARATOR = "separator"
    OPERATOR = "operator"
    LITERAL = "literal"
    COMMENT = "comment"
    WHITESPACE = "whitespace"
    EOF = "EOF"


class Token:
    def __init__(self, value: str, kind: TokenEnum, start_pos: int = -1):
        self.value = value
        self.kind = kind
        self.start_pos = start_pos

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"Token(\"{self.value}\", {self.kind.value}, {self.start_pos})"


globals().update(TokenEnum.__members__)
