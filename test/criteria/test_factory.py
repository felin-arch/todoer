import unittest

from app.criteria.repository import NoSuchCriterionDefinitionError
from ddt import ddt, data, unpack
from app.criteria.factory import CriterionFactory, InvalidCriterionDescriptorError
from app.criteria.logical import *
from app.criteria.item import *
from app.criteria.project import *
from app.criteria.label import *
import app.criteria.logical
import app.criteria.item
import app.criteria.project
import app.criteria.label

@ddt
class TestCriterionFactory(unittest.TestCase):
    def setUp(self):
        self.criterion_factory = CriterionFactory([
            app.criteria.logical,
            app.criteria.item,
            app.criteria.project,
            app.criteria.label
        ])

    @data([{'true': ''}, TrueCriterion],
          [{'false': ''}, FalseCriterion],
          [{'item_has_due_date': ''}, ItemHasDueDateCriterion])
    @unpack
    def test_given_simple_definition_constructs_criterion(self, definition, klass):
        criterion = self.criterion_factory.create(definition)
        self.assertIsInstance(criterion, klass)

    def test_given_definition_with_multiple_keys_raises_error(self):
        with self.assertRaises(InvalidCriterionDescriptorError) as ctx:
            self.criterion_factory.create({'true': '', 'false': ''})

        self.assertEquals(str(ctx.exception), 'Descriptor should only have a single key')

    def test_given_nonexistent_criterion_raises_error(self):
        with self.assertRaises(NoSuchCriterionDefinitionError) as ctx:
            self.criterion_factory.create({'non-existent': ''})

        self.assertEquals(str(ctx.exception), 'No such criterion definition: non-existent')

    @data([{'project_name_equals': 'Test'}, ProjectNameEqualsCriterion, {'project_name': 'Test'}],
          [{'project_name_starts_with': '*'}, ProjectNameStartsWithCriterion, {'name_prefix': '*'}],
          [{'label_name_equals': 'nice_label'}, LabelNameEqualsCriterion, {'label_name': 'nice_label'}])
    @unpack
    def test_given_arguments_constructs_criterion(self, definition, klass, state):
        criterion = self.criterion_factory.create(definition)
        self.assertIsInstance(criterion, klass)
        self.assertEquals(criterion.__dict__, state)
