import string

# List of dictionaries
keywords = ("boolean", "break", "continue", "else", "float", "for", "if", "int", "return", "void", "while")
letters = string.ascii_letters + '_'
digits = string.digits
boolean_literal = ("true", "false")

# Class for classifiying keywords, identifiers, and boolean literals (letter-first)
class keyword_identifier:

    # Curent token reading
    current_token = ""
    def __init__(self):
        pass

    # check_append() to check word/char passed is valid to append
    def check_append(self, token):
        if token in letters + digits:
            if not self.current_token and token not in letters:
                return False
            return True
        else:
            return False

    # append() to append token to current_token
    def append(self, token):
        if self.check_append(token):
            self.current_token += token
    
    # is_final() to check if current_token is a keyword, identifier, or boolean literal (final state in graph)
    def is_final(self):
        if self.current_token in keywords:
            return "keyword"
        elif self.current_token in boolean_literal:
            return "literal"
        elif self.current_token:
            return "identifier"
        else:
            return ""
    
    # clear() to clear current_token and ready for next token
    def clear(self):
        self.current_token = ""


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