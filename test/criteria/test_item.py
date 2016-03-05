import unittest
from unittest.mock import MagicMock

from app.criteria.item import (ItemHasDueDateCriterion, ItemHasLabelCriterion,
                               ItemsProjectCriterion, ItemIsNthInProjectCriterion)
from app.criteria.logical import FalseCriterion, TrueCriterion
from test.mocks import MockItem, MockLabel, MockProject


class TestItemHasLabelCriterion(unittest.TestCase):

    def test_item_has_label_returns_True(self):
        l = MockLabel(id=1)
        i = MockItem(labels=[1])

        ic = ItemHasLabelCriterion(l)

        self.assertTrue(ic.applies_to(i))

    def test_item_has_other_labels_returns_False(self):
        l = MockLabel(id=1)
        i = MockItem(labels=[2, 3, 4])

        ic = ItemHasLabelCriterion(l)

        self.assertFalse(ic.applies_to(i))


class TestItemHasDueDate(unittest.TestCase):

    def test_item_has_no_due_date_returns_False(self):
        i = MockItem()

        ic = ItemHasDueDateCriterion()

        self.assertFalse(ic.applies_to(i))

    def test_item_has_due_date_returns_True(self):
        i = MockItem(due_date='2016-01-01')

        ic = ItemHasDueDateCriterion()

        self.assertTrue(ic.applies_to(i))


class TestItemsProjectCriterion(unittest.TestCase):

    def setUp(self):
        self.todoist = MagicMock()
        self.project_id = 1234
        self.mockItem = MockItem(project_id=self.project_id)

    def test_no_such_project_returns_False(self):
        self.todoist.get_project_by_id.return_value = None

        ic = ItemsProjectCriterion(self.todoist, TrueCriterion())

        self.assertFalse(ic.applies_to(self.mockItem))
        self.todoist.get_project_by_id.assert_called_with(self.project_id)

    def test_project_criteria_matches_returns_True(self):
        self.todoist.get_project_by_id.return_value = MockProject()

        ic = ItemsProjectCriterion(self.todoist, TrueCriterion())

        self.assertTrue(ic.applies_to(self.mockItem))
        self.todoist.get_project_by_id.assert_called_with(self.project_id)

    def test_project_criteria_does_not_match_returns_False(self):
        self.todoist.get_project_by_id.return_value = MockProject()

        ic = ItemsProjectCriterion(self.todoist, FalseCriterion())

        self.assertFalse(ic.applies_to(self.mockItem))
        self.todoist.get_project_by_id.assert_called_with(self.project_id)


class TestItemIsNthInProjectCriterio(unittest.TestCase):

    def test_item_is_nth_in_project_returns_True(self):
        t = MagicMock()
        i = MockItem(item_order=2, project_id=1234)
        t.get_items_by_project.return_value = [
            MockItem(item_order=0), MockItem(item_order=1), i
        ]

        ic = ItemIsNthInProjectCriterion(t, 3)

        self.assertTrue(ic.applies_to(i))
        t.get_items_by_project.assert_called_with(1234)

    def test_item_is_not_nth_in_project_returns_False(self):
        t = MagicMock()
        i = MockItem(item_order=2, project_id=1234)
        t.get_items_by_project.return_value = [
            MockItem(item_order=0), MockItem(item_order=1), i
        ]

        ic = ItemIsNthInProjectCriterion(t, 1)

        self.assertFalse(ic.applies_to(i))
        t.get_items_by_project.assert_called_with(1234)
