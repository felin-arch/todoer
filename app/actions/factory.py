import logging

from app.actions.repository import ActionsRepository
from app.todoist import TodoistRepository


class ActionFactory:
    def __init__(self, actions_repository: ActionsRepository, todoist_repository: TodoistRepository):
        self._actions_repository = actions_repository
        self._todoist_repository = todoist_repository
        self._logger = logging.getLogger('ActionFactory')
        self._log_indent = 0

    def create(self, action_descriptor):
        action_type, argument_descriptors = self._unpack_descriptor(action_descriptor)

        self._log_build_start(action_type)
        action = self._construct_action(action_type, argument_descriptors)
        self._log_build_end(action_type)

        return action

    def _log_build_end(self, criterion_type):
        self._log_indent -= 1
        self._log('\u2517  built {0}'.format(criterion_type))

    def _log_build_start(self, criterion_type):
        self._log('\u250f  building {0}'.format(criterion_type))
        self._log_indent += 1

    @staticmethod
    def _unpack_descriptor(action_descriptor):
        if len(action_descriptor.keys()) is not 1:
            raise InvalidActionDescriptorError('Descriptor should only have a single key')

        return action_descriptor.popitem()

    def _construct_action(self, criterion_type, argument_descriptors):
        definition = self._actions_repository.get_action_definition(criterion_type)
        arguments = self._construct_arguments(definition, argument_descriptors)

        return definition.class_(*arguments)

    def _construct_arguments(self, definition, argument_descriptors):
        raw_arguments = [argument_descriptors]
        arguments = []

        for parameter_definition, raw_argument in zip(definition.parameters, raw_arguments):
            arguments.append(self._construct_argument(parameter_definition, raw_argument))

        return arguments

    def _construct_argument(self, parameter_definition, parameter):
        if parameter_definition is 'label':
            return self._construct_label_argument(parameter)

        return None

    def _construct_label_argument(self, parameter):
        self._log(' arg: `label({0})`'.format(parameter))
        label = self._todoist_repository.get_label_by_name(parameter)
        if not label:
            raise ActionConstructionError('Could not resolve necessary label: {0}'.format(parameter))

        return label

    def _log(self, message):
        self._logger.debug('{0}{1}'.format(self._get_log_prefix(), message))

    def _get_log_prefix(self):
        return '\u2503 ' * self._log_indent


class InvalidActionDescriptorError(RuntimeError):
    pass


class ActionConstructionError(RuntimeError):
    pass
