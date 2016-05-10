from app.criteria import Criterion
from app.actions import Action


class Rule:
    def __init__(self, name, rule_type, criterion: Criterion, action: Action):
        self.name = name
        self.rule_type = rule_type
        self.criterion = criterion
        self.action = action
