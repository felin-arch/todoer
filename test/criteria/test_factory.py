import unittest
from unittest.mock import MagicMock

from app.criteria.repository import NoSuchCriterionDefinitionError, CriteriaRepository
from app.criteria.factory import CriterionFactory, InvalidCriterionDescriptorError
from app.criteria.logical import AllCriterion, NotCriterion, TrueCriterion, FalseCriterion
from app.criteria.project import ProjectNameEqualsCriterion
from app.criteria.item import ProjectOfItemCriterion
import app.criteria.logical
import app.criteria.item
import app.criteria.project
import app.criteria.label


class TestCriterionFactory(unittest.TestCase):
    def setUp(self):
        self.todoist_repository_mock = MagicMock()
        criteria_repository = CriteriaRepository([
            app.criteria.logical,
            app.criteria.item,
            app.criteria.project,
            app.criteria.label
        ])
        criteria_repository.initialize()
        self.criterion_factory = CriterionFactory(criteria_repository, self.todoist_repository_mock)

    def test_given_simple_definition_constructs_criterion(self):
        criterion = self.criterion_factory.create({'true': ''})
        self.assertIsInstance(criterion, TrueCriterion)

    def test_given_definition_with_multiple_keys_raises_error(self):
        with self.assertRaises(InvalidCriterionDescriptorError) as ctx:
            self.criterion_factory.create({'true': '', 'false': ''})

        self.assertEquals(str(ctx.exception), 'Descriptor should only have a single key')

    def test_given_nonexistent_criterion_raises_error(self):
        with self.assertRaises(NoSuchCriterionDefinitionError) as ctx:
            self.criterion_factory.create({'non-existent': ''})

        self.assertEquals(str(ctx.exception), 'No such criterion definition: non-existent')

    def test_given_arguments_constructs_criterion(self):
        criterion = self.criterion_factory.create({'project_name_equals': 'Test'})
        self.assertIsInstance(criterion, ProjectNameEqualsCriterion)
        self.assertEquals(criterion.__dict__, {'project_name': 'Test'})

    def test_given_single_inner_criterion_constructs_correctly(self):
        definition = {'not': {'true': ''}}
        criterion = self.criterion_factory.create(definition)
        self.assertIsInstance(criterion, NotCriterion)
        self.assertIsInstance(criterion.criterion, TrueCriterion)

    def test_given_multiple_inner_criteria_constructs_correctly(self):
        definition = {'all': [{'true': ''}, {'false': ''}]}
        criterion = self.criterion_factory.create(definition)
        self.assertIsInstance(criterion, AllCriterion)
        self.assertIsInstance(criterion.criteria[0], TrueCriterion)
        self.assertIsInstance(criterion.criteria[1], FalseCriterion)

    def test_given_todoist_repository_injection_should_construct_correctly(self):
        definition = {'project_of_item': {'true': ''}}
        criterion = self.criterion_factory.create(definition)
        self.assertIsInstance(criterion, ProjectOfItemCriterion)
        self.assertIsInstance(criterion.criterion, TrueCriterion)
        self.assertEquals(criterion.todoist_repository, self.todoist_repository_mock)



        # @data([{'labels_of_item': 'Test'}, LabelsOfItemCriterion, {'project_name': 'Test'}],
        #       [{'project_of_item': '*'}, ProjectOfItemCriterion, {'name_prefix': '*'}])
        # @unpack
        # def test_criterion_requires_todoist_injected_correctly(self, definition, klass, state):
        #     pass
