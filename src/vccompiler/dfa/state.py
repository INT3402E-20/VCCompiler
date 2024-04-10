class State:
    none = object()

    def __init__(self, index):
        self.id = index
        self.transition = dict()
        self.default_transition = State.none

    def add(self, pattern, state):
        for ch in pattern:
            if ch in self.transition:
                raise RuntimeError("duplicated transition")
            self.transition[ch] = state

    def default(self, state):
        self.default_transition = state

    def consume(self, ch):
        return self.transition.get(ch, self.default_transition)

    def is_end_state(self):
        return False


class EndState(State):
    def __init__(self, index, cb):
        super().__init__(index)
        self.cb = cb

    def is_end_state(self):
        return True

    def callback(self, token):
        return self.cb(token)
