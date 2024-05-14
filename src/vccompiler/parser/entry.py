import argparse
import logging
import sys

from vccompiler.dfa import DFA
from vccompiler.exceptions import SourceError
from vccompiler.lexer import tokenize, rules
from vccompiler.lexer.token import TokenEnum
from vccompiler.ll1.grammar import LL1ParserError
from vccompiler.ll1.format import source_format
from vccompiler.parser import grammars


logger = logging.getLogger(__name__)


class ParserError(SourceError):
    pass


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

    source = args.input.read()
    tokens = tokenize(source, DFA(rules.vc))

    # filter whitespaces and comments
    tokens = [token for token in tokens if token.kind != TokenEnum.WHITESPACE and token.kind != TokenEnum.COMMENT]

    # retrieve default grammar
    grammar = grammars.vc
    grammar.build()
    try:
        transforms = grammar.parse(tokens)
    except LL1ParserError as e:
        raise ParserError(source, e.token.start_pos, e.what)

    args.output.write(source_format(grammar.start, transforms))
