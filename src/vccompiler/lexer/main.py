from ..dfa import DFA
from . import rules

import argparse
import logging
import sys

from .token import TokenEnum


logger = logging.getLogger()


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
    source = args.input.read()
    source_index = 0

    # loop until EOF
    while source_index < len(source):
        # find the longest unique matching token from the current position
        token, (evaluated, kind) = dfa.search(source[source_index:])
        # raise the current position
        source_index += len(token)
        logger.debug(f"found {kind.value}: {repr(token)}, evaluated {repr(evaluated)}")

        # skip whitespace and comment
        if kind == TokenEnum.WHITESPACE or kind == TokenEnum.COMMENT:
            continue

        print(token, file=args.output)
