import base_classifer as bc

class float_literal(bc.base_classifier):
    def __init__(self):
        super().__init__()

    # check_append() to check word/char passed is valid to append
    def check_append(self, token):
        if token in bc.digits:
            return True
        elif token == '.':
            if ('.' not in self.current_token) and ('e' not in self.current_token) and ('E' not in self.current_token):
                return True
        elif token == 'e' or token == 'E':
            if (self.current_token) and (self.current_token[-1] in bc.digits) and ('e' not in self.current_token) \
                and ('E' not in self.current_token):
                    return True
        elif token == '+' or token == '-':
            if ('e' in self.current_token or 'E' in self.current_token) and (self.current_token[-1] in ('e', 'E')):
                return True
        else:
            return False
        
    # is_final() to check if current_token is a float literal (final state in graph)
    def is_final(self):
        if (len(self.current_token) == 1 and self.current_token in ('.', 'e', 'E', '+', '-')) or (not self.current_token or \
            ('.' not in self.current_token and 'e' not in self.current_token and 'E' not in self.current_token) or \
            self.current_token[-1] in ('e', 'E', '+', '-')):
                return ""
        else:
            return "float_literal"