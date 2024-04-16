import logging


logger = logging.getLogger(__name__)


def tokenize(source, dfa):
    source_index = 0
    tokens = []

    # loop until EOF
    while source_index < len(source):
        # find the longest unique matching token from the current position
        token, kind = dfa.search(source[source_index:])
        # raise the current position
        source_index += len(token)
        logger.info(f"found {kind.value}: {repr(token)}")

        tokens.append((token, kind))
    return tokens
