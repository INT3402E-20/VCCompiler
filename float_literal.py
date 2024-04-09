import base_classifer as bc

class float_literal(bc.base_classifier):
    def __init__(self):
        super().__init__()

    # check_append() to check word/char passed is valid to append
    def check_append(self, token):
        if token in bc.digits:
            return True
        elif token == '.':
            if (self.current_token[-1] in bc.digits) and ('.' not in self.current_token) and ('e' not in self.current_token) and ('E' not in self.current_token):
                return True
        elif token == 'e' or token == 'E':
            if (self.current_token[-1] in bc.digits):
                return True
        elif token == '+' or token == '-':
            if ('e' in self.current_token or 'E' in self.current_token) and (self.current_token[-1] in ('e', 'E')):
                return True
        else:
            return False
        
    # is_final() to check if current_token is a keyword, identifier, or boolean literal (final state in graph)
    def is_final(self):
        if self.current_token and ('.' in self.current_token or 'e' in self.current_token or 'E' in self.current_token)and self.current_token[-1] not in ('e', 'E', '+', '-'):
            return "float_literal"
        else:
            return ""