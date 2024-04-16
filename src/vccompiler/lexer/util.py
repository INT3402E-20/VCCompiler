from ..dfa import State


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
