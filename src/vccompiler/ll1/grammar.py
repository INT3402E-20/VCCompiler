class Rule:
    def __init__(self, alpha, betas):
        self.alpha = alpha
        self.betas = betas


class LL1Grammar:
    def __init__(self, start):
        self.start = start
        self.production_rules = []

    def add_rule(self, alpha, *betas):
        rule = Rule(alpha, betas)
        self.production_rules.append(rule)

    def build_first(self):
        pass

    def build_follow(self):
        pass

    def build_ll1(self):
        pass
