from app.actions.factory import ActionFactory
from app.criteria.factory import CriterionFactory
from app.rule import Rule
from app.rule.validator import RuleValidator


class RuleFactory:
    def __init__(self, rule_validator: RuleValidator, criterion_factory: CriterionFactory,
                 action_factory: ActionFactory):
        self._rule_validator = rule_validator
        self._criterion_factory = criterion_factory
        self._action_factory = action_factory

    def create(self, rule_definition):
        self._validate_rule(rule_definition)
        return Rule(
            rule_definition['name'],
            rule_definition['type'],
            self._criterion_factory.create(rule_definition['criterion']),
            self._action_factory.create(rule_definition['action'])
        )

    def _validate_rule(self, rule_definition):
        validation_result = self._rule_validator.validate(rule_definition)
        if not validation_result['is_valid']:
            raise InvalidRuleError(validation_result['errors'])


class InvalidRuleError(RuntimeError):
    def __init__(self, errors):
        super().__init__()
        self.errors = errors
