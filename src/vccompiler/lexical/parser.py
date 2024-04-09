import logging
import string

from ..dfa import DFA
from .rules import comment_rule


logger = logging.getLogger(__name__)


def preprocess(source):
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

    return processed
