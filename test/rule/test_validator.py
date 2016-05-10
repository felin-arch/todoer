import os
import unittest

import ruamel.yaml as yaml
from ddt import ddt, unpack, data

from app.rule.validator import RuleValidator


@ddt
class TestRuleValidator(unittest.TestCase):
    def test_empty_schema_empty_rule(self):
        validator = RuleValidator({})
        result = validator.validate({})
        self.assertTrue(result['is_valid'])
        self.assertTrue(len(result['errors']) is 0)

    def test_complex_schema_complex_rule(self):
        validator = RuleValidator(load_file('files/test_schema1.yaml'))
        result = validator.validate(load_file('files/test_rule1.yaml'))
        self.assertTrue(result['is_valid'])
        self.assertTrue(len(result['errors']) is 0)

    @data(['test_invalid_rule1.yaml'],
          ['test_invalid_rule2.yaml'])
    @unpack
    def test_basic_rule_and_schema_validation_ok(self, rule_filename):
        schema = load_file('files/test_schema1.yaml')
        rule = load_file('files/' + rule_filename)
        validator = RuleValidator(schema)
        result = validator.validate(rule)
        self.assertFalse(result['is_valid'])


def load_file(path):
    contents = get_file_contents(path)
    return yaml.safe_load(contents)


def get_file_contents(path):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), path)
    with open(path) as stream:
        return stream.read()
