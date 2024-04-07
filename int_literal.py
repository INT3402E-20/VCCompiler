import base_classifer as bc

class int_literal(bc.base_classifier):
    def __init__(self):
        super().__init__()

    # check_append() to check word/char passed is valid to append
    def check_append(self, token):
        if token in bc.digits:
            return True
        else:
            return False
    
    # is_final() to check if current_token is a keyword, identifier, or boolean literal (final state in graph)
    def is_final(self):
        if self.current_token:
            return "int_literal"
        else:
            return ""