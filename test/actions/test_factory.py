import unittest
from unittest.mock import MagicMock

import app.actions.item
from app.actions.factory import ActionFactory, InvalidActionDescriptorError, ActionConstructionError
from app.actions.item import AddLabelToItemAction
from app.actions.repository import ActionsRepository, NoSuchActionDefinitionError


class TestActionFactory(unittest.TestCase):
    def setUp(self):
        self.todoist_repository_mock = MagicMock()
        criteria_repository = ActionsRepository([
            app.actions.item
        ])
        criteria_repository.initialize()
        self.criterion_factory = ActionFactory(criteria_repository, self.todoist_repository_mock)

    def test_given_definition_with_multiple_keys_raises_error(self):
        with self.assertRaises(InvalidActionDescriptorError) as ctx:
            self.criterion_factory.create({'true': '', 'false': ''})

        self.assertEquals(str(ctx.exception), 'Descriptor should only have a single key')

    def test_given_nonexistent_criterion_raises_error(self):
        with self.assertRaises(NoSuchActionDefinitionError) as ctx:
            self.criterion_factory.create({'non-existent': ''})

        self.assertEquals(str(ctx.exception), 'No such action definition: non-existent')

    def test_given_arguments_needing_lookup_constructs_criterion(self):
        self.todoist_repository_mock.get_label_by_name.return_value = 'TestLabel'

        action = self.criterion_factory.create({'add_label_to_item': 'Test'})

        self.assertIsInstance(action, AddLabelToItemAction)
        self.assertEquals(action.__dict__, {'label': 'TestLabel'})
        self.todoist_repository_mock.get_label_by_name.assert_called_with('Test')

    def test_given_arguments_failed_lookup_raises_error(self):
        self.todoist_repository_mock.get_label_by_name.return_value = None

        with self.assertRaises(ActionConstructionError) as ctx:
            self.criterion_factory.create({'add_label_to_item': 'Test'})

        self.assertEquals(str(ctx.exception), 'Could not resolve necessary label: Test')
