import unittest

from app.criteria.label import *
from test.mocks import MockLabel


class TestLabelNameEqualsCriterion(unittest.TestCase):

    def test_label_name_equals_returns_True(self):
        l = MockLabel(name='name')
        lc = LabelNameEqualsCriterion('name')
        self.assertTrue(lc.applies_to(l))

    def test_label_name_does_not_equal_returns_False(self):
        l = MockLabel(name='name')
        lc = LabelNameEqualsCriterion('name_not_equal')
        self.assertFalse(lc.applies_to(l))
