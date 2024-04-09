import string


EOF = "\xff"

alias = {
    "whitespace": " \t\f\r\n",
    "newline": "\n",
    "letter": string.ascii_letters + "_",
    "digit": string.digits,
}
