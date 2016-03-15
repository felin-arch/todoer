from app.criteria.logical import *
from app.criteria.item import *
from app.criteria.project import *
from app.criteria.label import *

MAPPING = {
    'true': TrueCriterion,
    'false': FalseCriterion,

    'item_has_due_date': ItemHasDueDateCriterion,

    'project_name_equals': ProjectNameEqualsCriterion,
    'project_name_starts_with': ProjectNameStartsWithCriterion,

    'label_name_equals': LabelNameEqualsCriterion
}


class CriterionFactory:
    def __init__(self):
        pass

    def create(self, definition):
        return self._construct_criterion(*self._unpack_definition(definition))

    @staticmethod
    def _unpack_definition(definition):
        if len(definition.keys()) is not 1:
            raise InvalidCriterionDefinitionError('Definition should only have a single key')

        return definition.popitem()

    def _construct_criterion(self, criterion_type, arguments):
        criterion_class = self._get_criterion_class(criterion_type)
        prepared_arguments = self._prepare_arguments(arguments)

        return criterion_class(*prepared_arguments)

    @staticmethod
    def _get_criterion_class(criterion_type):
        if criterion_type not in MAPPING:
            raise InvalidCriterionDefinitionError(
                'No such criterion: {0}'.format(criterion_type))

        return MAPPING[criterion_type]

    @staticmethod
    def _prepare_arguments(arguments):
        return [arg for arg in [arguments] if arg is not '']


class InvalidCriterionDefinitionError(RuntimeError):
    pass
