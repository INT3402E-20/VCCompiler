import string

# List of dictionaries
keywords = ("boolean", "break", "continue", "else", "float", "for", "if", "int", "return", "void", "while")
letters = string.ascii_letters + '_'
digits = string.digits
boolean_literal = ("true", "false")

# Base class for classifying
class base_classifier:

    # Curent token reading
    current_token = ""
    def __init__(self):
        pass

    # is_final(): NEED TO OVERWRITE, DEFAULT WRONG to check if it's in final state
    def is_final(self):
        return ""
    
    # clear() to clear current_token and ready for next token
    def clear(self):
        self.current_token = ""

    # check_append(): NEED TO OVERWRITE, DEFAULT FALSE to check word/char passed is valid to append
    def check_append(self, token):
        return False
    
    # append() to append token to current_token
    def append(self, token):
        self.current_token += token