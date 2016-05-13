from app.actions import Action
from app.criteria import Criterion


class Rule:
    def __init__(self, name, rule_type, criterion: Criterion, action: Action):
        self.name = name
        self.rule_type = rule_type
        self.criterion = criterion
        self.action = action

    def raw(self):
        return {
            'name': self.name,
            'type': self.rule_type,
            'criterion': self.criterion.raw(),
            'action': self.action.raw()
        }
