from .state import State


class DFA:
    def __init__(self, initial_states):
        self.initial_states = initial_states

    def search(self, content):
        end_states = []

        for state in self.initial_states:
            token = ""

            for ch in content:
                state = state.consume(ch)
                if state is State.none:
                    break
                if state.is_end_state():
                    break
                token += ch

            if state is State.none:
                continue

            if state.is_end_state():
                end_states.append((token, state))

        if len(end_states) == 0:
            raise RuntimeError("none state reached")

        if len(end_states) > 1:
            raise RuntimeError("dfa error: ambiguous state")

        token, state = end_states.pop()
        return token, state.evaluate(token)
