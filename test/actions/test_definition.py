import unittest

from app.actions.definition import ActionDefinition
from app.actions.item import AddLabelToItemAction
from test.mocks.actions.simple import TestSimpleAction


class TestActionDefinition(unittest.TestCase):
    def test_equals_true(self):
        a = ActionDefinition(AddLabelToItemAction, ['label'])
        b = ActionDefinition(AddLabelToItemAction, ['label'])
        self.assertTrue(a == b)
        self.assertFalse(a != b)

    def test_equals_false(self):
        a = ActionDefinition(AddLabelToItemAction, ['label'])
        b = ActionDefinition(AddLabelToItemAction, ['label2'])
        self.assertFalse(a == b)
        self.assertTrue(a != b)

    def test_equals_different_type(self):
        a = ActionDefinition(AddLabelToItemAction, ['label'])
        b = ActionDefinition(TestSimpleAction, [])
        self.assertFalse(a == b)
        self.assertTrue(a != b)
