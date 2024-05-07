from vccompiler.dfa.state import State


class DFA:
    """
    .. py:class:: DFA

    This class represents a Deterministic Finite Automaton (DFA).

    :param initial_states: The initial state(s) of the DFA.
    :type initial_states: list or State

    :ivar initial_states: List of initial states.
    :vartype initial_states: list
    """
    def __init__(self, initial_states):
        if not isinstance(initial_states, list):
            initial_states = [initial_states]
        self.initial_states = initial_states

    def search(self, content):
        """
        .. py:method:: search(content)

        Search for a valid token in the given string using the DFA.

        :param content: The input string to search.
        :type content: str

        :return: A tuple containing the valid token and the associated hook.
        :rtype: tuple(str, any)

        :raises RuntimeError: If no valid token is found (reaches a "none" state) or if the DFA is ambiguous.
        """
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
            raise RuntimeError("ambiguous dfa")

        state = filtered.pop()
        token = content[:longest_token_len]
        return token, state.hook
