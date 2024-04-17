from ..dfa import State


def insert_keyword(state, keyword, index, hook):
    for ch in keyword:
        old_state = state.consume(ch)

        # clone old state
        if old_state != State.none:
            new_state = old_state.copy()
        else:
            new_state = State(-1)

        # create transition from current state
        state.add(ch, new_state, skip_check=True)
        state = new_state

    # overwrite the hook (token type) of the last state
    state.hook = hook
    state.id = index
    return state
