from app.criteria.logical import *
from app.criteria.item import *
from app.criteria.project import *

MAPPING = {
    'true': TrueCriterion,
    'false': FalseCriterion,

    'item_has_due_date': ItemHasDueDateCriterion,

    'project_name_equals': ProjectNameEqualsCriterion
}

class CriterionFactory():

    def __init__(self):
        pass

    def create(self, definition):
        criterion_type, arguments = self._unpack_definition(definition)
        CriterionClass = self._get_criterion_class(criterion_type)

        return CriterionClass()

    def _unpack_definition(self, definition):
        if len(definition.keys()) is not 1:
            raise InvalidCriterionDefinitionError('Definition should only have a single key')

        return definition.popitem()

    def _get_criterion_class(self, criterion_type):
        if criterion_type not in MAPPING:
            raise InvalidCriterionDefinitionError(
                'No such criterion: {0}'.format(criterion_type))

        return MAPPING[criterion_type]


class InvalidCriterionDefinitionError(RuntimeError):
    pass
