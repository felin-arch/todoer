import unittest
from unittest.mock import MagicMock

from app.rule import Rule
from app.rule.factory import RuleFactory, InvalidRuleError


class TestRuleFactory(unittest.TestCase):
    def setUp(self):
        self.rule_validator = MagicMock()
        self.criterion_factory = MagicMock()
        self.action_factory = MagicMock()
        self.rule_factory = RuleFactory(
            self.rule_validator, self.criterion_factory, self.action_factory
        )

    def test_create_given_invalid_rule_definition_throws_error(self):
        self.rule_validator.validate.return_value = {'is_valid': False, 'errors': [1, 2, 3]}
        with self.assertRaises(InvalidRuleError) as ctx:
            self.rule_factory.create('invalid_rule')

        self.rule_validator.validate.assert_called_with('invalid_rule')
        self.assertEquals(ctx.exception.errors, [1, 2, 3])

    def test_create_given_good_rule_definition_correctly_creates_rule(self):
        self.rule_validator.validate.return_value = {'is_valid': True, 'errors': []}
        self.criterion_factory.create.return_value = 'created_criterion'
        self.action_factory.create.return_value = 'created_action'
        rule = self.rule_factory.create({
            'name': 'Rule name #1',
            'type': 'item',
            'criterion': {
                'item_has_due_date': ''
            },
            'action': {
                'add_label_to_item': 'label #1'
            }
        })

        self.criterion_factory.create.assert_called_with({'item_has_due_date': ''})
        self.action_factory.create.assert_called_with({'add_label_to_item': 'label #1'})
        self.assertRule(rule)

    def assertRule(self, rule):
        self.assertIsInstance(rule, Rule)
        self.assertEquals('Rule name #1', rule.name)
        self.assertEquals('item', rule.rule_type)
        self.assertEquals('created_criterion', rule.criterion)
        self.assertEquals('created_action', rule.action)
