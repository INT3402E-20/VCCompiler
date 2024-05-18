import argparse
import logging
import sys

from vccompiler.dfa import DFA
from vccompiler.exceptions import SourceError
from vccompiler.lexer import tokenize, rules
from vccompiler.lexer.token import TokenEnum
from vccompiler.ll1.grammar import LL1ParserError
from vccompiler.ll1.format import CSTFormatter

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
    parser.add_argument('--tab',
                        help='tab character',
                        type=str)
    parser.add_argument('--eol',
                        help='end of line character',
                        type=str)
    parser.add_argument('--draw', metavar='PATH',
                        help='draw parse tree to dot file',
                        type=argparse.FileType('w'))

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
    from vccompiler.parser.grammars import vc as grammar
    grammar.build()
    try:
        cst = grammar.parse(tokens)
    except LL1ParserError as e:
        raise ParserError(source, e.token.start_pos, e.what)

    # resolve left associativity
    cst.left_to_right()

    # parse tree pruning
    cst.prune()

    # draw parse tree
    if args.draw:
        cst.draw(args.draw.name)

    engine = CSTFormatter()
    if args.tab:
        engine.tab = args.tab
    if args.eol:
        engine.eol = args.eol

    args.output.write(cst.format(engine))
