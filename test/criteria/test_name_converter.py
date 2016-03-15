from unittest import TestCase

from app.criteria.name_converter import CriterionNameConverter
from ddt import ddt, data, unpack


@ddt
class TestCriterionNameConverter(TestCase):
    @data(['TestCriterion', 'test'],
          ['TestSomeOtherCriterion', 'test_some_other'],
          ['AnOtherCriterion', 'an_other'])
    @unpack
    def test_convert_name(self, name, expected):
        self.assertEquals(CriterionNameConverter.convert_name(name), expected)
