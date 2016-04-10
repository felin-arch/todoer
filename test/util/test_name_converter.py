from unittest import TestCase

from ddt import ddt, data, unpack

from app.util import NameConverter


@ddt
class TestNameConverter(TestCase):
    @data(['TestCriterion', 'test'],
          ['TestSomeOtherCriterion', 'test_some_other'],
          ['AnOtherCriterion', 'an_other'])
    @unpack
    def test_convert_criterion_name(self, name, expected):
        self.assertEquals(NameConverter.convert_criterion_name(name), expected)

    @data(['TestAction', 'test'],
          ['TestSomeOtherAction', 'test_some_other'],
          ['AnOtherAction', 'an_other'])
    @unpack
    def test_convert_criterion_name(self, name, expected):
        self.assertEquals(NameConverter.convert_action_name(name), expected)
