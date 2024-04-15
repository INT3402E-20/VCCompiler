from ...dfa import EndState, State
from ..token import TokenEnum
from ..charset import alias


class KeywordGenerator:
    def __init__(self):
        self.initial_state = State(0)
        self.fallback_state = EndState(1, identifier_cb)
        self.states = []
        self.index = 1

    def add_keyword(self, keyword, callback):
        state = self.initial_state
        for pos, ch in enumerate(keyword):
            next_state = state.consume(ch)
            if next_state == State.none:
                self.index += 1
                if pos + 1 == len(keyword):
                    # last character, match the callback
                    new_state = EndState(self.index, callback)
                    # print(f"id{self.index - 1}((({self.index - 1})))") # mermaid gen
                else:
                    # not the last character, so any up til here is identifier
                    new_state = EndState(self.index, identifier_cb)
                    # print(f"id{self.index - 1}(({self.index - 1}))") # mermaid gen
                state.add(ch, new_state)
                # print(f"id{state.id - 1 if state.id != 0 else 0}-->|{ch}|id{new_state.id - 1}") # mermaid gen
                self.states.append(new_state)
                next_state = new_state
            state = next_state

    def add_fallback_to_all(self):
        # browse through all states including initial one and add fallback to all of them
        for state in [self.initial_state] + self.states:

            # get all characters that are not in the transition
            fall_ch = []
            for ch in state.transition:
                if ch not in fall_ch:
                    fall_ch.append(ch)
            removers = alias.letter
            for ch in fall_ch:
                removers = removers.replace(ch, "")
            
            # for the initial, we want to input letter only
            if state.id == 0:
                state.add(removers, self.fallback_state)
            else:
                state.add(removers + alias.digit, self.fallback_state)

    def get_state_list(self):
        return self.states

    def get_initial_state(self):
        return self.initial_state


def keyword_cb(token):
    return token, TokenEnum.KEYWORD

def identifier_cb(token):
    return token, TokenEnum.IDENTIFIER


keyword_generator = KeywordGenerator()

KEYWORDS = ["boolean", "break", "continue", "else", "float", "for","if", "int", "return", "void", "while"]

for keyword in KEYWORDS:
    keyword_generator.add_keyword(keyword, keyword_cb)

keyword_generator.add_keyword("true", lambda token: (token, TokenEnum.LITERAL))
keyword_generator.add_keyword("false", lambda token: (token, TokenEnum.LITERAL))
keyword_generator.add_fallback_to_all()

# repeat EndState as if there still identifier
keyword_generator.fallback_state.add(alias.letter + alias.digit, keyword_generator.fallback_state)

states = keyword_generator.get_state_list()
state0 = keyword_generator.get_initial_state()
