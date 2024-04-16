from enum import Enum


class TokenEnum(Enum):
    IDENTIFIER = "identifier"
    KEYWORD = "keyword"
    SEPARATOR = "separator"
    OPERATOR = "operator"
    LITERAL = "literal"
    COMMENT = "comment"
    WHITESPACE = "whitespace"
