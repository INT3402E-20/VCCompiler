import string
from types import SimpleNamespace


__all__ = ['EOF', 'alias']

EOF = "\xff"

alias = SimpleNamespace(**{
    "whitespace": " \t\f\r\n",
    "newline": "\n",
    "letter": string.ascii_letters + "_",
    "digit": string.digits,
})
