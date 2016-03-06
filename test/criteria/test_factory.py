import unittest
from ddt import ddt, data, unpack
from app.criteria.factory import CriterionFactory, InvalidCriterionDefinitionError
from app.criteria.logical import *
from app.criteria.item import *
from app.criteria.project import *

@ddt
class TestCriterionFactory(unittest.TestCase):

    def setUp(self):
        self.criterion_factory = CriterionFactory()

    @data( [ { 'true': '' }, TrueCriterion ],
           [ { 'false': '' }, FalseCriterion ],
           [ { 'item_has_due_date': '' }, ItemHasDueDateCriterion ])
    @unpack
    def test_given_simple_definition_constructs_criterion(self, definition, klass):
        criterion = self.criterion_factory.create(definition)
        self.assertIsInstance(criterion, klass)

    def test_given_definition_with_multiple_keys_raises_error(self):
        with self.assertRaises(InvalidCriterionDefinitionError) as ctx:
            self.criterion_factory.create({ 'true': '', 'false': '' })

        self.assertEquals(str(ctx.exception), 'Definition should only have a single key')

    def test_given_nonexistent_criterion_raises_error(self):
        with self.assertRaises(InvalidCriterionDefinitionError) as ctx:
            self.criterion_factory.create({ 'non-existent': '' })

        self.assertEquals(str(ctx.exception), 'No such criterion: non-existent')

    # @data([
    #     { 'project_name_equals': 'Test' },
    #     ProjectNameEqualsCriterion,
    #     { 'project_name': 'Test' }
    #     ])
    # @unpack
    # def test_given_arguments_constructs_criterion(self, definition, klass, state):
    #     criterion = self.criterion_factory.create(definition)
    #     self.assertIsInstance(criterion, klass)
    #     self.assertEquals(criterion.__dict__, state)