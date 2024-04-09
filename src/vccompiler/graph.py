class State:
    none = object()

    def __init__(self, id):
        self.id = id
        self.transition = dict()
        self.default_transition = State.none

    def add_transition(self, pattern, state):
        for ch in pattern:
            if ch in self.transition:
                raise RuntimeError("duplicated transition")
            self.transition[ch] = state
    
    def add_negative_transition(self, pattern):
        for ch in pattern:
            if ch in self.transition:
                raise RuntimeError("duplicated transition")
            self.transition[ch] = State.none
    
    def set_default_transition(self, state):
        self.default_transition = state

    def consume(self, ch):
        return self.transition.get(ch, self.default_transition)

    def is_end_state(self):
        return False


class EndState(State):
    def __init__(self, id, cb):
        super().__init__(id)
        self.cb = cb

    def is_end_state(self):
        return True

    def callback(self, token):
        return self.cb(token)
