import unittest

from app.criteria.logical import (AllCriterion, AnyCriterion, FalseCriterion,
                                  NegativeCriterion, TrueCriterion)
from test.mocks import MockItem


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


class TestNegativeCriterion(unittest.TestCase):

    def test_is_True_if_inner_is_False(self):
        fc = FalseCriterion()
        nc = NegativeCriterion(fc)
        self.assertTrue(nc.applies_to(MockItem('Anything')))

    def test_is_False_if_inner_is_True(self):
        tc = TrueCriterion()
        nc = NegativeCriterion(tc)
        self.assertFalse(nc.applies_to(MockItem('Anything')))
