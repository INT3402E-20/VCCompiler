import argparse
import logging
import sys

from vccompiler.dfa import DFA
from vccompiler.lexer import tokenize, rules
from vccompiler.lexer.token_types import TokenEnum
from vccompiler.parser import grammars


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        help='default: WARN; (-v): INFO; (-vv): DEBUG',
                        action='count',
                        default=0)
    parser.add_argument('-o', '--output',
                        help='output file',
                        default=sys.stdout,
                        type=argparse.FileType('w'))
    parser.add_argument('input',
                        help='source file',
                        type=argparse.FileType('r'))

    args = parser.parse_args()

    # setup verbose level
    if args.verbose == 0:
        logging.basicConfig(level=logging.WARN)
    elif args.verbose == 1:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG)

    tokens = tokenize(args.input.read(), DFA(rules.vc))

    # filter whitespaces and comments
    tokens = [(token, kind) for token, kind in tokens if kind != TokenEnum.WHITESPACE and kind != TokenEnum.COMMENT]

    # retrieve default grammar
    grammar = grammars.vc
    grammar.build()
    grammar.parse(tokens)
