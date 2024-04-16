from .state import State


class DFA:
    def __init__(self, initial_states):
        self.initial_states = initial_states

    def search(self, content):
        end_states = []

        for state in self.initial_states:
            token_len = 0
            end_state = None

            for index, ch in enumerate(content):
                state = state.consume(ch)
                if state is State.none:
                    break
                if state.is_end_state():
                    end_state = state
                    token_len = index + 1

            if token_len > 0:
                end_states.append((token_len, end_state))

        if len(end_states) == 0:
            raise RuntimeError("none state reached")

        longest_token_len = max(token_len for token_len, _ in end_states)
        filtered = [end_state for token_len, end_state in end_states if token_len == longest_token_len]

        if len(filtered) > 1:
            raise RuntimeError("dfa error: ambiguous state")

        state = filtered.pop()
        token = content[:longest_token_len]
        return token, state.hook
