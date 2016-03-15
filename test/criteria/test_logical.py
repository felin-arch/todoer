import unittest
from unittest.mock import MagicMock, call

from app.criteria.logical import *
from test.mocks import MockItem, MockLabel


class TestTrueCriterion(unittest.TestCase):

    def test_is_True(self):
        tc = TrueCriterion()
        self.assertTrue(tc.applies_to(MockItem('Anything')))


class TestFalseCriterion(unittest.TestCase):

    def test_is_False(self):
        fc = FalseCriterion()
        self.assertFalse(fc.applies_to(MockItem('Anything')))


class TestAllCriterion(unittest.TestCase):

    def test_is_False_if_anything_is_False(self):
        fc = FalseCriterion()
        tc = TrueCriterion()
        ac = AllCriterion([fc, tc])
        self.assertFalse(ac.applies_to(MockItem('Anything')))

    def test_is_True_if_everything_is_True(self):
        tc = TrueCriterion()
        tc2 = TrueCriterion()
        ac = AllCriterion([tc, tc2])
        self.assertTrue(ac.applies_to(MockItem('Anything')))


class TestAnyCriterion(unittest.TestCase):

    def test_is_False_if_everything_is_False(self):
        fc = FalseCriterion()
        fc2 = FalseCriterion()
        ac = AnyCriterion([fc, fc2])
        self.assertFalse(ac.applies_to(MockItem('Anything')))

    def test_is_True_if_anything_is_True(self):
        fc = FalseCriterion()
        tc = TrueCriterion()
        ac = AnyCriterion([tc, fc])
        self.assertTrue(ac.applies_to(MockItem('Anything')))


class TestNotCriterion(unittest.TestCase):

    def test_is_True_if_inner_is_False(self):
        fc = FalseCriterion()
        nc = NotCriterion(fc)
        self.assertTrue(nc.applies_to(MockItem('Anything')))

    def test_is_False_if_inner_is_True(self):
        tc = TrueCriterion()
        nc = NotCriterion(tc)
        self.assertFalse(nc.applies_to(MockItem('Anything')))


class TestAnyOfCriterion(unittest.TestCase):

    def test_is_True_if_at_least_one_item_is_True(self):
        c = MagicMock()
        c.applies_to = MagicMock(side_effect=[False, True])
        aoc = AnyOfCriterion(c)
        self.assertTrue(aoc.applies_to([7, 9]))
        self.assertEquals(
            c.applies_to.mock_calls,
            [call.applies_to(7), call.applies_to(9)])

    def test_is_False_if_all_items_are_False(self):
        c = MagicMock()
        c.applies_to = MagicMock(side_effect=[False, False])
        aoc = AnyOfCriterion(c)
        self.assertFalse(aoc.applies_to([3, 6]))
        self.assertEquals(
            c.applies_to.mock_calls,
            [call.applies_to(3), call.applies_to(6)])
