import logging

class NegativeCriterion():

    def __init__(self, criterion):
        self._logger = logging.getLogger('NegativeCriterion')
        self._criterion = criterion

    def applies_to(self, item):
        self._logger.debug('{0}` not matches criteria?'.format(item['content']))
        result = not self._criterion.applies_to(item)
        self._logger.debug(result)
        return result
