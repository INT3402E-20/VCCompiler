from ...dfa import EndState, State
from ..token import TokenEnum


class KeywordGenerator:
    def __init__(self):
        self.initial_state = State(0)
        self.states = []
        self.index = 0

    def add_keyword(self, keyword, callback):
        state = self.initial_state
        for pos, ch in enumerate(keyword):
            next_state = state.consume(ch)
            if next_state == State.none:
                self.index += 1
                if pos + 1 == len(keyword):
                    # last character
                    new_state = EndState(self.index, callback)
                else:
                    # not the last character
                    new_state = State(self.index)
                state.add(ch, new_state)
                self.states.append(new_state)
                next_state = new_state
            state = next_state

    def get_state_list(self):
        return self.states

    def get_initial_state(self):
        return self.initial_state


def keyword_cb(token):
    return token, TokenEnum.KEYWORD


keyword_generator = KeywordGenerator()

KEYWORDS = ["if", "int"]

for keyword in KEYWORDS:
    keyword_generator.add_keyword(keyword, keyword_cb)

states = keyword_generator.get_state_list()
state0 = keyword_generator.get_initial_state()
