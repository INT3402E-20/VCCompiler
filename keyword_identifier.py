import base_classifer as bc

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
            return "literal"
        elif self.current_token:
            return "identifier"
        else:
            return ""


# Testing below
text = "boolean 8check = false"
identifi = keyword_identifier()
for i in range(text.__len__() - 1):
    is_keyide_tree = identifi.check_append(text[i])
    if is_keyide_tree:
        identifi.append(text[i])

        # TODO: function to identify whitespace types or detect wrong state
        # Since the function only append and not determine it should be in wrong state instead of being ready for next token
        # "8check" identifier case will fail (class take in 8 and mark wrong already, but the check behind still valid)
        # Solution: cooperate with number literal to mark the wrong state, or implement better whitespace handling
        if not identifi.check_append(text[i+1]) and identifi.is_final() != "":
            print(identifi.is_final())
            identifi.clear()
        elif i+1 == text.__len__()-1 and identifi.is_final() != "":
            identifi.append(text[i+1])
            print(identifi.is_final())
            identifi.clear()