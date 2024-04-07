import string

keywords = ("boolean", "break", "continue", "else", "float", "for", "if", "int", "return", "void", "while")
letters = string.ascii_letters + '_'
digits = string.digits
boolean_literal = ("true", "false")

class keyword_identifier:
    current_token = ""
    def __init__(self):
        pass

    def check_append(self, token):
        if token in letters + digits:
            if not self.current_token and token not in letters:
                return False
            return True
        else:
            return False

    def append(self, token):
        if self.check_append(token):
            self.current_token += token
    
    def is_final(self):
        if self.current_token in keywords:
            return "keyword"
        elif self.current_token in boolean_literal:
            return "literal"
        elif self.current_token:
            return "identifier"
        else:
            return ""
    
    def clear(self):
        self.current_token = ""

text = "boolean check = false"
identifi = keyword_identifier()
for i in range(text.__len__() - 1):
    is_keyide_tree = identifi.check_append(text[i])
    if is_keyide_tree:
        identifi.append(text[i])
        if not identifi.check_append(text[i+1]) and identifi.is_final() != "":
            print(identifi.is_final())
            identifi.clear()
        elif i+1 == text.__len__()-1 and identifi.is_final() != "":
            identifi.append(text[i+1])
            print(identifi.is_final())
            identifi.clear()