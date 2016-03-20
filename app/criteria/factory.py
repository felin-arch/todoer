class CriterionFactory:
    def __init__(self, criteria_repository, todoist_repository):
        self._criteria_repository = criteria_repository
        self._todoist_repository = todoist_repository

    def create(self, descriptor):
        return self._construct_criterion(*self._unpack_descriptor(descriptor))

    @staticmethod
    def _unpack_descriptor(descriptor):
        if len(descriptor.keys()) is not 1:
            raise InvalidCriterionDescriptorError('Descriptor should only have a single key')

        return descriptor.popitem()

    def _construct_criterion(self, criterion_type, arguments):
        definition = self._criteria_repository.get_criterion_definition(criterion_type)
        arguments = self._prepare_arguments(arguments)

        return definition['class'](*arguments)

    def _prepare_arguments(self, arguments):
        return [self._transform_argument(argument) for argument in [arguments] if argument is not '']

    def _transform_argument(self, argument):
        if self._is_criterion_definition(argument):
            return self.create(argument)
        if self._is_criterion_definition_collection(argument):
            return list([self.create(item) for item in argument])

        return argument

    @staticmethod
    def _is_criterion_definition(argument):
        return isinstance(argument, dict)

    @staticmethod
    def _is_criterion_definition_collection(argument):
        return isinstance(argument, list)


class InvalidCriterionDescriptorError(RuntimeError):
    pass
