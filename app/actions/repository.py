import inspect

from app.util import NameConverter


class ActionsRepository:
    def __init__(self, action_categories):
        self._action_categories = action_categories
        self._repository = {}

    def initialize(self):
        self._repository = {}
        actions = self._discover_actions()
        for action_name, klass in actions:
            self._register_action(action_name, klass)

    def _discover_actions(self):
        actions = []
        for action_category in self._action_categories:
            actions.extend(inspect.getmembers(action_category, inspect.isclass))

        return actions

    def get_action_definition(self, action_label):
        if action_label not in self._repository.keys():
            raise NoSuchActionDefinitionError('No such action definition: {0}'.format(action_label))

        return self._repository[action_label]

    def _register_action(self, action_name, klass):
        action_name = NameConverter.convert_action_name(action_name)

        if action_name in self._repository.keys():
            raise ActionDefinitionCollisionError('Definition collision: {0}'.format(action_name))

        self._repository[action_name] = klass


class NoSuchActionDefinitionError(RuntimeError):
    pass


class ActionDefinitionCollisionError(RuntimeError):
    pass
