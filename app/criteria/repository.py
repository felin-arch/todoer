import inspect

from app.criteria import Criterion
from app.criteria.definition import CriterionDefinition
from app.criteria.logical import AllCriterion, AnyCriterion, NotCriterion, AnyOfCriterion
from app.util import NameConverter

BASE_CRITERIA = [Criterion, AllCriterion, AnyCriterion, NotCriterion, AnyOfCriterion]


class CriteriaRepository:
    def __init__(self, criterion_categories):
        self._criterion_categories = criterion_categories
        self._repository = {}

    def initialize(self):
        self._repository = {}
        item_criteria = self._discover_criteria()
        for criterion_name, class_ in item_criteria:
            if self._should_register_criterion(class_):
                self._register_criterion(criterion_name, class_)

    def get_criterion_definition(self, criterion_label) -> CriterionDefinition:
        if criterion_label not in self._repository.keys():
            raise NoSuchCriterionDefinitionError('No such criterion definition: {0}'.format(criterion_label))

        return self._repository[criterion_label]

    def _discover_criteria(self):
        criteria = []
        for criterion_category in self._criterion_categories:
            criteria.extend(inspect.getmembers(criterion_category, inspect.isclass))

        return criteria

    @staticmethod
    def _should_register_criterion(class_):
        return issubclass(class_, Criterion) and class_ not in BASE_CRITERIA

    def _register_criterion(self, criterion_name, class_):
        should_inject_todoist = self._should_inject_todoist_in_constructor(class_)
        criterion_name = NameConverter.convert_criterion_name(criterion_name)

        if criterion_name in self._repository.keys():
            raise CriterionDefinitionCollisionError('{0} already exists in repository'.format(criterion_name))

        self._repository[criterion_name] = CriterionDefinition(class_, should_inject_todoist)

    @staticmethod
    def _should_inject_todoist_in_constructor(class_):
        parameters = list(
            [p.name for p in inspect.signature(class_.__init__).parameters.values() if p.name is not 'self'])
        return len(parameters) > 0 and parameters[0] is 'todoist_repository'


class NoSuchCriterionDefinitionError(RuntimeError):
    pass


class CriterionDefinitionCollisionError(RuntimeError):
    pass
