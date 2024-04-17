class State:
    none = object()

    def __init__(self, index, hook=None):
        self.id = index
        self.hook = hook
        self.transition = dict()
        self.default_transition = State.none

    def add(self, pattern, state, skip_check=False):
        for ch in pattern:
            if not skip_check and ch in self.transition:
                raise RuntimeError("duplicated transition")
            self.transition[ch] = state

    def default(self, state, skip_check=False):
        if not skip_check and self.default_transition is not State.none:
            raise RuntimeError("duplicated transition")
        self.default_transition = state

    def copy(self, new_id=-1):
        state = State(new_id, self.hook)
        state.transition = self.transition.copy()
        state.default_transition = self.default_transition
        return state

    def consume(self, ch):
        return self.transition.get(ch, self.default_transition)

    def insert_keyword(self, keyword, index, hook):
        state = self
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

    def is_end_state(self):
        return self.hook is not None

    def __str__(self):
        return str(self.id)


def EndState(index, hook):
    return State(index, hook)
