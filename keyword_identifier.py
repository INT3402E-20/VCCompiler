import base_classifer as bc
from int_literal import int_literal
from float_literal import float_literal

# Inherit base_classifier class for classifiying keywords, identifiers, and boolean literals (letter-first)
class keyword_identifier(bc.base_classifier):
    def __init__(self):
        super().__init__()

    # check_append() to check word/char passed is valid to append
    def check_append(self, token):
        if token in bc.letters + bc.digits:
            
            # Check first character is letter
            if not self.current_token and token not in bc.letters:
                return False
            return True
        else:
            return False
    
    # is_final() to check if current_token is a keyword, identifier, or boolean literal (final state in graph)
    def is_final(self):
        if self.current_token in bc.keywords:
            return "keyword"
        elif self.current_token in bc.boolean_literal:
            return "boolean_literal"
        elif self.current_token:
            return "identifier"
        else:
            return ""


# Testing below
text = "boolean check = false; float num = ..1E-2e\nint ui = 6"

# Define classifier (end with i), with currenti is current token type
identifi = keyword_identifier()
inti = int_literal()
floati = float_literal()
currenti = None

for i in range(text.__len__()):
    # Fit type
    if not currenti:
        # Check around all type
        is_keyide_tree = identifi.check_append(text[i])
        is_int_tree = inti.check_append(text[i])
        is_float_tree = floati.check_append(text[i])

        if is_keyide_tree:
            currenti = identifi
        elif is_int_tree:
            currenti = inti
        elif is_float_tree:
            currenti = floati

    # Check false alarm, with whitespace ending
    # TODO: Recheck whitespace dictionary + rulesets
    if currenti and currenti.false_alarm == True:
        if text[i] in bc.whitespace:
            currenti.false_alarm = False
            currenti.clear()
            currenti = None
        else:
            continue

    # For the last iteration, TODO: refactor
    if currenti and i+1 == text.__len__():
        currenti.append(text[i])
        if currenti.is_final != "":
            print(currenti.is_final() + " " + currenti.current_token)
            currenti.clear()
            currenti = None
            continue
        else:
            print("Wrong token")
            currenti.clear()
            currenti = None
            continue
    
    # Every iteration, append
    if currenti:
        currenti.append(text[i])
        if not currenti.check_append(text[i+1]): 
            if (currenti == inti and text[i+1] in bc.letters.replace('e', '').replace('E', '')) or \
                (currenti == floati and currenti.is_final() == "") or \
                (currenti.is_final() == "float_literal" and text[i+1] in bc.letters):
                    currenti.false_alarm = True
                    print("Wrong token")
                    continue

            if currenti == inti and floati.check_append(text[i+1]):
                currenti = floati
                continue

            if currenti.is_final() != "":
                print(currenti.is_final() + " " + currenti.current_token)
                currenti.clear()
                currenti = None