import logging

class HasDueDateCriterion():

    def __init__(self):
        self._logger = logging.getLogger('HasDueDateCriterion')

    def applies_to(self, item):
        self._logger.debug('`{0}` has due date?'.format(item['content']))
        result = item['due_date'] is not None
        self._logger.debug('{0}'.format(result))
        return result
