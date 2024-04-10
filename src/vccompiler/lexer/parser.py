import logging
import string

from ..dfa import DFA
from . import rules
from .charset import *


logger = logging.getLogger(__name__)


def preprocess(source):
    dfa = rules.dfa
    source_index = 0
    token_list = []

    while source_index < len(source):
        token, (evaluated, kind) = dfa.search(source[source_index:])
        source_index += len(token)
        token_list.append((token, evaluated, kind))
        logger.debug(f"found {kind.value}: {repr(token)}")

    return token_list
