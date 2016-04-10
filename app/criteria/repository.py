import inspect
from app.util import NameConverter
from app.criteria.definition import CriterionDefinition


class CriteriaRepository:
    def __init__(self, criterion_categories):
        self._criterion_categories = criterion_categories
        self._repository = {}

    def initialize(self):
        self._repository = {}
        item_criteria = self._discover_criteria()
        for criterion_name, klass in item_criteria:
            self._register_criterion(criterion_name, klass)

    def _discover_criteria(self):
        criteria = []
        for criterion_category in self._criterion_categories:
            criteria.extend(inspect.getmembers(criterion_category, inspect.isclass))

        return criteria

    def get_criterion_definition(self, criterion_label):
        if criterion_label not in self._repository.keys():
            raise NoSuchCriterionDefinitionError('No such criterion definition: {0}'.format(criterion_label))

        return self._repository[criterion_label]

    def _register_criterion(self, criterion_name, klass):
        should_inject_todoist = self._should_inject_todoist_in_constructor(klass)
        criterion_name = NameConverter.convert_criterion_name(criterion_name)

        if criterion_name in self._repository.keys():
            raise CriterionDefinitionCollisionError()

        self._repository[criterion_name] = CriterionDefinition(klass, should_inject_todoist)

    @staticmethod
    def _should_inject_todoist_in_constructor(klass):
        parameters = inspect.signature(klass.__init__).parameters.values()
        return any([parameter.name == 'todoist_repository' for parameter in parameters])


class NoSuchCriterionDefinitionError(RuntimeError):
    pass


class CriterionDefinitionCollisionError(RuntimeError):
    pass
