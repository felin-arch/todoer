import logging

class AnyCriterion():

    def __init__(self, criteria):
        self._logger = logging.getLogger('AnyCriterion')
        self._criteria = criteria

    def applies_to(self, item):
        self._logger.debug(
            '`{0}` matches any criteria?'.format(item['content'])
        )
        result = reduce(
            lambda acc, criteria: acc or criteria.applies_to(item),
            self._criteria,
            False
        )
        self._logger.debug(result)
        return result
