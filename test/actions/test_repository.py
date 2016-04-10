from unittest import TestCase

from ddt import ddt, unpack, data

from app.actions.repository import (ActionsRepository, NoSuchActionDefinitionError,
                                    ActionDefinitionCollisionError)
from test.mocks.actions import simple, another_simple
from test.mocks.actions.another_simple import TestAnotherSimpleAction
from test.mocks.actions.simple import TestSimpleAction


@ddt
class TestActionsRepository(TestCase):
    def test_action_not_in_repository_throws_error(self):
        repository = ActionsRepository([])
        with self.assertRaises(NoSuchActionDefinitionError) as ctx:
            repository.get_action_definition('not_existing')

        self.assertEquals(str(ctx.exception), 'No such action definition: not_existing')

    def test_action_name_collision_throws_error(self):
        repository = ActionsRepository([simple, simple])
        with self.assertRaises(ActionDefinitionCollisionError) as ctx:
            repository.initialize()

        self.assertEquals(str(ctx.exception), 'Definition collision: test_simple')

    @data([[simple], 'test_simple', TestSimpleAction])
    @unpack
    def test_module_actions_correctly_register_in_repository(
            self, modules, criterion_name, expected_definition
    ):
        repository = ActionsRepository(modules)
        repository.initialize()

        criterion_definition = repository.get_action_definition(criterion_name)
        self.assertEquals(criterion_definition, expected_definition)

    def test_multiple_module_actions_correctly_register_in_repository(self):
        repository = ActionsRepository([simple, another_simple])
        repository.initialize()

        action_definition = repository.get_action_definition('test_simple')
        self.assertEquals(action_definition, TestSimpleAction)

        action_definition = repository.get_action_definition('test_another_simple')
        self.assertEquals(action_definition, TestAnotherSimpleAction)
