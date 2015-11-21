import logging

class HasLabelCriterion():

    def __init__(self, label):
        self._logger = logging.getLogger('HasLabelCriterion')
        self._label = label

    def applies_to(self, item):
        self._logger.debug(
            '`{0}` has `{1}` label?'.format(
                item['content'], self._label['name']
            )
        )
        result = self._label['id'] in item['labels']
        self._logger.debug('{0}'.format(result))
        return result
