class State:
    """
    .. py:class:: State

    This class represents a state in a Deterministic Finite Automaton (DFA).

    :param index: The unique identifier for the state.
    :type index: int

    :param hook: An optional hook associated with the state (e.g., token type).
    :type hook: callable or None

    :ivar id: The unique identifier for the state.
    :vartype id: int

    :ivar hook: The associated hook (e.g., token type) for the state.
    :vartype hook: callable or None

    :ivar transition: A dictionary representing transitions from the current state to other states.
    :vartype transition: dict

    :ivar default_transition: The default transition state when no specific transition is defined.
    :vartype default_transition: State
    """
    none = object()

    def __init__(self, index, hook=None):
        self.id = index
        self.hook = hook
        self.transition = dict()
        self.default_transition = State.none

    def add(self, pattern, state, skip_check=False):
        """
        .. py:method:: add(pattern, state, skip_check=False)

        Add a transition from the current state to another state based on a pattern.

        :param pattern: The input pattern (e.g., character) triggering the transition.
        :type pattern: str

        :param state: The target state for the transition.
        :type state: State

        :param skip_check: If True, skip duplicate transition checks (default is False).
        :type skip_check: bool
        """
        for ch in pattern:
            if not skip_check and ch in self.transition:
                raise RuntimeError("duplicated transition")
            self.transition[ch] = state

    def default(self, state, skip_check=False):
        """
        .. py:method:: default(state, skip_check=False)

        Set the default transition state when no specific transition is defined.

        :param state: The default target state.
        :type state: State

        :param skip_check: If True, skip duplicate transition checks (default is False).
        :type skip_check: bool
        """
        if not skip_check and self.default_transition is not State.none:
            raise RuntimeError("duplicated transition")
        self.default_transition = state

    def copy(self, new_id=-1):
        """
        .. py:method:: copy(new_id=-1)

        Clone the current state with an optional new identifier.

        :param new_id: The new identifier for the copied state (default is -1).
        :type new_id: int

        :return: A new state with copied transition information.
        :rtype: State
        """
        state = State(new_id, self.hook)
        state.transition = self.transition.copy()
        state.default_transition = self.default_transition
        return state

    def consume(self, ch):
        """
        .. py:method:: consume(ch)

        Determine the next state based on the input character.

        :param ch: The input character.
        :type ch: str

        :return: The next state after consuming the character.
        :rtype: State
        """
        return self.transition.get(ch, self.default_transition)

    def insert_keyword(self, keyword, index, hook):
        """
        .. py:method:: insert_keyword(keyword, index, hook)

        Insert a keyword into the DFA by creating transitions and updating hooks.

        :param keyword: The keyword to insert.
        :type keyword: str

        :param index: The unique identifier for the keyword.
        :type index: int

        :param hook: The associated hook (e.g., token type) for the keyword.
        :type hook: callable

        :return: The final state after inserting the keyword.
        :rtype: State
        """
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
        """
        .. py:method:: is_end_state()

        Check if the current state is an end state (has an associated hook).

        :return: True if the state is an end state, False otherwise.
        :rtype: bool
        """
        return self.hook is not None

    def __str__(self):
        return str(self.id)


def EndState(index, hook):
    """
    .. py:function:: EndState(index, hook)

    Create an end state with the specified index and hook.

    :param index: The unique identifier for the end state.
    :type index: int

    :param hook: The associated hook (e.g., token type) for the end state.
    :type hook: callable

    :return: An end state.
    :rtype: State
    """
    return State(index, hook)
