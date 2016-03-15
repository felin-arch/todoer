import unittest

from app.criteria.project import *
from test.mocks import MockProject


class TestProjectNameEqualsCriterion(unittest.TestCase):

    def test_project_name_equals_returns_True(self):
        p = MockProject(name='name')
        pc = ProjectNameEqualsCriterion('name')
        self.assertTrue(pc.applies_to(p))

    def test_project_name_does_not_equal_returns_False(self):
        p = MockProject(name='name')
        pc = ProjectNameEqualsCriterion('name_not_equal')
        self.assertFalse(pc.applies_to(p))


class TestProjectNameStartsWithCriterion(unittest.TestCase):

    def test_project_name_starts_with_returns_True(self):
        p = MockProject(name='name is something nice')
        pc = ProjectNameStartsWithCriterion('name')
        self.assertTrue(pc.applies_to(p))

    def test_project_name_does_not_start_with_returns_False(self):
        p = MockProject(name='name is something bad')
        pc = ProjectNameStartsWithCriterion('nama')
        self.assertFalse(pc.applies_to(p))
