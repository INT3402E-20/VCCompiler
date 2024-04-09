import logging
import string

from ..dfa import DFA
from .rules import comment_rule
from . import charset


logger = logging.getLogger(__name__)


def preprocess(source):
    if any(ch not in string.printable for ch in source):
        raise RuntimeError("source contains non-printable characters")

    source += charset.EOF  # append EOF to string end
    comment_dfa = DFA([comment_rule])
    processed = ""
    source_index = 0

    while source_index < len(source):
        try:
            token_len, (token, _) = comment_dfa.search(source[source_index:])
        except RuntimeError:
            processed += source[source_index]
            source_index += 1
        else:
            source_index += token_len
            logger.debug(f"found comment: {token}")

    assert processed[-1] == charset.EOF
    processed = processed[:-1]

    return processed
