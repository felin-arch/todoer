from unittest import TestCase
from ddt import ddt, unpack, data
from app.criteria.repository import (CriteriaRepository, NoSuchCriterionDefinitionError,
                                     CriterionDefinitionCollisionError)
from test.mocks.criterion import (simple, single_argument, todoist_repository,
                                  todoist_repository_and_single_argument)
from test.mocks.criterion.simple import TestSimpleCriterion
from test.mocks.criterion.single_argument import TestSingleArgumentCriterion
from test.mocks.criterion.todoist_repository import TestRequireTodoistRepositoryCriterion
from test.mocks.criterion.todoist_repository_and_single_argument import (
    TestRequireTodoistRepositoryAndSingleArgumentCriterion)
from app.criteria.definition import CriterionDefinition


@ddt
class TestCriteriaRepository(TestCase):
    def test_criterion_not_in_repository_throws_error(self):
        repository = CriteriaRepository([])
        with self.assertRaises(NoSuchCriterionDefinitionError) as ctx:
            repository.get_criterion_definition('not_existing')

        self.assertEquals(str(ctx.exception), 'No such criterion definition: not_existing')

    def test_criterion_name_collision_throws_error(self):
        repository = CriteriaRepository([simple, simple])
        with self.assertRaises(CriterionDefinitionCollisionError) as ctx:
            repository.initialize()

        self.assertEquals(str(ctx.exception), 'test_simple already exists in repository')

    @data([[simple], 'test_simple', CriterionDefinition(TestSimpleCriterion, False)],
          [[single_argument], 'test_single_argument', CriterionDefinition(TestSingleArgumentCriterion, False)],
          [[todoist_repository], 'test_require_todoist_repository',
           CriterionDefinition(TestRequireTodoistRepositoryCriterion, True)],
          [[todoist_repository_and_single_argument], 'test_require_todoist_repository_and_single_argument',
           CriterionDefinition(TestRequireTodoistRepositoryAndSingleArgumentCriterion, True)])
    @unpack
    def test_module_criteria_correctly_register_in_repository(
            self, modules, criterion_name, expected_definition
    ):
        repository = CriteriaRepository(modules)
        repository.initialize()

        criterion_definition = repository.get_criterion_definition(criterion_name)
        self.assertEquals(criterion_definition, expected_definition)

    def test_multiple_module_criteria_correctly_register_in_repository(self):
        repository = CriteriaRepository([simple, todoist_repository])
        repository.initialize()

        criterion_definition = repository.get_criterion_definition('test_simple')
        self.assertEquals(criterion_definition, CriterionDefinition(TestSimpleCriterion, False))

        criterion_definition = repository.get_criterion_definition('test_require_todoist_repository')
        self.assertEquals(criterion_definition,
                          CriterionDefinition(TestRequireTodoistRepositoryCriterion, True))
