import unittest

from app.actions.item import AddLabelToItemAction, NullAction
from test.mocks import MockItem, MockLabel


class TestNullAction(unittest.TestCase):
    def test_null_action_does_nothing(self):
        item = MockItem()
        original = item.__dict__

        action = NullAction()
        action.apply_to(item)

        self.assertEqual(original, item.__dict__)


class TestAddLabelToItemAction(unittest.TestCase):
    def test_label_added_to_item(self):
        item = MockItem()
        label = MockLabel()

        action = AddLabelToItemAction(label)
        action.apply_to(item)

        self.assertIn(label['id'], item['labels'])

    def test_label_not_added_to_item_if_it_is_already_present(self):
        label = MockLabel()
        item = MockItem(labels=[label['id']])

        action = AddLabelToItemAction(label)
        action.apply_to(item)

        self.assertIn(label['id'], item['labels'])
        self.assertEquals(1, len(item['labels']))
