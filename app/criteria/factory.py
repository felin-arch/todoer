import logging


class CriterionFactory:
    def __init__(self, criteria_repository, todoist_repository):
        self._criteria_repository = criteria_repository
        self._todoist_repository = todoist_repository
        self._logger = logging.getLogger('CriterionFactory')
        self._log_indent = 0

    def create(self, criterion_descriptor):
        criterion_type, argument_descriptors = self._unpack_descriptor(criterion_descriptor)

        self._log_build_start(criterion_type)
        criterion = self._construct_criterion(criterion_type, argument_descriptors)
        self._log_build_end(criterion_type)

        return criterion

    def _log_build_end(self, criterion_type):
        self._log_indent -= 1
        self._log('\u2517  built {0}'.format(criterion_type))

    def _log_build_start(self, criterion_type):
        self._log('\u250f  building {0}'.format(criterion_type))
        self._log_indent += 1

    @staticmethod
    def _unpack_descriptor(criterion_descriptor):
        if len(criterion_descriptor.keys()) is not 1:
            raise InvalidCriterionDescriptorError('Descriptor should only have a single key')

        return criterion_descriptor.popitem()

    def _construct_criterion(self, criterion_type, argument_descriptors):
        definition = self._criteria_repository.get_criterion_definition(criterion_type)
        arguments = self._construct_arguments(definition, argument_descriptors)

        return definition.klass(*arguments)

    def _construct_arguments(self, definition, argument_descriptors):
        arguments = [self._todoist_repository] if definition.should_inject_todoist_repository else []
        if self._is_not_empty(argument_descriptors):
            arguments.append(self._construct_argument(argument_descriptors))

        return arguments

    @staticmethod
    def _is_not_empty(argument):
        return argument is not '' and argument is not None

    def _construct_argument(self, argument):
        if self._is_criterion_definition(argument):
            self._log_criterion_definition(argument)
            return self.create(argument)

        if self._is_criterion_definition_collection(argument):
            self._log_criterion_definition_collection(argument)
            return list([self.create(item) for item in argument])

        self._log_pure_argument(argument)
        return argument

    @staticmethod
    def _is_criterion_definition(argument):
        return isinstance(argument, dict)

    def _log_criterion_definition(self, argument):
        self._log(' arg: `{0}` criterion'.format(list(argument.keys())[0]))

    @staticmethod
    def _is_criterion_definition_collection(argument):
        return isinstance(argument, list)

    def _log_criterion_definition_collection(self, argument):
        self._log(' args: {0}'.format(', '.join(['`{0}` criterion'.format(list(item.keys())[0]) for item in argument])))

    def _log_pure_argument(self, argument):
        self._log(' arg: `{0}`'.format(argument))

    def _log(self, message):
        self._logger.debug('{0}{1}'.format(self._get_log_prefix(), message))

    def _get_log_prefix(self):
        return '\u2503 ' * self._log_indent


class InvalidCriterionDescriptorError(RuntimeError):
    pass
