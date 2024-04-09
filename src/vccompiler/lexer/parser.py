import logging
import string

from ..dfa import DFA
from . import rules
from .charset import *


logger = logging.getLogger(__name__)


def preprocess(source):
    if any(ch not in string.printable for ch in source):
        raise RuntimeError("source contains non-printable characters")

    source += EOF   # append EOF to string end
    comment_dfa = DFA([rules.comment])
    processed = ""
    source_index = 0

    while source_index < len(source):
        try:
            token, _ = comment_dfa.search(source[source_index:])
        except RuntimeError:
            processed += source[source_index]
            source_index += 1
        else:
            source_index += len(token)
            logger.debug(f"found comment: {repr(token)}")

    assert processed[-1] == EOF
    processed = processed[:-1]

    return processed


def evaluate(source):
    source += EOF

    dfa = rules.dfa
    source_index = 0
    token_list = []

    while source[source_index] != EOF:
        token, (evaluated, kind) = dfa.search(source[source_index:])
        source_index += len(token)
        token_list.append((token, evaluated, kind))
        logger.debug(f"found {kind.value}: {repr(token)}")

    return token_list
