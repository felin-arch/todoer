from app.criteria.repository import CriteriaRepository


class CriterionFactory:
    def __init__(self, modules):
        self._criteria_repository = CriteriaRepository(modules)
        self._criteria_repository.load_criteria()

    def create(self, descriptor):
        return self._construct_criterion(*self._unpack_descriptor(descriptor))

    @staticmethod
    def _unpack_descriptor(descriptor):
        if len(descriptor.keys()) is not 1:
            raise InvalidCriterionDescriptorError('Descriptor should only have a single key')

        return descriptor.popitem()

    def _construct_criterion(self, criterion_type, arguments):
        definition = self._criteria_repository.get_criterion_definition(criterion_type)
        prepared_arguments = self._prepare_arguments(arguments)

        return definition['class'](*prepared_arguments)

    @staticmethod
    def _prepare_arguments(arguments):
        return [arg for arg in [arguments] if arg is not '']


class InvalidCriterionDescriptorError(RuntimeError):
    pass
