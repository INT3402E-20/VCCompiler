import argparse
import logging
import sys

from ..dfa import DFA
from . import rules
from .token_types import TokenEnum
from .util import tokenize


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

    # create DFA based on the specified rule
    dfa = DFA(rules.vc)

    tokens = tokenize(args.input.read(), dfa)

    for token, kind in tokens:
        # skip whitespaces and comments
        if kind != TokenEnum.WHITESPACE and kind != TokenEnum.COMMENT:
            print(token, file=args.output)
