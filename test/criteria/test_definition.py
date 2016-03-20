import unittest
from app.criteria.definition import CriterionDefinition
from app.criteria.logical import TrueCriterion, FalseCriterion


class TestCriterionDefinition(unittest.TestCase):
    def test_equals_true(self):
        a = CriterionDefinition(TrueCriterion, False)
        b = CriterionDefinition(TrueCriterion, False)
        self.assertTrue(a == b)
        self.assertFalse(a != b)

    def test_equals_false(self):
        a = CriterionDefinition(TrueCriterion, True)
        b = CriterionDefinition(TrueCriterion, False)
        self.assertFalse(a == b)
        self.assertTrue(a != b)

    def test_equals_different_type(self):
        a = CriterionDefinition(TrueCriterion, True)
        b = CriterionDefinition(FalseCriterion, True)
        self.assertFalse(a == b)
        self.assertTrue(a != b)
