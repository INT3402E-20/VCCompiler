import argparse
import logging
import sys

from ..dfa import DFA
from . import rules
from .token_types import TokenEnum
from ..exceptions import VCSourceError


logger = logging.getLogger(__name__)


class LexerError(VCSourceError):
    pass


def tokenize(source, dfa):
    source_index = 0
    tokens = []

    # loop until EOF
    while source_index < len(source):
        # find the longest unique matching token from the current position
        try:
            token, kind = dfa.search(source[source_index:])
        except RuntimeError as err:
            raise LexerError(source, source_index, err) from None
        # raise the current position
        source_index += len(token)
        logger.info(f"found {kind.value}: {repr(token)}")

        tokens.append((token, kind))
    return tokens


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
    parser.add_argument('-r', '--rule',
                        help='rules file')
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
    if args.rule:
        import importlib.util
        spec = importlib.util.spec_from_file_location("", args.rule)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        dfa = DFA(module.rule)
    else:
        # use default rule
        dfa = DFA(rules.vc)

    tokens = tokenize(args.input.read(), dfa)

    for token, kind in tokens:
        # skip whitespaces and comments
        if kind != TokenEnum.WHITESPACE and kind != TokenEnum.COMMENT:
            print(token, file=args.output)
