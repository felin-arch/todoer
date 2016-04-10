import unittest

from app.actions.label import AddLabelAction
from test.mocks import MockItem, MockLabel


class TestAddLabelAction(unittest.TestCase):
    def test_label_added_to_item(self):
        item = MockItem()
        label = MockLabel()

        action = AddLabelAction(label)
        action.apply_to(item)

        self.assertIn(label['id'], item['labels'])

    def test_label_not_added_to_item_if_it_is_already_present(self):
        label = MockLabel()
        item = MockItem(labels=[label['id']])

        action = AddLabelAction(label)
        action.apply_to(item)

        self.assertIn(label['id'], item['labels'])
        self.assertEquals(1, len(item['labels']))
