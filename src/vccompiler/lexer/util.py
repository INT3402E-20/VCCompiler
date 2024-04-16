import logging

from ..dfa import State
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


def insert_keyword(state, keyword, index, hook):
    for pos, ch in enumerate(keyword):
        old_state = state.consume(ch)

        # clone old state
        if old_state != State.none:
            new_state = old_state.copy()
        else:
            new_state = State(-1)

        if pos + 1 == len(keyword):
            # overwrite the hook (token type), if we reach the last character
            new_state.hook = hook
            new_state.id = index

        # create transition from current state
        state.add(ch, new_state, skip_check=True)
        state = new_state
    return state
